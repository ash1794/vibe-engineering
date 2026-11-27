#!/usr/bin/env python3
"""archcheck: keep a codebase's design matrix lower triangular.

Builds the import graph of each configured source tree and fails when:
  1. an import loop exists that is not inside a recorded baseline loop (loops may shrink, never grow), or
  2. a module imports a module in a higher layer than its own (unless that edge is in the baseline).

Stdlib only. Supports Python (AST), TypeScript/JavaScript (import/require/dynamic import), Java (imports plus
same-package references), Kotlin (package level) and agent skill libraries (SKILL.md body references). Config: .archcheck.json at the repository root (see ARCHCHECK.md next to this file).

Usage:
  python3 tools/archcheck/archcheck.py                  # check, exit 1 on new violations
  python3 tools/archcheck/archcheck.py --report         # print size, edges, loops and layer map per graph
  python3 tools/archcheck/archcheck.py --update-baseline  # rewrite baselines to the current state (shrinks only
                                                           # unless --allow-growth; growth needs a reviewed reason)
"""
from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import os
import re
import sys
from collections import defaultdict

VERSION = 1
DEFAULT_EXCLUDES = ["node_modules", ".git", "__pycache__", ".next", "dist", "build", "coverage", ".venv", "venv"]


# ---------------------------------------------------------------- graph builders
def _walk(root, exts, excludes):
    for dp, dn, fn in os.walk(root):
        rel_dir = os.path.relpath(dp, root)
        dn[:] = sorted(d for d in dn if d not in DEFAULT_EXCLUDES
                       and not any(fnmatch.fnmatch(os.path.normpath(os.path.join(rel_dir, d)), x) for x in excludes)
                       and d not in excludes)
        for f in sorted(fn):
            rel = os.path.normpath(os.path.join(rel_dir, f))
            if f.endswith(exts) and not any(fnmatch.fnmatch(rel, x) or fnmatch.fnmatch(f, x) for x in excludes):
                yield os.path.join(dp, f), rel


def _type_checking_lines(tree):
    """Line ranges of `if TYPE_CHECKING:` bodies; imports there are not runtime dependencies."""
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            t = node.test
            name = t.id if isinstance(t, ast.Name) else t.attr if isinstance(t, ast.Attribute) else None
            if name == "TYPE_CHECKING":
                for b in node.body:
                    spans.append((b.lineno, getattr(b, "end_lineno", b.lineno)))
    return spans


def _strip(name, package):
    """Map an absolute import onto the graph's unit names (drop the package prefix that the root stands for)."""
    if package and (name == package or name.startswith(package + ".")):
        return name[len(package) + 1:]
    return name


def python_graph(root, cfg):
    package = cfg.get("package", "")  # absolute-import prefix that maps to root, e.g. "arena"
    mods = {}
    for path, rel in _walk(root, (".py",), cfg.get("exclude", [])):
        name = rel[:-3].replace(os.sep, ".")
        if name.endswith("__init__"):
            name = name[: -len("__init__")].rstrip(".")
        if name:
            mods[name] = path
    names = set(mods)
    edges = defaultdict(set)
    for m, path in mods.items():
        try:
            tree = ast.parse(open(path, encoding="utf-8", errors="ignore").read())
        except SyntaxError:
            continue
        skip = _type_checking_lines(tree)
        is_pkg = os.path.basename(path) == "__init__.py"
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            if any(a <= node.lineno <= b for a, b in skip):
                continue
            if isinstance(node, ast.Import):
                targets = [a.name for a in node.names]
            else:
                base = node.module or ""
                if node.level:
                    parts = m.split(".") if m else []
                    if not is_pkg:
                        parts = parts[:-1]
                    up = node.level - 1
                    parts = parts[: len(parts) - up] if up else parts
                    base = ".".join(parts + ([base] if base else []))
                # `from base import name`: name is a submodule if one exists, else an attribute of base
                targets = []
                for a in node.names:
                    full = base + "." + a.name if base else a.name
                    targets.append(full if _strip(full, package) in names else base)
            relative = isinstance(node, ast.ImportFrom) and node.level > 0
            for c in targets:
                if package and not relative and not (c == package or c.startswith(package + ".")) \
                        and not cfg.get("bare_imports", False):
                    continue  # an absolute name outside the package (e.g. stdlib `platform`) is not ours
                c = _strip(c, package)
                while c:
                    if c in names:
                        if c != m:
                            edges[m].add(c)
                        break
                    c = c.rsplit(".", 1)[0] if "." in c else ""
    return names, edges


TS_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".mts", ".cjs")
TS_RX = re.compile(r"""(?:^|[;\s])(?:import|export)\s(?:type\s)?[^'"`;]*?from\s*['"]([^'"]+)['"]"""
                   r"""|import\s*\(\s*['"]([^'"]+)['"]\s*\)|require\(\s*['"]([^'"]+)['"]\s*\)|^\s*import\s+['"]([^'"]+)['"]""",
                   re.M)


