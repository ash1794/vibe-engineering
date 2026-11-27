# archcheck

Keeps this codebase's design matrix lower triangular: every dependency points one way, so any part can be changed, tested and owned by one agent without moving the others.

## Run it

```bash
python3 tools/archcheck/archcheck.py            # CI gate: fails on a new import loop or an upward import
python3 tools/archcheck/archcheck.py --report   # sizes, loops, upward edges, unassigned modules
python3 -m unittest tools/archcheck/test_archcheck.py   # the checker's own tests
```

Config lives in `.archcheck.json` at the repository root: one entry per source tree (`python`, `ts`, `java`, `kotlin` or `skills`), an optional ordered `layers` list (lowest first), and a `baseline` of loops and upward edges that existed when the check was adopted.

## The two rules

1. **No new import loops.** A loop is a set of modules that import each other, directly or through others. Loops in the baseline may shrink or disappear, never grow.
2. **No upward imports.** A module may import its own layer or lower layers only. A function-local import is still an import; `if TYPE_CHECKING:` imports (Python) are not.

## The baseline is a ratchet

- After you break a loop, run `--update-baseline` and commit the smaller baseline with your change.
- `--update-baseline` refuses to record a new loop or upward edge. `--allow-growth` exists for adoption only; a PR that uses it must say why in its description and get a human review.

## How to break a loop

| Situation | Move |
|---|---|
| A hub imports the features it hosts, and the features import the hub | Features register with the hub (a registry in the lower module); the composition root at the top imports the features |
| A cross-cutting concern (privacy export, audit, tenancy) imports every feature | The concern defines an interface or registry; each feature implements or registers it |
| Two modules share helpers | Move the shared code into a new lower module that both import |
| A lower module needs one value from a higher one | Pass it in as an argument or a callback instead of importing |
| A lazy import inside a function hides a loop | Treat it as a failed check, not a fix: apply one of the moves above |

This file and `archcheck.py` are the same in every ash1794 repository (version 1). Change them in all repositories together, or not at all.
