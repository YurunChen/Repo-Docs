# Aider CLI Edit Code Map

This map covers the first-party source areas that own the documented CLI edit workflow. Read [how one terminal request becomes an edit](walkthroughs/one-real-run.md) first if the runtime behavior is not clear yet.

| Path | Responsibility | Key code | Connection to the main path |
| --- | --- | --- | --- |
| `aider/` | Turns terminal, config, model, file, and git state into one configured coding session. | [`main.py`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/main.py#L451) | Owns startup and the policy passed into the coder. |
| `aider/coders/` | Runs the model turn and constrains model text into permitted, checkable file edits. | [`base_coder.py`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L124), [`editblock_coder.py`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py) | Owns the request-to-edit lifecycle after session assembly. |
| `tests/basic/` | Verifies edit parsing, dry runs, dirty-file protection, and commit scope. | [`test_editblock.py`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_editblock.py), [`test_coder.py`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_coder.py) | Proves the main local mechanics without requiring a live provider. |

## `aider/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `aider/main.py` | Resolves git/config context and assembles the objects and options for a coding session. | `main()`, `Coder.create()` call site | Console entrypoint and `python -m aider`; followed by the session-assembly module. |

## `aider/coders/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `aider/coders/base_coder.py` | Selects coder implementations, runs model turns, gates edits, protects dirty work, reflects failures, and commits accepted changes. | `Coder.create()`, `apply_updates()`, `allowed_to_edit()` | The configured session; verified by `tests/basic/test_coder.py`. |
| `aider/coders/editblock_coder.py` | Parses diff-style SEARCH/REPLACE blocks and reports non-matching edits. | `EditBlockCoder`, `get_edits()` | The default diff path documented by the walkthrough; verified by `tests/basic/test_editblock.py`. |

## `tests/basic/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `tests/basic/test_editblock.py` | Checks parsing, full edits, and dry-run behavior. | `test_full_edit`, `test_full_edit_dry_run` | First verification point for edit-format changes. |
| `tests/basic/test_coder.py` | Checks dirty-file baselines and edited-file-only commits. | `test_gpt_edit_to_dirty_file`, `test_only_commit_gpt_edited_file` | First verification point for persistence and commit-scope changes. |

## Coverage

Covered: CLI session assembly, the diff-style coder lifecycle, and the focused tests that prove edit and commit boundaries. GUI launch, watch and copy/paste modes, browser and voice input, repo-map ranking, model metadata registration, OAuth onboarding, and architect/editor splits are excluded because this guide does not trace those workflows.

Read [how session policy is assembled](modules/session-assembly.md) or [why model output is gated before writes](modules/edit-lifecycle.md) for mechanism detail.

Evidence status: Confirmed unless noted.
