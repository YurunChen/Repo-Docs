# bolt.diy Web Chat Code Map

This map covers the first-party source areas that own the documented browser-prompt-to-streamed-answer path. Read [how one prompt becomes a streamed answer](walkthroughs/one-real-run.md) first if the behavior is not clear yet.

| Path | Responsibility | Key code | Connection to the main path |
| --- | --- | --- | --- |
| `app/components/chat/` | Builds the browser-side request from the user message, workbench state, and selected provider/model. | [`Chat.client.tsx`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/components/chat/Chat.client.tsx#L134) | Creates the request contract sent to `/api/chat`. |
| `app/routes/` | Orchestrates the server request, context work, response continuation, annotations, and user-facing stream errors. | [`api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L51) | Owns the central relay between browser and model stream. |
| `app/lib/.server/llm/` | Selects context, cleans model tags, assembles prompts, resolves the model call, and monitors streaming. | `select-context.ts`, `stream-text.ts`, `create-summary.ts` | Implements the non-trivial context and model-call boundaries. |
| `app/lib/modules/llm/` | Registers providers and exposes static and dynamic model lists. | `manager.ts`, `registry.ts` | Supplies provider/model choices to the server stream helper. |

## `app/components/chat/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `app/components/chat/Chat.client.tsx` | Adds workbench fields and provider/model tags, then starts or appends the chat request. | `useChat`, send path | Browser chat UI; contract fields are detailed in the chat API module. |

## `app/routes/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `app/routes/api.chat.ts` | Parses request/cookie state, runs MCP and context work, merges the model stream, continues length-limited output, and maps errors. | `action()`, data-stream execution, `onError` | `/api/chat`; verify nearby behavior with `pnpm run typecheck` and `pnpm run test`. |
| `app/routes/api.models.ts` | Exposes model-list behavior adjacent to chat model selection. | model route | Provider/model UI and lookup surfaces. |

## `app/lib/.server/llm/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `select-context.ts` | Requires a bounded XML-like file selection and rejects invalid or empty selections. | `selectContext()` | `/api/chat` context optimization. |
| `stream-text.ts` | Removes provider/model tags, resolves a model, builds the mode-specific prompt, and starts the AI SDK stream. | `streamText()` | `/api/chat` response generation. |
| `create-summary.ts` | Compresses earlier chat history before selected context is attached. | summary helper | Context optimization and usage accounting. |
| `stream-recovery.ts`, `switchable-stream.ts` | Monitor activity and support stream handoffs. | recovery and stream wrappers | The route's continuation and timeout surfaces. |

## `app/lib/modules/llm/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `manager.ts` | Stores registered providers and combines static with dynamic model lists. | `LLMManager` | `streamText()` and model-list routes. |
| `registry.ts` | Defines which provider classes enter the manager. | provider registry | Provider initialization. |

## Coverage

Covered: browser chat request construction, `/api/chat`, context optimization, provider/model resolution, and stream continuation/error handling. Electron startup, deployment integrations, Git and Supabase flows, workbench action-to-file writes, individual provider implementations, and MCP server internals are excluded or deferred because they sit outside the streamed-answer boundary.

Read [how chat streaming manages context pressure](modules/chat-stream.md) or [how provider tags become a model instance](modules/provider-model-selection.md) for mechanism detail.

Evidence status: Confirmed unless noted.
