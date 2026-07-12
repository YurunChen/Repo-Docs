# Quality review

## Reader Simulation

| Reader question | Answer from the guide |
| --- | --- |
| What real path is followed? | A user sends a workbench chat prompt; the client posts to `/api/chat`; the server selects context, resolves provider/model, and streams the response. |
| What is hard or non-trivial? | The route must keep context useful but bounded, and it must resolve user-selected providers/models that can come from static or dynamic lists. |
| What changes at each phase? | Text becomes a tagged request contract; request state becomes stream prework; selected files and summary become prompt context; provider tags become a model instance; model output becomes stream chunks and annotations. |
| Where would I change this behavior? | [`code-map.md`](../code-map.md) routes browser request changes to `app/components/chat/`, route orchestration to `app/routes/`, and context/model-call behavior to the two LLM source areas. |
| Where do assumptions stop? | `selectContext()` can fail on invalid or empty selector output; provider lookup can fail or fall back; the guide stops before generated actions become workbench file changes. |
| What would prove this explanation wrong? | Removing provider/model tags from `Chat.client.tsx`, changing `selectContext()`'s response contract, or changing `/api/chat` continuation/error handling. |
| What would a careful newcomer ask next? | How streamed `<boltAction>` output is parsed and applied to files; deferred to a future guide pass. |
| How can I verify it? | Read `references/source-evidence.md`, run the repo-docs validator, and run `pnpm run typecheck` / `pnpm run test` for the available code checks. |

## Review Table

| Review question | Result | Evidence | Follow-up |
| --- | --- | --- | --- |
| Can a reader state the hard part of the main path in one sentence? | Pass | README and walkthrough both name context pressure and provider/model resolution. | Add route-level tests if future work changes chat behavior. |
| Can the walkthrough still explain the flow if source links are hidden? | Pass | Each step starts with user-visible or system-visible behavior before source locators. | Keep source names out of first paragraphs in future syncs. |
| Is there a real boundary or failure path? | Pass | Invalid context selector format, empty selected files, model lookup failures, token-limit continuation, and mapped provider/API errors are documented. | Re-check `SwitchableStream` use if continuation is refactored. |
| Are claims backed by evidence? | Pass | `references/source-evidence.md` has Pass 1 and Pass 2 rows plus claim/evidence/caveat mapping. | Add command output from route-specific tests if such tests are introduced. |
| Does the evidence map name adjacent paths checked but not traced? | Pass | Coverage and exclusions list Electron, deployment, workbench artifact parsing, provider internals, and MCP internals. | Build another walkthrough for artifact parsing when needed. |
| What residual risk remains? | Source-confirmed but not route-test-confirmed | Tests discovered in normal source paths do not directly cover `/api/chat`. | A future sync should update the guide if route tests are added or behavior changes. |

Evidence status: Confirmed unless noted.
