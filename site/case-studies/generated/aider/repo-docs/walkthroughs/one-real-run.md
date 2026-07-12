# One Real Run: A Terminal Request Becomes An Edit

This walkthrough follows the default CLI edit path: a developer starts `aider`, sends a message, receives a diff-style SEARCH/REPLACE reply, and Aider applies the edit while preserving user control over files and git state.

The pressure in this path is that model output is useful but not trusted: it must be parsed, scoped to approved files, checked against dirty work, and reflected back when it fails.

The example behavior is represented in tests by stubbing the model response instead of calling a provider. That keeps the walkthrough focused on the repository’s own responsibilities: session setup, edit parsing, file permissions, dirty-work protection, reflection, and commit hooks.

## Step 1: The terminal command becomes a configured session

The observable starting point is the `aider` command. Package metadata maps that command to `aider.main:main`, and `aider/__main__.py` calls the same entrypoint when the package is run as a module.

Inside `main()`, Aider first discovers git context and configuration. It builds a config search order, parses arguments once to find environment/config inputs, loads dotenv files, then parses again with the updated environment. This matters because later edit behavior depends on options such as `--auto-commits`, `--dirty-commits`, `--dry-run`, `--lint-cmd`, and `--test-cmd`.

The source anchor is [`main()` setting git/config/parser state](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/main.py#L451). The config behavior is tested in [`test_main_with_git_config_yml`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_main.py#L88), which writes `.aider.conf.yml` and asserts that `auto_commits` reaches `Coder.create()`.

## Step 2: Startup hands the edit loop its operating policy

Before a user message is sent, `main()` assembles the session objects that the edit loop will need: command handlers, chat summarization, repo state, file lists, stream and repo-map settings, lint/test commands, commit behavior, and language preferences. It passes those into `Coder.create()`.

That handoff is the boundary between CLI policy and coding behavior. The CLI decides what the session should allow; the concrete coder decides how model output becomes file changes.

The source anchor is [`main()` calling `Coder.create()` with session policy](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/main.py#L972). The concrete class is chosen by [`Coder.create()` matching `edit_format` against registered coder classes](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L124). For the path followed here, [`EditBlockCoder`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L15) provides the `"diff"` edit format.

## Step 3: The user message is sent, but the reply is still just text

When a message arrives, `send_message()` adds the user content to the current conversation, formats all chat chunks into provider messages, checks token limits, warms prompt cache when configured, and sends the messages. The send loop handles retryable provider errors with backoff, context-window exhaustion, output-limit continuation for models that support assistant prefill, keyboard interruption, and generic exceptions.

Only after the send loop finishes does the reply become candidate edit content. `send_message()` captures the accumulated assistant output in `partial_response_content`, strips reasoning content, records usage, and adds the assistant reply to the conversation. At this point no file has been changed yet.

The source anchor is [`send_message()` formatting, sending, and capturing the response](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L1419). The provider call itself is deliberately replaceable in tests: [`test_full_edit`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_editblock.py#L373) stubs `coder.send` so the rest of the local edit path can be verified.

## Step 4: The reply is parsed into edits before files are touched

For the diff-style path, the concrete coder parses model output as SEARCH/REPLACE blocks. `EditBlockCoder.get_edits()` reads `partial_response_content`, calls the block parser, separates shell-command blocks from file edits, and returns structured edit tuples.

`apply_updates()` then performs a dry-run edit pass before asking file-permission questions or writing. This is the critical safety shape: Aider first proves that the reply can be interpreted as edits, then checks whether each path is allowed, then writes.

The source anchors are [`EditBlockCoder.get_edits()`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L21), [`EditBlockCoder.apply_edits()`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L41), and [`apply_updates()` ordering dry-run, prepare, then write](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2296). [`test_full_edit`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_editblock.py#L373) verifies the successful case by changing `one\ntwo\nthree\n` into `one\nnew\nthree\n`.

## Step 5: File access is narrowed before writing

Before final writes, `prepare_to_edit()` asks whether each target path is allowed. Files already in the chat can be edited directly. Gitignored files are skipped. Missing files require a create-file confirmation. Existing files outside the chat require a separate confirmation before Aider adds them to the editable set.

This is why the edit loop is not a blind patch applier. The model can propose paths, but `allowed_to_edit()` decides whether those paths are inside the current session’s authority.

The source anchor is [`allowed_to_edit()` checking in-chat, gitignore, new-file, and out-of-chat cases](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2191). The new-file path is exercised by [`test_new_file_edit_one_commit`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_coder.py#L570), where a stubbed model reply creates `file.txt`.

## Step 6: Dirty work is protected before the model edit lands

When a target file is already dirty and dirty commits are enabled, Aider marks it for a pre-edit commit. After all edit permissions are checked, `prepare_to_edit()` calls `dirty_commit()` before final writes. That creates a git checkpoint for the user’s pre-existing work, then the model edit can be committed separately.

This separation is the hard part of the path. The system must distinguish user dirt from Aider dirt so undo and commit history remain meaningful.

The source anchors are [`check_for_dirty_commit()` marking dirty files](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2175), [`prepare_to_edit()` calling `dirty_commit()`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2269), and [`dirty_commit()` committing marked paths](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2411). [`test_gpt_edit_to_dirty_file`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_coder.py#L667) verifies the result: the dirty state is committed before the Aider edit, and the final file content becomes `three\n`.

## Step 7: The edit is written, then commit/lint/test feedback can run

After final writes, `apply_updates()` reports each edited file. Back in `send_message()`, Aider records edited files, optionally auto-commits them, moves the commit summary back into chat history, runs lint for edited files, reflects lint errors when the user agrees, runs shell commands requested by the model, and can run a configured test command.

The source anchor is [`send_message()` handling auto-commit, lint, shell output, and tests after edits](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L1585). [`test_only_commit_gpt_edited_file`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_coder.py#L612) verifies a key boundary: an unrelated dirty file is left dirty and is not included in the Aider edit commit diff.

## Step 8: Failed edits become reflected feedback

If a SEARCH block does not match the file, `EditBlockCoder.apply_edits()` builds a `SearchReplaceNoExactMatch` explanation with the failed block and nearby candidate lines when available, then raises `ValueError`. `apply_updates()` catches that error, increments the malformed-response count, prints the edit-format help URL, and stores the error text in `reflected_message`.

The effect is that a failed edit is not silently treated as success. It becomes feedback that the conversation can use to ask the model for a corrected edit.

The source anchors are [`EditBlockCoder.apply_edits()` constructing the no-match message](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/editblock_coder.py#L82) and [`apply_updates()` reflecting malformed edits](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/base_coder.py#L2305). A falsifying check for this walkthrough is the dry-run test: [`test_full_edit_dry_run`](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/tests/basic/test_editblock.py#L398) must keep the original file content unchanged.

## Verification

The local mechanics are verified by the focused tests named in [the source evidence ledger](../references/source-evidence.md#verification-commands). In the current environment, those tests require project dependencies such as `oslex`; if dependency installation has not been run, collection fails before the tests execute.

Use [the CLI edit code map](../code-map.md) to locate the source areas and focused tests behind these steps.

For the next concept-level explanation, read [why the edit lifecycle treats model output as a proposal](../modules/edit-lifecycle.md).

Evidence status: Confirmed unless noted.
