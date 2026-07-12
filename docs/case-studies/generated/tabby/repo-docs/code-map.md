# Tabby Completion Code Map

This map covers the first-party Rust source areas that own the documented `tabby serve` completion path. Read [how one completion request becomes text](walkthroughs/one-real-run.md) first if the behavior is not clear yet.

| Path | Responsibility | Key code | Connection to the main path |
| --- | --- | --- | --- |
| `crates/tabby/src/` | Starts the server, merges CLI/config state, creates completion services, and installs the HTTP route. | `main.rs`, `serve.rs` | Owns startup and route availability. |
| `crates/tabby/src/routes/` | Adapts HTTP request context to the completion service and maps service failures to responses. | `completions.rs` | Owns the `/v1/completions` boundary. |
| `crates/tabby/src/services/` | Defines completion request/response contracts and runs generation. | `completion.rs` | Owns prompt-source choice, inference, output normalization, and event logging. |
| `crates/tabby/src/services/completion/` | Collects optional context and rewrites editor segments into model prompt form. | `completion_prompt.rs` | Enriches the request before inference without making retrieval mandatory. |
| `crates/tabby/tests/` | Exercises the server as a real completion endpoint. | `goldentests.rs` | Verifies the end-to-end response shape. |
| `crates/tabby-common/src/` | Defines shared server configuration used by the completion route. | `config.rs` | Supplies timeout and related defaults. |

## `crates/tabby/src/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `crates/tabby/src/main.rs` | Dispatches the `Serve` command and converts CLI model input into local model config. | `Serve`, `to_local_config()` | `tabby serve`. |
| `crates/tabby/src/serve.rs` | Merges arguments, builds services, and installs `/v1/completions` or its `501` fallback. | `serve::main`, `api_router`, `merge_args()` | Server startup; verify route assembly with the walkthrough's unit and golden tests. |

## `crates/tabby/src/routes/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `crates/tabby/src/routes/completions.rs` | Adds user and user-agent context, calls generation, returns JSON, and maps service errors to `400`. | completion route handler | Axum `/v1/completions` route. |

## `crates/tabby/src/services/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `crates/tabby/src/services/completion.rs` | Defines request/response shapes, chooses raw-prompt or segment flow, normalizes CRLF, calls inference, logs the event, and builds the response. | `CompletionRequest`, `CompletionService::generate`, `CompletionResponse` | HTTP completion route; contains focused unit tests. |

## `crates/tabby/src/services/completion/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `completion_prompt.rs` | Prioritizes editor snippets, optionally searches indexed code, tolerates retrieval failures, and applies the model prompt template. | `PromptBuilder::collect`, `collect_snippets`, `build_prompt` | `CompletionService::generate`; contains retrieval and template tests. |

## `crates/tabby/tests/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `crates/tabby/tests/goldentests.rs` | Starts a local model server, posts completion JSON, and snapshots the normalized response. | `run_golden_tests_cpu` | Heavy end-to-end verification. |

## `crates/tabby-common/src/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `crates/tabby-common/src/config.rs` | Holds the shared server defaults consumed during route construction. | `ServerConfig`, `completion_timeout` | `serve.rs`; exact knobs are listed in the completion contract module. |

## Coverage

Covered: the open-source `crates/tabby` completion server, prompt construction, retrieval fallback, shared timeout config, and completion unit/golden tests. Chat completions, enterprise webserver/UI behavior, code-index construction, model downloader internals, IDE clients, deployment tooling, website assets, Python evaluation tools, and HTTP adapter internals are excluded or deferred.

Read [the completion pipeline model](modules/completion-pipeline.md), [how retrieval enters the prompt](modules/retrieval-context.md), or [the exact completion contract](modules/completion-contract.md) for mechanism detail.

Evidence status: Confirmed unless noted.
