# One Real Run: A Completion Request Becomes Text

This walkthrough follows the request shape shown in Tabby's troubleshooting docs: a client posts Python editor segments to `/v1/completions`, with a prefix before the cursor and an optional suffix after it. The hard part is that the server cannot pass those fields straight to the model. It may need to merge CLI config, attach a route only when a completion model exists, preserve the user's line-ending style, add relevant code context when available, and still return a useful response when retrieval context is missing or not ready.

The success state is a JSON response with an id, one choice, and optional debug data. The source path for this run starts in the `tabby` CLI, crosses the Axum route, enters `CompletionService::generate`, builds a prompt, calls the loaded code-generation engine, logs the completion event, and returns `CompletionResponse`.

## Step 1: The server is started with a completion model

The run starts when a user chooses the `serve` subcommand. At startup, Tabby loads config, prepares the Tabby data root, and dispatches to the server code. The server then merges CLI arguments into the loaded config so a command-line `--model` can create or override the configured completion model.

The route is only useful if that completion model exists. `serve::main` downloads local models when needed, creates embedding-backed code search only when `TABBY_EMBEDDING_ENABLED=yes`, then calls `create_completion_service_and_chat` to obtain the completion service. The completion route is installed when that service exists; otherwise `/v1/completions` is registered as `501 Not Implemented`. The route is also wrapped in `server.completion_timeout`, which defaults to 30 seconds.

Source: [`main.rs` dispatches `Serve`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/main.rs#L53-L73), [`serve.rs` builds services and routes](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L117-L232), and [`api_router` installs `/v1/completions`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/serve.rs#L289-L310). Exact knobs are listed in [the completion contract module](../modules/completion-contract.md).

## Step 2: The HTTP route adds request context

The route receives JSON as a `CompletionRequest`. Before the service sees it, the route can copy an authenticated user from the typed header into the request and capture the `User-Agent`. It also receives an `AllowedCodeRepository`, which is important later when retrieval wants to use a `git_url` from the request.

The route keeps error reporting simple: successful service output becomes a JSON response; service errors are logged and mapped to `400 Bad Request`. This makes missing prompt material visible at the HTTP boundary without exposing internal error variants.

Source: [`crates/tabby/src/routes/completions.rs`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/routes/completions.rs#L26-L48).

## Step 3: The service chooses the prompt source

At this point the server has a request, but it still has to decide what text the model should see. Standard completions take one of two paths. If `debug_options.raw_prompt` is present, the raw prompt goes directly to inference and `segments` are ignored. Otherwise, the service requires `segments`; without raw prompt or segments it returns `CompletionError::EmptyPrompt`, which the route maps to `400 Bad Request`.

For segment-based requests, the service records the language, builds generation options from request values and config defaults, and checks whether the editor text uses CRLF line endings. If it sees CRLF in the prefix or suffix, it normalizes the prompt to LF before inference and later converts model output back to CRLF where needed. The unit tests cover both detection and conversion.

Source: [`CompletionRequest` fields](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L41-L65), [`CompletionService::generate`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L358-L439), and [CRLF tests](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L658-L752).

## Step 4: Optional context is gathered before the prompt is built

The request may contain snippets from the editor, or it may identify a repository where Tabby can search indexed code. This phase is careful because context is useful but should not be allowed to break completions. If the request disables retrieval augmentation, snippet collection returns empty immediately. Editor-provided declarations have priority, then snippets from changed files, then recently opened files. Indexed-code search is tried only if there is enough remaining character budget, a code-search service exists, the request has `git_url`, and the repository is allowed.

When code search is unavailable, not ready, or fails to parse/search, the builder logs or ignores the retrieval problem and returns the snippets it already has. That is the main boundary in this path: the model request continues even when retrieval context cannot be added.

Source: [`build_snippets` handles the disable flag](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L315-L329), [`PromptBuilder::collect` gates indexed retrieval](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L40-L86), [`collect_snippets` falls back on search errors](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L206-L264), and [retrieval tests cover `NotReady`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L313-L336). For the concept model, read [how retrieval context enters the prompt](../modules/retrieval-context.md).

## Step 5: The prompt is rewritten into model form

The prompt builder first rewrites editor segments if snippets exist. For languages with a known line-comment marker, snippets are prepended as commented lines with `Path: ...` labels so the model can see related code without turning it into executable code. If the language has no line-comment marker, the original prefix is left unchanged.

The builder then applies the model prompt template if one exists. For fill-in-the-middle models, this is where prefix and suffix are arranged into the model's expected form. If there is no template, the builder uses the prefix alone. An absent or empty suffix is normalized to a newline before templating.

Source: [`rewrite_with_snippets` and `build_prefix`](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L100-L143), [`build_prompt` and default suffix behavior](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L32-L38), and [prompt-template tests](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion/completion_prompt.rs#L338-L459). The broader handoff is explained in [the completion pipeline model](../modules/completion-pipeline.md).

## Step 6: The model output is returned and logged

Once the prompt and generation options are ready, the service calls the loaded code-generation engine. It then restores CRLF style when the input used CRLF, logs the completion event with request context and generated choice, and builds a response whose single choice contains the generated text. Debug data is included only when the request asked for returned snippets or prompt.

The CPU golden test verifies the end-to-end server shape by starting `tabby serve --model TabbyML/StarCoder-1B --no-webserver --port 9090`, waiting for `/v1/health`, posting completion requests to `/v1/completions`, and snapshotting the response with the generated id normalized.

Source: [`CompletionService::generate` calls the engine, logs, and returns](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L407-L438), [`CompletionResponse` shape](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/src/services/completion.rs#L242-L280), and [the golden test run](https://github.com/TabbyML/tabby/blob/e8608d6d8f4016b9836a72037f72630d7e993468/crates/tabby/tests/goldentests.rs#L34-L159).

## Verification

Fast unit checks for this guide's core behavior:

```bash
cargo test -p tabby services::completion::tests::test_completion_service
cargo test -p tabby services::completion::tests::test_contains_crlf
cargo test -p tabby services::completion::tests::test_override_prompt
cargo test -p tabby services::completion::tests::test_override_generated
cargo test -p tabby services::completion::completion_prompt::tests::test_collect_snippets
cargo test -p tabby services::completion::completion_prompt::tests::test_prompt_template
```

The heavier end-to-end check is `cargo test -p tabby run_golden_tests_cpu`. It starts a local model server and may download or load a model, so it is slower than the unit checks.

Use [the completion code map](../code-map.md) to locate startup, routing, service, prompt, shared-config, and golden-test source areas behind these steps.

Evidence status: Confirmed unless noted.
