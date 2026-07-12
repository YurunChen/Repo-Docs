# Aider Repository Guide

Aider is a terminal pair-programming tool. The core behavior to understand first is not the model call by itself; it is the control loop that turns a user request into a constrained file edit while preserving enough state for review, lint/test feedback, and undoable git history.

This guide is scoped to the CLI edit workflow in the current source tree. It does not attempt to document every mode in the repository. GUI launch, watch mode, browser scraping, voice input, model metadata registration, and repo-map ranking internals are adjacent paths recorded in [the evidence coverage notes](references/source-evidence.md#coverage-notes).

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- |
| Build a mental model quickly | [How one terminal request becomes an edit](walkthroughs/one-real-run.md) | The main behavior trace from startup through model reply, file write, reflection, and commit hooks. |
| Locate the implementation | [Use the CLI edit code map](code-map.md) | Directory responsibilities, important files and symbols, related tests, and scoped exclusions. |
| Understand why startup passes so many objects into the edit loop | [How a session is assembled before the first model call](modules/session-assembly.md) | The CLI boundary where config, git, files, commands, and model settings become session policy. |
| Understand why Aider does not blindly write model output | [How edits are parsed, checked, written, and reflected](modules/edit-lifecycle.md) | The gates that stand between a model reply and disk writes. |
| Audit claims and caveats | [The source evidence ledger](references/source-evidence.md) | Source, tests, confidence, caveats, coverage notes, and verification commands. |
| Check guide quality and residual risk | [The reader-simulation review](references/quality-review.md) | A short audit of whether the guide transfers the scoped model. |

## The Model To Keep

Aider separates the coding session into two responsibilities.

First, startup turns terminal state into a configured session: command-line arguments, config files, environment variables, git state, model settings, tracked files, lint/test preferences, and command helpers are resolved before a `Coder` is created. That keeps policy decisions near the CLI boundary instead of hiding them inside the model-response parser.

Second, the `Coder` owns the edit lifecycle. It formats chat context, sends the user request to the selected model, captures the reply, parses the reply into an edit format, asks whether files may be created or broadened into the chat, protects dirty work, writes files, reflects malformed edits or lint/test failures, and optionally commits the result.

The important design pressure is control. Aider expects model output to be useful but not inherently safe. The edit loop narrows what the model can change, checks whether the output matches the requested format, and turns failed checks into feedback that can be sent back through the same conversation.

## Reproduce The Main Behavior

The full behavior depends on an LLM provider, but the repository tests isolate the important local mechanics by stubbing the model response. The most direct checks are:

```bash
python -m pytest tests/basic/test_editblock.py::TestEditBlockCoder::test_full_edit tests/basic/test_editblock.py::TestEditBlockCoder::test_full_edit_dry_run
python -m pytest tests/basic/test_coder.py::TestCoder::test_gpt_edit_to_dirty_file tests/basic/test_coder.py::TestCoder::test_only_commit_gpt_edited_file
```

Those tests prove that a diff-style model reply can edit file content, dry-run avoids writing, dirty work is committed before an Aider edit when needed, and unrelated dirty files are left out of the Aider edit commit.

Evidence status: Confirmed unless noted.
