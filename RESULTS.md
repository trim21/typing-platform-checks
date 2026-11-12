# Results

All measurements for this tree in one table: three type checkers, each in a
baseline state and a patched state (pyright in two patch branches). 2026-11-12,
Linux host; every case was also run with a Windows target and produced the same
verdict, so one table is shown. `case14`–`case16` have no Windows twin because
they reference no platform-specific API.

## States

| Column | Checker | Version / revision |
| --- | --- | --- |
| `pyright` | pyright | 1.1.414, `microsoft/pyright` `main` at `227769493` |
| `pyright+` | pyright | 1.1.414 + `trim21/pyright` `final-literal-type` at `10836da98` (microsoft/pyright#12000): a module-scope annotated `Final` exposes the literal value of its initializer |
| `pyright++` | pyright | 1.1.414 + `trim21/pyright` `final-static-condition` at `2f4cbcc13`, a separate branch off `main`: a bare `Final` counts as a static condition in reachability analysis. Not stacked on `pyright+` |
| `ty` | ty | 0.0.100, `astral-sh/ty` `main` at `6c90fe0` |
| `ty+` | ty | astral-sh/ruff#30255 at `1ca929eefe`: a module-level `Final` exposes the type inferred from its bindings when that type is a `Literal[…]`, keeping the `FINAL` qualifier |
| `mypy` | mypy | `python/mypy` `master` at `5dc284074` (`mypy 2.5.0+dev`) |
| `mypy+` | mypy | python/mypy#22428 at `ff56d9b99`: a module-level annotated `Final` records the literal value of its initializer, and a `Final[bool]` initialized from a static platform/version check folds to `Literal[True]`/`Literal[False]` |

The local `mypy 2.4.1` release behaves the same as the `5dc284074` baseline case
for case, including `case14`–`case16`.

`ty 0.0.100` still does not contain astral-sh/ruff#30255: `case5`, `case7`,
`case12` and `case13` fail exactly as they did at `0.0.99`, so the `ty+` column
remains a patch state rather than a released one. That column is still measured at
the PR revision listed above; the three cases added after that measurement are
marked `—` there.

Invocation, one case directory at a time, from the repository root:

```bash
pyright --pythonplatform Linux --pythonversion 3.12 pass/linux/<case>
ty check --python-platform linux pass/linux/<case>
mypy --platform linux --no-incremental pass/linux/<case>
```

Windows runs use `--pythonplatform Windows`, `--python-platform win32`,
`--platform win32`. The ty spelling matters: `--python-platform windows` is not
the accepted value and is not rejected either — it silently loses platform
evaluation, so every `fail/windows` case reports nothing.

## Summary

`✓` = matches the expectation (`pass/` → zero errors, `fail/` → at least one
error), `✗` = does not, `—` = not measured.

| Case | pyright | pyright+ | pyright++ | ty | ty+ | mypy | mypy+ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `pass` `case1_inline_check` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `pass` `case2_same_module_bare_final` | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case3_same_module_annotated_final` | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case4_import_bare_final` | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case5_import_annotated_final` | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| `pass` `case6_module_attr_bare_final` | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case7_module_attr_annotated_final` | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| `pass` `case8_dead_branch_not_analyzed` | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case9_type_bare_final` | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case10_type_annotated_final` | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| `pass` `case11_type_import_bare_final` | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case12_type_import_annotated_final` | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ |
| `pass` `case13_type_attr_annotated_final` | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ |
| `pass` `case14_type_runtime_value_same_module` | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| `pass` `case15_type_runtime_value_import` | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| `pass` `case16_type_runtime_value_attr` | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| `fail` `case1_unguarded_platform_api` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fail` `case2_mutable_bool_guard` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fail` `case3_nonstatic_final_guard` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fail` `case4_wrong_direction_guard` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

| State | `pass/` satisfied | `fail/` satisfied |
| --- | --- | --- |
| pyright | 9 / 16 | 4 / 4 |
| pyright+ | 11 / 16 | 4 / 4 |
| pyright++ | 10 / 16 | 4 / 4 |
| ty | 12 / 16 | 4 / 4 |
| ty+ | 13 / 16 | 4 / 4 |
| mypy | 4 / 16 | 4 / 4 |
| mypy+ | 7 / 16 | 4 / 4 |

Every `fail/` case stays reported in every state, so no patch trades a real
error for silence. `case14`–`case16` are satisfied by every state measured: no
checker turns a `Final` whose initializer is not statically evaluable into a
literal, so the literal-value work stays confined to values that exist.

## What each checker is missing

Two capabilities decide every `pass/` row. `A` = the literal value reaches the
type of the name. `B` = reachability honours that value, so a guarded branch is
not analyzed.

| State | `A` | `B` | Failing rows |
| --- | --- | --- | --- |
| pyright | annotated `Final` only, same module only | same-module annotated `Final` only | `case2`, `case4`–`case7`, `case12`, `case13` |
| pyright+ | `A` extended across modules | unchanged | `case2`, `case4`–`case7` |
| pyright++ | unchanged (`A` is the `pyright` one) | same-module bare `Final` added | `case4`–`case7`, `case12`, `case13` |
| ty | bare `Final` everywhere; annotated `Final` same module only | both spellings, same module and across modules | `case5`, `case7`, `case12`, `case13` |
| ty+ | `A` extended across modules | unchanged | none |
| mypy | only a literal initializer on an annotated `Final` | inline checks only (syntax driven) | `case2`–`case13` |
| mypy+ | `A` extended to platform-check initializers and across modules | unchanged | `case2`–`case9`, `case11` |

Notes on the individual gaps:

- **pyright** skips a bare `Final` in the reachability analysis: the reference's
  symbol has no typed declaration, so `hasTypedDeclarations()` in
  `codeFlowEngine.ts` short-circuits the check. Cross-module pruning does not
  happen for any form, including a plain imported `Literal[False]` constant,
  because reachability is decided per file and an imported name has no flow node
  in the reading file. That is why `case4`–`case7` fail in every pyright state.
  The `final-static-condition` branch teaches reachability to read the bare
  `Final`'s declaration and closes the same-module row (`case2`) only.
- **ty** already prunes the bare spelling across modules (`case4`, `case6`) and
  already gives it a literal type (`case11`); the annotated spelling loses the
  value at the module boundary, which is exactly what astral-sh/ruff#30255 fixes
  (`case5`, `case7`, `case12`, `case13`).
- **mypy** prunes only inline `sys.platform` conditions, which happen during
  semantic analysis and never consult types. Making `true_only()`/`false_only()`
  in `mypy/typeops.py` honour `last_known_value` closes the `B` gap for
  annotated `Final` but not for the bare spelling, whose type is not yet
  available when the initializer is checked (`case9`, `case11`). That change is
  not part of python/mypy#22428; it was measured separately and keeps the mypy
  test suite green, adding seven `Statement is unreachable` errors to mypy's own
  self check on `Final = False` debug switches such as `mypy/main.py:180`
  (`if MEM_PROFILE:`).
- `case14`–`case16` fail for a checker that reports a literal type for
  `Final[bool] = os.getenv(...) == "1"`; none of the states above does. They are
  the rows that make an over-eager `A` visible, which is why they were added
  alongside the literal-value columns.

## Reading the table

- A `pass/` row that a checker fails is a place where the checker analyzes code
  that cannot run on the target platform, or reports a wider type than the value
  allows.
- Rows are paired by annotation (`case2`/`case3`, `case4`/`case5`,
  `case6`/`case7`, `case11`/`case12`) and by access form (`case4`/`case6`,
  `case5`/`case7`, `case12`/`case13`), so a single `✗` isolates one variable.
- `case1` is the anchor mandated by the typing spec ("Version and platform
  checking"), and `case14`–`case16` follow from it being a platform-check rule:
  a name the checker cannot evaluate keeps its declared type. Everything else is
  beyond the spec; see `README.md`.
