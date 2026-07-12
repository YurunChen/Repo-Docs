# bolt.diy repo guide

bolt.diy turns a browser chat prompt into code-oriented model output inside a workbench. The important shape is not just "chat calls a model". A user message carries the selected runtime, current project files, feature settings, service state, tool limits, and optional attachments into one server route. The route then decides how much context to send, which model to call, how to keep long answers moving, and how to report failures back to the user.

## Scope

This first guide is scoped to the main web chat request path. It does not yet trace Electron startup, deployment integrations, Git flows, Supabase query flows, or provider-specific implementations beyond the model-selection boundary.

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand one real run | [follow a user prompt into the streaming response](walkthroughs/one-real-run.md) | The main request path from the browser hook to server-sent stream. |
| Locate the implementation | [use the web chat code map](code-map.md) | Directory responsibilities, important files and symbols, and scoped exclusions. |
| Understand why the path is not a pass-through | [see how chat streaming protects context and output](modules/chat-stream.md) | The plain model for summaries, selected files, continuation, and stream errors. |
| Understand provider/model lookup | [see how provider tags become a model instance](modules/provider-model-selection.md) | How selected model/provider text is resolved against registered providers and model lists. |
| Look up exact request fields | [inspect the chat API contract](modules/chat-api-contract.md) | Payload fields, cookies, stream annotations, and verification commands. |
| Audit the guide | [review the source evidence](references/source-evidence.md) | Evidence passes, claims, caveats, and out-of-scope paths. |

## The short model

The browser owns the visible chat action. The Vercel AI SDK React hook posts to the chat route, sends extra message fields, and adds body data such as files, prompt choice, context optimization, chat mode, Supabase state, and max MCP steps. When the user sends text, the client prepends model and provider tags before calling the hook's reload or append path. Those tags are the handoff that lets the server reconstruct the selected model without a separate server-side session.

The server route owns orchestration. It reads the request JSON and provider cookies, starts a data stream, lets MCP process tool invocations, optionally summarizes the chat and selects a small context buffer, then calls the lower-level stream helper with the cleaned messages and runtime options. That helper resolves the provider/model, builds either the coding system prompt or discuss prompt, adds selected file context and locked-file instructions, adjusts token parameters for reasoning models, and calls the AI SDK stream.

The hard part is context pressure. The system has to keep the prompt useful without blindly sending every project file or every old message. That is why the chat route can create a summary, ask a model to select up to five relevant files, attach `chatSummary` and `codeContext` annotations, and slice older messages once a summary is available. If that selection model returns the wrong format or no files, the route surfaces an error instead of silently sending an unbounded context.

## Verification

Use these checks for this scoped guide:

```bash
pnpm run typecheck
pnpm run test
python path/to/repo-docs-skill/scripts/validate_repo_docs.py repo-docs --repo-root .
```

`pnpm run test` currently covers nearby UI/parser utilities, not the `/api/chat` route itself. Treat the chat path in this guide as source-confirmed unless a future route-level test is added.

For the detailed evidence trail and caveats, use [the source evidence ledger](references/source-evidence.md).

Evidence status: Confirmed unless noted.
