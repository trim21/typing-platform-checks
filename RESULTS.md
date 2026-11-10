# Results

All measurements for this tree in one table: three type checkers, each in a
baseline state and a patched state. 2026-11-10, Linux host; every case was also
run with a Windows target and produced the same verdict, so one table is shown.

## States

| Column | Checker | Version / revision |
| --- | --- | --- |
| `pyright` | pyright | 1.1.414, `microsoft/pyright` `main` at `c2b4c6d7110d100cfdde2514955289f2780a43de` |
| `pyright+` | pyright | 1.1.414 + `trim21/pyright` `final-literal-type` at `50088497bb5aba1250c4ca9a51810efda8a382c4` (microsoft/pyright#12000): a module-scope annotated `Final` exposes the literal value of its initializer |
| `ty` | ty | 0.0.99, `astral-sh/ruff` `main` at the merge base of astral-sh/ruff#30255 |
| `ty+` | ty | astral-sh/ruff#30255 at `1ca929eefe`: a module-level `Final` exposes the type inferred from its bindings when that type is a `Literal[…]`, keeping the `FINAL` qualifier |
| `mypy` | mypy | `python/mypy` `master` at `5dc284074` (`mypy 2.5.0+dev`) |
| `mypy+` | mypy | python/mypy#22428 at `ff56d9b99`: a module-level annotated `Final` records the literal value of its initializer, and a `Final[bool]` initialized from a static platform/version check folds to `Literal[True]`/`Literal[False]` |

The local `mypy 2.4.1` release behaves the same as the `5dc284074` baseline case
for case.

Invocation, one case directory at a time:

```bash
pyright --pythonplatform Linux --typeshedpath <typeshed> -p pass/linux/<case>
ty check --python-platform linux pass/linux/<case>
mypy --platform linux --no-incremental pass/linux/<case>
```

Windows runs use `--pythonplatform Windows`, `--python-platform win32`,
`--platform win32`.

## Summary

`✓` = matches the expectation (`pass/` → zero errors, `fail/` → at least one
error), `✗` = does not.

| Case | pyright | pyright+ | ty | ty+ | mypy | mypy+ |
| --- | --- | --- | --- | --- | --- | --- |
| `pass` `case1_inline_check` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `pass` `case2_same_module_bare_final` | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case3_same_module_annotated_final` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case4_import_bare_final` | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case5_import_annotated_final` | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| `pass` `case6_module_attr_bare_final` | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case7_module_attr_annotated_final` | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| `pass` `case8_dead_branch_not_analyzed` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case9_type_bare_final` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case10_type_annotated_final` | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| `pass` `case11_type_import_bare_final` | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `pass` `case12_type_import_annotated_final` | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ |
| `pass` `case13_type_attr_annotated_final` | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ |
| `fail` `case1_unguarded_platform_api` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fail` `case2_mutable_bool_guard` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fail` `case3_nonstatic_final_guard` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `fail` `case4_wrong_direction_guard` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

| State | `pass/` satisfied | `fail/` satisfied |
| --- | --- | --- |
| pyright | 6 / 13 | 4 / 4 |
| pyright+ | 8 / 13 | 4 / 4 |
| ty | 9 / 13 | 4 / 4 |
| ty+ | 13 / 13 | 4 / 4 |
| mypy | 1 / 13 | 4 / 4 |
| mypy+ | 4 / 13 | 4 / 4 |

Every `fail/` case stays reported in every state, so no patch trades a real
error for silence.

## What each checker is missing

Two capabilities decide every `pass/` row. `A` = the literal value reaches the
type of the name. `B` = reachability honours that value, so a guarded branch is
not analyzed.

| State | `A` | `B` | Failing rows |
| --- | --- | --- | --- |
| pyright | annotated `Final` only, same module only | same-module annotated `Final` only | `case2`, `case4`–`case7` |
| pyright+ | `A` extended across modules | unchanged | `case2`, `case4`–`case7` |
| ty | bare `Final` everywhere; annotated `Final` same module only | both spellings, same module and across modules | `case5`, `case7`, `case12`, `case13` |
| ty+ | `A` extended across modules | unchanged | none |
| mypy | only a literal initializer on an annotated `Final` | inline checks only (syntax driven) | `case2`–`case9`, `case11` |
| mypy+ | `A` extended to platform-check initializers and across modules | unchanged | `case2`–`case9`, `case11` |

Notes on the individual gaps:

- **pyright** skips a bare `Final` in the reachability analysis: the reference's
  symbol has no typed declaration, so `hasTypedDeclarations()` in
  `codeFlowEngine.ts` short-circuits the check. Cross-module pruning does not
  happen for any form, including a plain imported `Literal[False]` constant,
  because reachability is decided per file and an imported name has no flow node
  in the reading file. That is why `case2`, `case4`–`case7` fail in both states.
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

## Reading the table

- A `pass/` row that a checker fails is a place where the checker analyzes code
  that cannot run on the target platform, or reports a wider type than the value
  allows.
- Rows are paired by annotation (`case2`/`case3`, `case4`/`case5`,
  `case6`/`case7`, `case11`/`case12`) and by access form (`case4`/`case6`,
  `case5`/`case7`, `case12`/`case13`), so a single `✗` isolates one variable.
- `case1` is the anchor mandated by the typing spec ("Version and platform
  checking"). Everything else is beyond the spec; see `README.md`.
