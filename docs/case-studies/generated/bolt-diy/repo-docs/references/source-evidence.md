# Source evidence

This page is the evidence base for the first repo-docs build. The guide is scoped to the main web chat request path: a user prompt sent from `Chat.client.tsx` to `/api/chat`, enriched with context, resolved to a provider/model, and returned as a streamed response.

## Evidence Traversal Log

| Pass | Purpose | Inspected evidence | What changed in the model |
| --- | --- | --- | --- |
| Pass 1 | Map the main path | `README.md`, `package.json`, `app/components/chat/Chat.client.tsx`, `app/routes/api.chat.ts`, `app/lib/.server/llm/stream-text.ts` | The representative behavior became "browser chat prompt to streamed model response" rather than a broad app tour. |
| Pass 2 | Challenge boundaries and fill gaps | `select-context.ts`, `create-summary.ts`, `utils.ts`, `constants.ts`, `stream-recovery.ts`, `switchable-stream.ts`, `LLMManager`, provider registry, `api.models.ts`, discovered Vitest files | The hard part was narrowed to context pressure plus provider/model resolution. Real boundaries were invalid context-selector output, empty file selection, missing/incorrect model lookup, token-limit continuation, stream timeout logging, and user-facing error mapping. |

## Understanding brief

| Field | Current answer |
| --- | --- |
| Scenario | A web user sends a chat prompt in build mode and receives a streamed response from `/api/chat`. |
| Input | The client `useChat` body plus tagged message content: `[Model: ...]`, `[Provider: ...]`, and user text. |
| Success / output | A `text/event-stream` response containing progress data, streamed model output, and final usage annotations when the finish reason is not `length`. |
| Hard part | The route must send useful project context without flooding the model, then resolve a provider/model that may be static, dynamic, cached, missing, or provider-specific. |
| Boundary / failure | `selectContext()` throws on missing `<updateContextBuffer>` or zero selected files; `streamText()` throws for no provider models and maps a known wrong Gemini 2.5 name; `/api/chat` maps common provider/API errors into custom stream errors. |
| Falsifying check | Inspect whether `Chat.client.tsx` still sends provider/model tags and whether `selectContext()` still enforces the XML-like response contract. |
| Next reader question | "How do generated `<boltAction>` edits become files in the workbench?" Deferred; this first guide stops at the streamed answer boundary. |

## Coverage and exclusions

Covered in this guide:

- Web chat request body and message tagging.
- Server `/api/chat` orchestration.
- Summary and selected-file context optimization.
- Provider/model resolution boundary.
- Stream continuation, usage annotation, and user-facing error mapping.

Checked but not traced:

- Electron startup and preload paths.
- Deployment routes for Netlify, Vercel, GitHub, GitLab, and Supabase.
- Full workbench artifact parsing and file-write lifecycle after the model emits actions.
- Individual provider implementations beyond registry and model-list lookup.
- MCP server configuration details beyond the chat route passing available tools and `maxLLMSteps`.

## Claim audit table

