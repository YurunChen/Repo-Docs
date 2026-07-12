# Tabby Repo Guide

Tabby is a self-hosted AI coding assistant. This guide starts with the local server path that IDE extensions rely on: a client sends a code-completion request, the server builds a model prompt from editor state and optional code context, then returns a completion response.

The current guide is scoped to the open-source `crates/tabby` completion request path. It does not try to explain the whole monorepo. After the walkthrough, you should be able to follow how `tabby serve --model ...` exposes `/v1/completions`, where request fields become prompt material, which fallbacks keep completion working when context is unavailable, and which tests verify the core behavior.

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand one real run | [Follow a completion request through the server](walkthroughs/one-real-run.md) | The observable request, service handoffs, prompt construction, model call, response, and boundary cases. |
| Locate the implementation | [Use the completion code map](code-map.md) | Directory responsibilities, important files and symbols, tests, and scoped exclusions. |
| Understand the main concept | [Read the completion pipeline model](modules/completion-pipeline.md) | A plain model for where routing ends, where prompt work begins, and where inference is called. |
| Understand code-context enrichment | [Read how retrieval context enters the prompt](modules/retrieval-context.md) | The rules for editor-provided snippets, indexed-code snippets, repository allow checks, and graceful fallback. |
| Look up exact fields and knobs | [Use the completion contract module](modules/completion-contract.md) | Request fields, response shape, timeout/defaults, and verification commands. |
| Audit the claims | [Inspect the evidence ledger](references/source-evidence.md) | Source links, tests, command evidence, caveats, and the traversal passes used to build the guide. |
| Check guide quality and scope | [Read the quality review](references/quality-review.md) | What the guide proves, what remains out of scope, and what would falsify the model. |

## Scope Note

Confirmed: this first guide covers the Rust server completion endpoint under `crates/tabby`, the shared config fields it depends on, and tests that exercise prompt construction and line-ending behavior.

Out of scope for this first build: the enterprise webserver attachment, chat completions, UI packages, IDE-client internals, model downloader details, code-index construction, deployment guides, and generated web assets. Those areas are adjacent, but they are separate reader paths.

Evidence status: Confirmed unless noted.