def ts_graph(root, cfg):
    alias = cfg.get("alias", {})
    excludes = cfg.get("exclude", []) + ["*.test.*", "*.spec.*", "*.d.ts"]
    files = {}
    for path, rel in _walk(root, TS_EXTS, excludes):
        files[os.path.abspath(path)] = re.sub(r"\.(tsx?|jsx?|mjs|mts|cjs)$", "", rel).replace(os.sep, "/")
    absroot = os.path.abspath(root)

    def resolve(src, spec):
        for a, tgt in alias.items():
            if spec.startswith(a):
                spec = os.path.join(absroot, tgt, spec[len(a):])
                break
        else:
            if not spec.startswith("."):
                return None
            spec = os.path.normpath(os.path.join(os.path.dirname(src), spec))
        stem = re.sub(r"\.(js|jsx|mjs|cjs)$", "", spec)
        for c in [spec, stem] + [stem + e for e in TS_EXTS] + [os.path.join(spec, "index" + e) for e in TS_EXTS]:
            if c in files:
                return c
        return None

    edges = defaultdict(set)
    for path, name in files.items():
        text = open(path, encoding="utf-8", errors="ignore").read()
        for mt in TS_RX.finditer(text):
            spec = next(g for g in mt.groups() if g)
            r = resolve(path, spec)
            if r and r != path:
                edges[name].add(files[r])
    return set(files.values()), edges


def java_graph(root, cfg):
    classes = {}
    for path, _ in _walk(root, (".java",), cfg.get("exclude", []) + ["*/test/*", "test"]):
        text = open(path, encoding="utf-8", errors="ignore").read()
        mt = re.search(r"^package\s+([\w.]+);", text, re.M)
        if mt:
            classes[mt.group(1) + "." + os.path.basename(path)[:-5]] = text
    by_pkg = defaultdict(dict)
    for fq in classes:
        pkg, simple = fq.rsplit(".", 1)
        by_pkg[pkg][simple] = fq
    edges = defaultdict(set)
    for fq, text in classes.items():
        pkg = fq.rsplit(".", 1)[0]
        body = re.sub(r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\])*\"", " ", text, flags=re.S)
        for imp in re.findall(r"^import\s+(?:static\s+)?([\w.]+?)(?:\.\*)?;", text, re.M):
            if imp in classes and imp != fq:
                edges[fq].add(imp)
            elif imp in by_pkg:  # wildcard package import
                for other in by_pkg[imp].values():
                    if re.search(r"\b" + other.rsplit(".", 1)[1] + r"\b", body):
                        edges[fq].add(other)
        for simple, other in by_pkg[pkg].items():
            if other != fq and re.search(r"\b" + re.escape(simple) + r"\b", body):
                edges[fq].add(other)
    return set(classes), edges


def kotlin_graph(root, cfg):
    """Kotlin: one unit per package (build modules already forbid loops between modules; this catches loops
    between packages inside one module). An edge is an import that resolves to another package of this tree."""
    pkgs, imports = set(), defaultdict(list)
    for path, _ in _walk(root, (".kt", ".kts"), cfg.get("exclude", []) + ["test", "androidTest", "testFixtures"]):
        text = open(path, encoding="utf-8", errors="ignore").read()
        mt = re.search(r"^package\s+([\w.]+)", text, re.M)
        if not mt:
            continue
        pkgs.add(mt.group(1))
        imports[mt.group(1)] += re.findall(r"^import\s+([\w.]+)", text, re.M)
    edges = defaultdict(set)
    for p, imps in imports.items():
        for imp in imps:
            q = imp
            while q and q not in pkgs:
                q = q.rsplit(".", 1)[0] if "." in q else ""
            if q and q != p:
                edges[p].add(q)
    return pkgs, edges


def skills_graph(root, cfg):
    """Agent skill library: one unit per skill folder; an edge when a SKILL.md body names another skill.

    Routing text is skipped: the YAML frontmatter and any section headed "When NOT to use", "See also" or
    "Related ..." tell an agent which skill to pick instead, they do not make this skill depend on that one.
    Everything else in the body says what the skill runs, so a mention there is a dependency."""
    names = sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "SKILL.md")))
    edges = defaultdict(set)
    for n in names:
        text = open(os.path.join(root, n, "SKILL.md"), encoding="utf-8", errors="ignore").read()
        text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
        text = re.sub(r"(?ims)^(#{1,6})\s*(when not to use|see also|related)\b.*?(?=^#{1,6}\s|\Z)", "", text)
        for o in names:
            if o != n and re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", text):
                edges[n].add(o)
    return set(names), edges


BUILDERS = {"python": python_graph, "ts": ts_graph, "java": java_graph, "kotlin": kotlin_graph,
            "skills": skills_graph}


# ---------------------------------------------------------------- analysis
def sccs(nodes, edges):
    index, low, stack, on, out = {}, {}, [], set(), []
    counter = [0]
    for start in sorted(nodes):
        if start in index:
            continue
        work = [(start, iter(sorted(edges.get(start, ()))))]
        index[start] = low[start] = counter[0]; counter[0] += 1
        stack.append(start); on.add(start)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]; counter[0] += 1
                    stack.append(w); on.add(w)
                    work.append((w, iter(sorted(edges.get(w, ())))))
                    advanced = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop(); on.discard(w); comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    out.append(sorted(comp))
    return sorted(out, key=lambda c: (-len(c), c))


