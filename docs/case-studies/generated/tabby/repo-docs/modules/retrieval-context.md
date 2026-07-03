# Retrieval Context

## What retrieval context adds

Retrieval context is extra code placed before the user's current editor prefix so the model can see nearby or related symbols. It is optional by design. A completion should still run when the request has no snippets, the embedding service is disabled, a repository is not allowed, or indexed search is not ready.

There are two sources. The editor can send declarations and recently relevant snippets directly in `segments`. The server can also search indexed code when embedding-backed code search is available and the request's `git_url` matches an allowed repository.

## How snippets are chosen and guarded

The snippet collector uses a fixed order and a small prompt budget. It first takes editor-provided declarations, then snippets from changed files, then snippets from recently opened files. Only after those does it try indexed search, and only if enough character budget remains.

Indexed search is guarded by three checks:

| Check | Why it matters |
| --- | --- |
| Code search service exists | Embedding search is only created when embedding is enabled during serve startup. |
| Request has `segments.git_url` | The search needs a repository identity. |
| `AllowedCodeRepository` has a closest match | The route/server must permit that repository before search uses it. |

The prompt builder then prepends snippets as line comments when the language has a comment marker. The tests show Python snippets becoming `# Path: ...` blocks before the original prefix. If the language lacks a line-comment marker, snippet rewriting is skipped rather than forcing an unsafe syntax.

Representative case:

| Input condition | Resulting prompt state |
| --- | --- |
| Python request with collected snippet `res_1 = invoke_function_1(n)` from `a1.py` | The snippet is prepended as `# Path: a1.py` and `# res_1 = invoke_function_1(n)` before the user's prefix. |
| Language has no supported line-comment marker | The original prefix remains usable because snippet comment rewriting is skipped. |

```text
# Path: a1.py
# res_1 = invoke_function_1(n)
def this_is_prefix():
```

Source: [`PromptBuilder::collect`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L40-L86), [`extract_snippets_from_segments`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L145-L204), [`collect_snippets`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L206-L264), and [`test_build_prefix_readable`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L461-L505).

## Where to follow the path

Return to [Step 4 of the walkthrough](../walkthroughs/one-real-run.md#step-4-optional-context-is-gathered-before-the-prompt-is-built) for the runtime path. Use [the source evidence ledger](../references/source-evidence.md) to audit the fallback claims and [the completion contract module](../modules/completion-contract.md) to find exact request fields.

Evidence status: Confirmed unless noted.
