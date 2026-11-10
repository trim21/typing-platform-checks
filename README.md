# Platform-check conformance cases

Self-contained cases for one expectation: **a `Final` name whose initializer is
a statically known platform check keeps that value everywhere it is read, and a
type checker should use it to prune dead branches — in the declaring module and
in modules that import it, for the bare (`Final`) and annotated (`Final[bool]`)
spelling alike.**

Each case is a directory with its own module(s), so it can be run in isolation.
`pass/` cases must produce **zero** errors; each `fail/` case must produce **at
least one** error. Both are checked for `linux` and `windows`, so a checker that
simply reports nothing cannot pass, and a checker that reports everything cannot
pass either.

Nothing here is tied to a specific checker: there are no config files, and the
only requirement is that the checker is told which platform to target.

## Layout

```
platform-check/
  pass/linux/case*/     zero errors expected with a Linux target
  pass/windows/case*/   zero errors expected with a Windows target
  fail/linux/case*/     at least one error expected per case, Linux target
  fail/windows/case*/   at least one error expected per case, Windows target
```

Entry modules are named `c<N>_main.py` and helper modules `c<N>_flags.py` so
that checkers which reject duplicate module basenames (mypy) can analyze a whole
platform directory in one run.

## Cases

Every case uses a Windows-only API (`os.startfile`) on Linux and a POSIX-only
API (`os.getuid`) on Windows, so an unpruned branch is always observable.

### `pass/`

| Case | What must hold |
| --- | --- |
| `case1_inline_check` | anchor: the inline `if sys.platform == "win32":` check is pruned (typing spec, "Version and platform checking") |
| `case2_same_module_bare_final` | bare `Final` declared and used in one file is pruned |
| `case3_same_module_annotated_final` | `Final[bool]` declared and used in one file is pruned |
| `case4_import_bare_final` | `from c4_flags import IS_OTHER` with a bare `Final` is pruned |
| `case5_import_annotated_final` | same, with `Final[bool]` |
| `case6_module_attr_bare_final` | `c6_flags.IS_OTHER` with a bare `Final` is pruned |
| `case7_module_attr_annotated_final` | same, with `Final[bool]` |
| `case8_dead_branch_not_analyzed` | a type error inside a pruned branch is not reported |
| `case9_type_bare_final` | `assert_type(IS_OTHER, Literal[False])` for a same-module bare `Final` |
| `case10_type_annotated_final` | same for a same-module `Final[bool]` |
| `case11_type_import_bare_final` | `assert_type` on a bare `Final` imported from another module |
| `case12_type_import_annotated_final` | `assert_type` on an imported `Final[bool]`: the declared type is `bool`, but the name is `Final`, so the literal value is what a reader observes |
| `case13_type_attr_annotated_final` | same as `case12` through a module attribute instead of a `from` import |

`case2`/`case3`, `case4`/`case5`, `case6`/`case7` and `case11`/`case12` differ
only in the annotation, so a failure in one and not the other isolates the
annotation as the cause.

### `fail/`

| Case | Error that must be reported |
| --- | --- |
| `case1_unguarded_platform_api` | the platform-specific API is called with no guard |
| `case2_mutable_bool_guard` | the guard is a plain `bool` that is rebound from an unknown value, so the branch is live |
| `case3_nonstatic_final_guard` | the guard is a `Final` whose initializer is a function call, so it is not a static condition |
| `case4_wrong_direction_guard` | the guard is negated, so the branch is live on this platform |

## How to run

The target platform must be a concrete value. Anything that disables platform
evaluation (pyright `"All"`, ty `all`) makes every case meaningless: nothing is
pruned and platform-specific APIs become unconditionally available.

The platform is passed on the command line, so no config file is needed. Note
that the accepted spelling differs between checkers — `linux`/`win32`/`darwin`
follow `sys.platform`, while pyright uses `Linux`/`Windows`/`Darwin`.

| Checker | Linux target | Windows target |
| --- | --- | --- |
| pyright | `pyright --pythonplatform Linux <dir>` | `pyright --pythonplatform Windows <dir>` |
| ty | `ty check --python-platform linux <dir>` | `ty check --python-platform win32 <dir>` |
| mypy | `mypy --platform linux <dir>` | `mypy --platform win32 <dir>` |

`<dir>` is one of the four platform directories, e.g. `pass/linux`. Run each
directory separately so a single failing case cannot be masked by another.

Two settings matter beyond the platform:

- **Python version**: `assert_type` needs 3.11 or newer. Pass `--pythonversion
  3.12` (pyright), `--python-version 3.12` (ty), or `--python-version 3.12`
  (mypy) if the checker would otherwise pick an older default.
- **Typeshed / stdlib stubs**: use the checker's own default. The expectations
  assume typeshed, where `os.startfile` is guarded by `sys.platform == "win32"`
  and `os.getuid` is not available on Windows.

## Results

See [`RESULTS.md`](RESULTS.md) for the measured table: pyright, ty and mypy,
each in a baseline and a patched state, across every case in this tree. Nothing
here asserts what a checker should do beyond what `README.md` and the typing
spec state, so re-run and rewrite that file whenever a checker changes.


## Known gaps

- `case2`–`case7` place the `if` at module level. Context matters for some
  checkers: a same-module `Final[bool]` guard inside a function is not pruned by
  ty `0.0.99` even though the module-level form is, so an in-function variant is
  worth adding as separate cases rather than mixing both into one file.
- Only `sys.platform` is exercised. `sys.version_info` and `os.name` are
  statically evaluated by the same mechanism and should be added if a checker is
  found to treat them differently.
- The cases cover `bool` only. Literal propagation for other annotation types
  (`Final[int] = 3`) is a separate concern and is deliberately out of scope.

## Relation to the typing spec

Only `case1` is mandated. The spec says that type checkers are expected to
understand simple version and platform checks, and that uses of a **bare**
`Final` initialized with a literal are treated as the literal. It says nothing
about an annotated `Final[bool]` and nothing about carrying either across a
module boundary, so `case2`–`case13` are expectations beyond the spec — the
point of the tree is to make each checker's position explicit and comparable.
