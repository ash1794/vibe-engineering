"""Self-tests for archcheck. Run: python3 -m unittest tools/archcheck/test_archcheck.py"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import archcheck  # noqa: E402


def tree(root, files):
    for rel, body in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(body))


class PythonGraph(unittest.TestCase):
    def test_relative_and_package_imports_and_type_checking(self):
        with tempfile.TemporaryDirectory() as d:
            tree(d, {
                "pkg/__init__.py": "",
                "pkg/a.py": "from . import b\n",
                "pkg/b.py": "from pkg.c import thing\n",
                "pkg/c.py": "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    from . import a\n",
                "pkg/sub/__init__.py": "",
                "pkg/sub/d.py": "from ..a import x\nfrom . import e\n",
                "pkg/sub/e.py": "def f():\n    from pkg import c\n",
            })
            nodes, edges = archcheck.python_graph(os.path.join(d, "pkg"), {"package": "pkg"})
            self.assertEqual(edges["a"], {"b"})
            self.assertEqual(edges["b"], {"c"})
            self.assertNotIn("c", edges)  # TYPE_CHECKING import is not a runtime dependency
            self.assertEqual(edges["sub.d"], {"a", "sub.e"})
            self.assertEqual(edges["sub.e"], {"c"})  # function-local imports still count


class TsGraph(unittest.TestCase):
    def test_alias_relative_dynamic_and_tests_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            tree(d, {
                "lib/x.ts": "import { y } from '@/lib/y';\nexport const x = 1;\n",
                "lib/y.ts": "export type { Z } from './z.js';\n",
                "lib/z.tsx": "const m = await import('../app/page');\n",
                "app/page.tsx": "import '../lib/x'\n",
                "lib/x.test.ts": "import { x } from './x';\n",
            })
            nodes, edges = archcheck.ts_graph(d, {"alias": {"@/": ""}})
            self.assertNotIn("lib/x.test", nodes)
            self.assertEqual(edges["lib/x"], {"lib/y"})
            self.assertEqual(edges["lib/y"], {"lib/z"})
            self.assertEqual(edges["lib/z"], {"app/page"})
            self.assertEqual(archcheck.sccs(nodes, edges), [["app/page", "lib/x", "lib/y", "lib/z"]])


class JavaGraph(unittest.TestCase):
    def test_comments_and_strings_do_not_create_edges(self):
        with tempfile.TemporaryDirectory() as d:
            tree(d, {
                "src/main/java/p/A.java": "package p;\n/** See {@link B}. */\nclass A { String s = \"B\"; }\n",
                "src/main/java/p/B.java": "package p;\nimport q.C;\nclass B { A a; C c; }\n",
                "src/main/java/q/C.java": "package q;\nclass C {}\n",
            })
            nodes, edges = archcheck.java_graph(d, {})
            self.assertNotIn("p.A", edges)
            self.assertEqual(edges["p.B"], {"p.A", "q.C"})


class KotlinGraph(unittest.TestCase):
    def test_package_level_edges_and_tests_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            tree(d, {
                "m/src/main/kotlin/a/A.kt": "package x.a\nimport x.b.B\nimport kotlin.math.max\nclass A\n",
                "m/src/main/kotlin/b/B.kt": "package x.b\nimport x.b.inner.C\nclass B\n",
                "m/src/main/kotlin/b/inner/C.kt": "package x.b.inner\nclass C\n",
                "m/src/test/kotlin/T.kt": "package x.t\nimport x.a.A\n",
            })
            nodes, edges = archcheck.kotlin_graph(d, {})
            self.assertEqual(nodes, {"x.a", "x.b", "x.b.inner"})
            self.assertEqual(edges["x.a"], {"x.b"})
            self.assertEqual(edges["x.b"], {"x.b.inner"})


class SkillsGraph(unittest.TestCase):
    def test_body_references_count_and_frontmatter_does_not(self):
        with tempfile.TemporaryDirectory() as d:
            tree(d, {
                "skill-a/SKILL.md": "---\nname: skill-a\ndescription: Not for B work; use skill-b.\n---\nRun skill-c first.\n",
                "skill-b/SKILL.md": "---\nname: skill-b\n---\nBody.\n",
                "skill-c/SKILL.md": "---\nname: skill-c\n---\nSee skill-a-extra, not a skill.\n",
            })
            nodes, edges = archcheck.skills_graph(d, {})
            self.assertEqual(nodes, {"skill-a", "skill-b", "skill-c"})
            self.assertEqual(dict(edges), {"skill-a": {"skill-c"}})


class Ratchet(unittest.TestCase):
    def run_cli(self, d, *args):
        return subprocess.run([sys.executable, os.path.join(HERE, "archcheck.py"), "--config",
                               os.path.join(d, ".archcheck.json"), *args], capture_output=True, text=True)

    def test_loops_and_layers_ratchet(self):
        with tempfile.TemporaryDirectory() as d:
            tree(d, {"src/a.py": "import b\n", "src/b.py": "import a\n", "src/core.py": "import a\n"})
            cfg = {"version": 1, "graphs": [{"name": "g", "lang": "python", "root": "src",
                                              "layers": [{"name": "core", "modules": ["core"]},
                                                         {"name": "feat", "modules": ["a", "b"]}]}]}
            with open(os.path.join(d, ".archcheck.json"), "w") as fh:
                json.dump(cfg, fh)
            r = self.run_cli(d)
            self.assertEqual(r.returncode, 1)
            self.assertIn("new import loop (2): a <-> b", r.stdout)
            self.assertIn("upward import (lower layer imports higher): core -> a", r.stdout)
            self.assertEqual(self.run_cli(d, "--update-baseline").returncode, 1)  # growth needs a reason
            self.assertEqual(self.run_cli(d, "--update-baseline", "--allow-growth").returncode, 0)
            self.assertEqual(self.run_cli(d).returncode, 0)
            tree(d, {"src/b.py": "x = 1\n"})  # the loop is broken: still passes, and says the baseline can shrink
            r = self.run_cli(d)
            self.assertEqual(r.returncode, 0)
            self.assertIn("baseline can shrink", r.stdout)
            tree(d, {"src/b.py": "import a\nimport core\n", "src/core.py": "import b\n"})  # a bigger loop
            r = self.run_cli(d)
            self.assertEqual(r.returncode, 1)
            self.assertIn("new import loop (3)", r.stdout)


if __name__ == "__main__":
    unittest.main()
