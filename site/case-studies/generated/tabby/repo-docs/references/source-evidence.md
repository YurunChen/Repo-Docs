# Source Evidence

This evidence ledger records the source inspection behind the scoped completion guide. Read the walkthrough first if you do not yet understand the behavior.

## Understanding Brief

| Field | Current answer |
| --- | --- |
| Scenario | A client posts a code-completion request to `/v1/completions` after `tabby serve --model TabbyML/StarCoder-1B --no-webserver --port 9090` starts a local server. |
| Input | JSON with `language` and `segments.prefix`, optionally `segments.suffix`, matching the request example in the troubleshooting docs and golden tests. |
| Success / output | `CompletionResponse` contains `id`, one `choices[0].text`, optional `debug_data`, and `mode`. Golden tests normalize the id and snapshot the response. |
| Hard part | The server has to assemble a model prompt from config, editor segments, optional context snippets, line-ending normalization, and model options. Context retrieval must be useful without being required for success. |
| Boundary / failure | Missing raw prompt and missing segments returns `CompletionError::EmptyPrompt`, which the route maps to `400`. Retrieval search failures return no indexed snippets and allow completion to continue. |
| Falsifying check | If `CompletionService::generate` stopped accepting segment-based requests, stopped mapping empty input to `EmptyPrompt`, or `PromptBuilder::collect` began propagating `CodeSearchError::NotReady`, this guide's model would be wrong. |
| Next reader question | How are repositories indexed before code search can return snippets? Deferred: this first guide names that dependency but does not trace the indexing pipeline. |

## Evidence Traversal Log

| Pass | Purpose | Inspected evidence | What changed in the model |
| --- | --- | --- | --- |
| Pass 1 | Map the main path | `README.md`, root `Cargo.toml`, `crates/tabby/src/main.rs`, `crates/tabby/src/serve.rs`, `crates/tabby/src/routes/completions.rs`, `crates/tabby/src/services/completion.rs` | Chose the scoped behavior: `tabby serve` exposes `/v1/completions`, and `CompletionService::generate` owns prompt construction and response creation. |
| Pass 2 | Challenge and fill | `completion_prompt.rs`, `config.rs`, `goldentests.rs`, troubleshooting docs, `http-api-bindings` completion adapters, unit tests for prompt templates, CRLF, and retrieval fallback | Added the hard part: context collection is optional and guarded; missing prompt data maps to `400`; line endings are normalized around inference; exact config defaults belong in references. |

## Coverage And Exclusions

Confirmed coverage: `crates/tabby` CLI/server setup, `/v1/completions` route, `CompletionRequest`/`CompletionResponse`, prompt construction, snippet collection, CRLF handling, config defaults, and completion unit/golden tests.

Adjacent paths inspected but not traced: chat completions, enterprise webserver attachment, HTTP model adapters, embedding service creation, and troubleshooting docs. These confirm route shape or dependencies but are not the main reader path.

Out of scope: enterprise UI and webserver behavior, code-index construction, model downloader internals, IDE-client request generation, deployment scripts, website build, and Python evaluation tooling.

## Claim Ledger

| Claim | Evidence | Confidence | Caveat | Used by |
| --- | --- | --- | --- | --- |
| Tabby is a self-hosted AI coding assistant with an OpenAPI-compatible server surface. | [`README.md`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/README.md) and [`serve.rs` OpenAPI paths](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L40-L80). | Confirmed | README marketing language is context; route claims use source. | `README.md` |
| The scoped run starts with `Serve` and dispatches into `serve::main`. | [`main.rs`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/main.rs#L53-L73). | Confirmed | `download` subcommand is not traced. | Walkthrough Step 1, code map |
| CLI `--model` can override configured completion model and create local model config. | [`ServeArgs`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L83-L115), [`merge_args`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L397-L418), [`to_local_config`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/main.rs#L93-L107). | Confirmed | Config-file model shapes are only summarized. | Walkthrough Step 1, contract module |
| `/v1/completions` is installed only when a completion service exists; otherwise it returns `501`. | [`api_router`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L289-L310). | Confirmed | EE webserver layers may attach additional policy outside this scoped path. | Walkthrough Step 1, code map |
| Completion requests are wrapped in a configurable timeout defaulting to 30 seconds. | [`api_router` timeout layer](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L289-L297), [`ServerConfig`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby-common/src/config.rs#L233-L245). | Confirmed | Timeout behavior itself was source-inspected, not runtime-tested here. | Walkthrough Step 1, code map, contract module |
| The route enriches the request with user/user-agent context and maps service errors to `400`. | [`crates/tabby/src/routes/completions.rs`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/routes/completions.rs#L26-L48). | Confirmed | Authentication mechanics are outside scope. | Walkthrough Step 2, code map |
| A standard completion needs either `debug_options.raw_prompt` or `segments`. | [`raw_prompt`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L90-L95), [`generate`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L382-L405). | Confirmed | `next_edit_suggestion` has its own `edit_history` requirement. | Walkthrough Step 3, module |
| Segment-based requests can collect snippets unless retrieval augmentation is disabled. | [`build_snippets`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L315-L329). | Confirmed | Snippet content may be empty depending on request and index state. | Walkthrough Step 4, code map, retrieval module |
| Editor-provided snippets are prioritized before indexed-code search. | [`extract_snippets_from_segments`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L145-L204), [`PromptBuilder::collect`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L40-L86). | Confirmed | The 768-character budget is implementation detail, not a public API guarantee. | Retrieval module |
| Indexed search is skipped when code search, `git_url`, or allowed repository match is absent. | [`PromptBuilder::collect`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L61-L71). | Confirmed | How allowed repositories are configured is not traced. | Retrieval module |
| Code-search `NotReady` and other search errors do not fail completion. | [`collect_snippets`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L224-L245), [`test_collect_snippets`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L313-L336). | Confirmed | Non-`NotReady` errors are logged and also return collected snippets. | Walkthrough Step 4 |
| Snippets are prepended as comments when the language has a line-comment marker. | [`build_prefix`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L109-L143), [`test_build_prefix_readable`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L461-L505). | Confirmed | Unknown/no-comment languages keep the original prefix. | Walkthrough Step 5 |
| CRLF input is normalized before inference and restored in generated output. | [`contains_crlf`, `override_prompt`, `override_generated_text`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L503-L536), [unit tests](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L658-L752). | Confirmed | The regex preserves existing `\r\n`; tests cover representative cases. | Walkthrough Step 3 and 6 |
| The service logs `Event::Completion` and returns a one-choice response. | [`generate`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L407-L438), [`CompletionResponse`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L242-L280). | Confirmed | Event storage backend is outside this guide. | Walkthrough Step 6 |
| Golden tests start a real server and post completion JSON to `/v1/completions`. | [`goldentests.rs`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/tests/goldentests.rs#L34-L159). | Confirmed | The CPU golden test is heavier than unit tests because it starts a model server. | Walkthrough verification, code map |

## Commands Inspected Or Used

```bash
rg --files
rg -n "CompletionRequest|/v1/completions|completion_timeout|disable_retrieval|EmptyPrompt|contains_crlf|override_generated_text|next_edit_suggestion" crates/tabby crates/http-api-bindings crates/tabby-common website/docs -g '*.rs' -g '*.md' -g '*.mdx'
git rev-parse --short HEAD
```

Evidence status: Confirmed unless noted.