| Claim | Evidence | Confidence | Caveat | Used by |
| --- | --- | --- | --- | --- |
| The project is an AI coding assistant with a Remix web app and many provider integrations. | [`README.md`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/README.md), [`package.json`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/package.json#L13), provider dependencies in [`package.json`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/package.json#L48) | Confirmed | README includes marketing and roadmap content; current source was used for behavior. | `README.md` |
| The client posts chat requests to `/api/chat` with body fields for keys, files, prompt ID, context optimization, chat mode, Supabase state, design scheme, and MCP steps. | [`Chat.client.tsx`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/components/chat/Chat.client.tsx#L134) | Confirmed | Field values come from hooks/stores not fully traced in this first guide. | `README.md`, walkthrough, code map, API contract |
| Client messages embed `[Model: ...]` and `[Provider: ...]` tags. | New chat and appended chat paths in [`Chat.client.tsx`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/components/chat/Chat.client.tsx#L435) and [`Chat.client.tsx`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/components/chat/Chat.client.tsx#L515) | Confirmed | Template seeding adds an extra hidden user message; the same tag pattern is still used. | walkthrough, provider module, API contract |
| The server route parses the same payload fields and reads `apiKeys` / `providers` cookies. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L51) | Confirmed | `/api.chat` has a local `parseCookies`; other routes use shared helpers. | walkthrough, code map, API contract |
| MCP tool processing happens before context optimization and response generation. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L87) and [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L210) | Confirmed | MCP service internals are not traced in this guide. | walkthrough |
| Context optimization runs only when files exist and the flag is enabled. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L97) and [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L108) | Confirmed | If there are no files, the final model call can still run without selected context. | README, walkthrough, chat-stream module |
| Summary and context selection contribute to cumulative token usage. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L121) and [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L163) | Confirmed | Usage depends on provider responses. | chat-stream module |
| `selectContext()` requires `<updateContextBuffer>` output and throws on invalid format or zero selected files. | [`select-context.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/select-context.ts#L179) and [`select-context.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/select-context.ts#L220) | Confirmed | The parser uses regex, not an XML parser. | walkthrough, code map, chat-stream module |
| Provider/model tags are extracted and cleaned before the model sees content. | [`utils.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/utils.ts#L8) and [`stream-text.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L85) | Confirmed | Attachments/parts preserve non-text parts. | walkthrough, provider module |
| `streamText()` resolves provider/model through static and dynamic model lists, with fallback behavior. | [`stream-text.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L107) | Confirmed | Fallback to first model can surprise users; the guide describes it as current behavior, not ideal behavior. | provider module |
| Provider classes are registered through `LLMManager` from the provider registry. | [`manager.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/modules/llm/manager.ts#L33), [`registry.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/modules/llm/registry.ts) | Confirmed | Dynamic provider APIs are not individually audited. | code map, provider module |
| Build mode adds selected file context, summaries, and locked-file instructions to the system prompt. | [`stream-text.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L165) and [`stream-text.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L198) | Confirmed | Effectiveness depends on model compliance. | walkthrough, chat-stream module |
| Reasoning models use `maxCompletionTokens`; other models use `maxTokens`, and unsupported options are removed for reasoning models. | [`constants.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/constants.ts#L25), [`stream-text.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L237) | Confirmed | The regex currently recognizes `o1`, `o3`, and `gpt-5` prefixes. | provider module |
| A normal finish writes cumulative usage and response-complete progress. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L230) | Confirmed | If the stream finishes by length, continuation logic runs instead. | walkthrough, API contract |
| Length finishes trigger a synthetic continue prompt until `MAX_RESPONSE_SEGMENTS` is reached. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L252), [`constants.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/constants.ts#L36) | Confirmed | `SwitchableStream.switches` is used as the segment counter, but the current route merges streams directly; future changes should re-check this mechanism. | walkthrough |
| Common provider/API errors are converted into custom user-facing messages. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L349) | Confirmed | Error matching is substring-based. | walkthrough |
| The current test surface does not include a direct `/api/chat` route test. | `find` found `app/utils/diff.spec.ts`, `app/components/chat/Markdown.spec.ts`, and `app/lib/runtime/message-parser.spec.ts`. | Confirmed | A deeper search may find generated or ignored test artifacts, but no normal source test was discovered. | README, API contract |

## Falsifying checks

Run or inspect these when the chat guide may be stale:

```bash
rg -n "api: '/api/chat'|\\[Model:|\\[Provider:" app/components/chat/Chat.client.tsx
rg -n "updateContextBuffer|No user message found|Bolt failed to select files" app/lib/.server/llm/select-context.ts
rg -n "finishReason !== 'length'|MAX_RESPONSE_SEGMENTS|Custom error:" app/routes/api.chat.ts
```

Evidence status: Confirmed unless noted.
