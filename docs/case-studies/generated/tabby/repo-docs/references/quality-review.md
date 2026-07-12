# Quality Review

This is an audit note. It checks whether the guide transfers a usable reader model and where risk remains.

## Reader Simulation

| Reader question | Answer from the guide |
| --- | --- |
| What real path is followed? | A `tabby serve` server handles a POST to `/v1/completions` and returns completion JSON. |
| What is hard or non-trivial? | The server must turn editor state into a model prompt while optional retrieval context, line-ending style, route availability, and debug switches can change the path. |
| What changes at each phase? | CLI/config creates the service, the router adds request context, the service chooses raw prompt or segments, optional snippets enter the prefix, the prompt is templated, the model output is logged and returned. |
| Where would I change this behavior? | [`code-map.md`](../code-map.md) routes startup to `crates/tabby/src/`, HTTP adaptation to `routes/`, completion logic to `services/`, prompt enrichment to `services/completion/`, and verification to `crates/tabby/tests/`. |
| Where do assumptions stop? | Missing prompt material returns `400`; no completion model returns `501`; retrieval errors return no snippets and allow completion to continue. |
| What would prove this explanation wrong? | Changes in `CompletionService::generate`, `PromptBuilder::collect`, route status mapping, or completion config defaults that contradict the documented flow. |
| What would a careful newcomer ask next? | How repositories are indexed before retrieval can work. The guide defers that path and labels it out of scope. |
| How can I verify it? | Run the listed unit tests for prompt construction, CRLF, and retrieval fallback; use `run_golden_tests_cpu` for a heavier end-to-end server check. |

## Review Table

| Review question | Result | Evidence | Follow-up |
| --- | --- | --- | --- |
| Can a reader state the hard part in one sentence? | Pass | Walkthrough opening names prompt construction, optional context, line endings, and route/model availability. | Keep this pressure visible if the guide later expands to chat or indexing. |
| Can the walkthrough explain the flow without source links? | Pass | Each step starts with behavior before source locators. | Re-check after future syncs. |
| Is there a real boundary path? | Pass | Empty input maps to `400`; missing completion model maps to `501`; retrieval failure falls back to no snippets. | Add runtime output examples if a future sync runs the full server check. |
| Are claims backed by source, tests, config, data, or command evidence? | Pass | `references/source-evidence.md` records Pass 1, Pass 2, claim rows, source links, and commands. | Keep claim rows merged and concise as scope grows. |
| Does the evidence map name adjacent paths checked but not traced? | Pass | Coverage notes exclude chat, EE webserver, indexing internals, clients, deployment, and UI. | Build separate walkthroughs for those paths when requested. |
| What residual risk remains? | Medium | Unit-test verification is cheap; full golden test may require model startup/download and was not assumed as already run in the guide. | Run the exact tests before relying on the guide for release-critical behavior. |

Evidence status: Confirmed unless noted.
