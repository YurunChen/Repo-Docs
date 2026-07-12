# One real run: a prompt becomes a streamed answer

This walkthrough follows the normal web chat path: a user types a request in the workbench, chooses a provider and model, and receives a streaming answer. The hard part is keeping the model call useful without sending every file or trusting every provider/model choice blindly. The useful mental model is a relay with guardrails: the client creates an explicit message contract, the server trims and enriches context, provider selection resolves the actual model call, and the response stream carries progress, usage, and errors back to the browser.

## Step 1: the browser turns the prompt into a contract

The first handoff happens before the server sees anything. The chat UI configures `useChat` to post to `/api/chat` and includes the runtime body: API keys, current files, prompt ID, context-optimization setting, chat mode, design scheme, Supabase connection state, and MCP step limit. This makes a chat request more than a text message; it is the current workbench state plus the selected AI runtime. Source: [the hook body in `Chat.client.tsx`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/components/chat/Chat.client.tsx#L134).

When the user sends a new message, the client prepends `[Model: ...]` and `[Provider: ...]` to the text. On a new chat it calls `reload()` after `setMessages()`. On an existing chat it calls `append()`, and if the workbench has modified files it serializes those changes as artifacts before appending the user text. Source: [the send path in `Chat.client.tsx`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/components/chat/Chat.client.tsx#L479).

This tag-based handoff matters because the server does not rely on hidden UI state to know which model to call. The model and provider travel in the message content and are later stripped out before the prompt is sent to the model.

## Step 2: the route opens a stream and reads runtime state

The server route starts by parsing the JSON payload and reading provider settings from cookies. The fields it expects are `messages`, `files`, `promptId`, `contextOptimization`, `chatMode`, optional `designScheme`, optional Supabase credentials, and `maxLLMSteps`. It also parses `apiKeys` and `providers` cookies, then creates a streaming response path. Source: [the request setup in `api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L51).

Once streaming begins, the route starts stream recovery monitoring, asks the MCP service to process any tool invocations already present in the messages, and records where it may slice older messages if a summary is later available. Source: [the data-stream execution setup](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L93).

The visible output starts as server-sent stream data. The route writes progress annotations such as "Analysing Request", "Determining Files to Read", and "Generating Response", then returns a `text/event-stream` response. The exact stream format also adapts model "thought" chunks that begin with `g` into a rendered thought wrapper before forwarding bytes to the browser. Source: [stream transformation and response headers](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L383).

## Step 3: context optimization compresses history and selects files

If the request includes files and context optimization is enabled, the server does not send the full project blindly. It first creates a chat summary, writes a `chatSummary` annotation, then asks `selectContext()` to pick relevant files from the workbench file map. Source: [summary and context progress in `api.chat.ts`](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L108).

The selector has a strict format boundary. It shows the model available file paths, current context buffer, and the last user question, then requires a response wrapped in `<updateContextBuffer>`. It accepts `<includeFile path="..."/>` and `<excludeFile path="..."/>`, ignores paths outside the allowed file list, and throws if the response does not contain the expected wrapper or if no files are selected. Source: [the selector prompt and parser](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/select-context.ts#L121).

This is the main non-trivial pressure in the path. The app is trying to keep the model informed enough to edit code while keeping context small and bounded. The current implementation relies on another model call to select files, so bad selector output is a real boundary rather than a theoretical risk.

## Step 4: provider tags become an actual model call

Before calling the AI SDK, `streamText()` scans user messages for the provider/model tags and removes them from the content. It then finds the provider in the registered provider list, tries static models first, asks the provider for dynamic models if needed, and falls back to the first model if the requested model is unavailable. A special Google/Gemini error is thrown for a known wrong 2.5-style model name. Source: [provider and model resolution](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L83).

The model call also builds the correct prompt for the mode. In build mode, selected context files are wrapped as a context buffer and any chat summary can shorten the message list. Locked files are appended to the system prompt as explicit "must not modify" instructions. Discuss mode uses a separate discuss prompt. Source: [prompt assembly and locked-file handling](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L152).

Finally, reasoning models use `maxCompletionTokens` while regular models use `maxTokens`; unsupported sampling options are stripped for reasoning models before the AI SDK call. Source: [token and option handling](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/lib/.server/llm/stream-text.ts#L237).

For the provider concept behind this step, read [how provider tags become a model instance](../modules/provider-model-selection.md).

## Step 5: the answer streams, continues, or fails visibly

The route calls `streamText()` and merges the result into the data stream. As chunks arrive, stream recovery activity is updated; if an error chunk appears, the route logs it and stops recovery. Source: [the main stream merge](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L310).

A normal finish writes a `usage` annotation with cumulative prompt, completion, and total tokens, then emits a completed response progress update. If the AI SDK reports `finishReason === 'length'`, the route appends the partial assistant content plus a synthetic user `CONTINUE_PROMPT`, keeps the same provider/model tags, and calls `streamText()` again. It will stop after `MAX_RESPONSE_SEGMENTS` continuations. Source: [usage and continuation handling](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L221).

User-facing failure messages are shaped in one place. Model-not-found, invalid JSON responses, missing API keys, token limits, rate limits, and network/timeout errors are mapped to custom error text before the stream reaches the client. Source: [the `onError` mapping](https://github.com/stackblitz-labs/bolt.diy/blob/2e254ac19a696394030601bc602f54945b12bfc4/app/routes/api.chat.ts#L349).

## What would prove this wrong

The fastest falsifying check is to change or inspect the client contract: if `Chat.client.tsx` stops sending `[Model: ...]` and `[Provider: ...]` tags, the model-selection part of this walkthrough is stale. A second check is to inspect `selectContext()`; if it no longer requires `<updateContextBuffer>` or no longer throws on an empty selection, the context-boundary explanation must be updated. The audit trail is in [the source evidence ledger](../references/source-evidence.md).

Verification commands for the current source:

```bash
pnpm run typecheck
pnpm run test
python path/to/repo-docs-skill/scripts/validate_repo_docs.py repo-docs --repo-root .
```

Use [the web chat code map](../code-map.md) to locate the browser, route, context, stream, and provider-registry source areas behind this run.

Evidence status: Confirmed unless noted.