def layer_of(unit, layers):
    for i, layer in enumerate(layers):
        for pat in layer.get("modules", []):
            if fnmatch.fnmatchcase(unit, pat) or unit == pat:
                return i
    return None


def analyse(name, gcfg, repo_root):
    root = os.path.join(repo_root, gcfg["root"])
    nodes, edges = BUILDERS[gcfg["lang"]](root, gcfg)
    edges = {k: {x for x in v if x in nodes} for k, v in edges.items()}
    loops = sccs(nodes, edges)
    layers = gcfg.get("layers", [])
    up_edges, unassigned = [], []
    if layers:
        for n in sorted(nodes):
            if layer_of(n, layers) is None:
                unassigned.append(n)
        for a in sorted(edges):
            la = layer_of(a, layers)
            for b in sorted(edges[a]):
                lb = layer_of(b, layers)
                if la is not None and lb is not None and lb > la:
                    up_edges.append([a, b])
    return {"nodes": nodes, "edges": edges, "loops": loops, "up_edges": up_edges, "unassigned": unassigned}


def check(cfg, repo_root, update=False, allow_growth=False, report=False):
    failures, changed = [], False
    for gcfg in cfg["graphs"]:
        name = gcfg["name"]
        r = analyse(name, gcfg, repo_root)
        base_loops = [sorted(x) for x in gcfg.get("baseline", {}).get("loops", [])]
        base_up = {tuple(x) for x in gcfg.get("baseline", {}).get("up_edges", [])}
        new_loops = [c for c in r["loops"] if not any(set(c) <= set(b) for b in base_loops)]
        new_up = [e for e in r["up_edges"] if tuple(e) not in base_up]
        stale_loops = [b for b in base_loops if not any(set(c) & set(b) and len(c) > 1 for c in r["loops"])]
        n_edges = sum(len(v) for v in r["edges"].values())
        in_loops = sum(len(c) for c in r["loops"])
        largest = len(r["loops"][0]) if r["loops"] else 0
        if report:
            print(f"[{name}] {gcfg['lang']} {gcfg['root']}: {len(r['nodes'])} units, {n_edges} edges, "
                  f"{len(r['loops'])} loops ({in_loops} units, largest {largest}), "
                  f"{len(r['up_edges'])} upward edges, {len(r['unassigned'])} unassigned")
            for c in r["loops"]:
                print(f"    loop {len(c)}: {', '.join(c[:12])}{' ...' if len(c) > 12 else ''}")
            for a, b in r["up_edges"][:40]:
                print(f"    up: {a} -> {b}")
            if r["unassigned"]:
                print(f"    unassigned: {', '.join(r['unassigned'][:20])}{' ...' if len(r['unassigned']) > 20 else ''}")
        if update:
            grow = new_loops or new_up
            if grow and not allow_growth:
                failures.append(f"[{name}] refusing to grow the baseline without --allow-growth")
            else:
                gcfg["baseline"] = {"loops": r["loops"], "up_edges": r["up_edges"]}
                changed = True
            continue
        for c in new_loops:
            failures.append(f"[{name}] new import loop ({len(c)}): {' <-> '.join(c[:10])}{' ...' if len(c) > 10 else ''}")
        for a, b in new_up:
            failures.append(f"[{name}] upward import (lower layer imports higher): {a} -> {b}")
        if gcfg.get("strict_layers") and r["unassigned"]:
            failures.append(f"[{name}] modules not assigned to a layer: {', '.join(r['unassigned'][:10])}")
        if stale_loops or len(base_up) > len(r["up_edges"]) - len(new_up):
            print(f"[{name}] baseline can shrink: run with --update-baseline and commit the result")
    return failures, changed


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--config", default=".archcheck.json")
    p.add_argument("--root", default=None, help="repository root (default: the config file's directory)")
    p.add_argument("--report", action="store_true")
    p.add_argument("--update-baseline", action="store_true")
    p.add_argument("--allow-growth", action="store_true")
    a = p.parse_args(argv)
    cfg_path = os.path.abspath(a.config)
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    repo_root = a.root or os.path.dirname(cfg_path)
    failures, changed = check(cfg, repo_root, a.update_baseline, a.allow_growth, a.report)
    if changed:
        with open(cfg_path, "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=2)
            fh.write("\n")
        print(f"baseline written to {os.path.relpath(cfg_path)}")
    for f in failures:
        print("FAIL " + f)
    if failures:
        print("\nHow to fix: invert the dependency (the lower module defines an interface or registry, the higher one "
              "implements or registers), move shared code down a layer, or wire both from the composition root. "
              "See ARCHCHECK.md.")
        return 1
    if not a.report and not a.update_baseline:
        print("archcheck: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
