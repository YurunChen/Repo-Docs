---
name: repo-docs
description: Build and maintain a Markdown guide that helps humans understand a repository through real behavior, concepts, and evidence. Use when a user asks to understand a repo, generate or update repo-docs, answer repo-architecture/onboarding questions, seed docs for a new project, sync docs after code changes, or delete generated repo docs.
---

# Repo-Docs

## Mission

`repo-docs` explains a repository to a human reader.

Do not start with a tree tour. Build a reader model first: what problem the repo solves, one real behavior it performs, the concepts behind that behavior, where those responsibilities live in code, where source truth lives, and how to verify the understanding.

## Load Order

1. Read this file first.
2. Open [REFERENCE.md](REFERENCE.md) for task routing when detailed rules are needed.
3. Open only the topic file the router points to.
4. Open [EXAMPLES.md](EXAMPLES.md) only for finished-page tone or output-shape examples.
5. Prefer bundled scripts over rewriting deterministic checks.

Keep the routing narrow. `SKILL.md` defines the contract; topic files carry the detailed rules. If a detail appears in two places, keep it in the topic file and leave a pointer here.

## Document Contract

| File | Role |
| --- | --- |
| `SKILL.md` | Entry: mission, core laws, output contract, mode router, finish gate |
| `REFERENCE.md` | Router to topic files; open only when detail is needed |
| `WRITING.md` | Explanation design, voice, evidence discovery |
| `PAGE_RULES.md` | Build workflow, reader paths, page types, output shape, navigation |
| `SCOPE_MODES.md` | Seed, large/monorepo scope, specialized repos |
| `SYNC_RULES.md` | Sync decision gate, question loop, change sync, widened content alignment |
| `ROOT_AGENT_RULES.md` | Root `AGENTS.md` / `CLAUDE.md` routing block and install contract |
| `QUALITY_RULES.md` | Evidence labels, source truth, quality bar |
| `EXAMPLES.md` | Finished-page tone and output-shape examples |
| `scripts/validate_repo_docs.py` | Structure, links, sync anchors, freshness, evidence, references scope, and quality-review checks |
| `validate_repo_docs.py` | Compatibility wrapper for older invocations |
| `evals/` | Source-repository regression fixtures and assertions for this skill; not required at runtime |
| `../repo-docs-zh/SKILL.md` | Chinese language overlay |

## Core Laws

- Behavior before inventory: teach one real workflow, request, task, failure, or data path before describing the tree.
- Code location after behavior: once the reader understands one real path, map every in-scope first-party source directory and the key files or symbols needed to locate changes without repeating module explanations.
- Representative case before abstraction: when a module explains a mechanism whose meaning depends on inputs, state changes, outputs, decisions, or boundaries, include a compact evidence-backed case or explicitly state why a case would mislead.
- Shape follows reader need: prose explains why; structure shows what. Use tables, lists, timelines, fenced blocks, or flowcharts when they make comparisons, cases, sequences, commands, or lookup easier to scan.
- Evidence before claims: inspect source, tests, config, data, commands, or artifacts before writing durable statements.
- One durable fact, one home: code location lives in `code-map.md`; concept knowledge and mechanism details live in `modules/`; fixed generated audit artifacts live in `references/`; terms live in `glossary.md`; guide history lives in `change-log.md`.
- Sync only when the guide would mislead: ordinary repo questions require a foreground decision, not automatic doc edits.
- Validate before delivery: run the validator or state why it could not run.

Red flags that mean stop and re-route:

| Thought or draft move | Better action |
| --- | --- |
| "I'll start with the file tree." | Pick the behavior the reader should follow. |
| "The path/function name explains it." | Write the reader handle first; use source as proof. |
| "This schema/catalog deserves a references page." | Put details in the owning module; keep `references/` fixed. |
| "A repo question always means patch docs." | Run the sync decision gate and use `answer-only` when the guide is already safe. |
| "The docs look fine; no validator needed." | Run the validator or report the blocker. |

## Output Contract

Use the smallest package that teaches the repo honestly.

- Standard: `README.md`, `walkthroughs/one-real-run.md`, `code-map.md`, `modules/`, `references/source-evidence.md`, `glossary.md`, `change-log.md`; add `references/quality-review.md` when the guide is source-heavy, high-risk, generated, or handoff-sensitive.
- Lite: `README.md`, `walkthroughs/one-real-run.md`, `references/source-evidence.md`, `change-log.md`; use for small repos with little durable terminology. Add `code-map.md` when the small repo still has multiple first-party implementation areas or the reader needs a change-location index.
- Seed: `README.md`, `change-log.md`, optional `glossary.md`; label facts as `Confirmed`, `Planned`, or `Unknown`.

## Page Ownership

| Page | Job |
| --- | --- |
| `README.md` | Orient the reader and point to the first useful path. |
| `walkthroughs/one-real-run.md` | Follow one real behavior end to end with numbered `## Step N: behavior` headings. |
| `code-map.md` | Map in-scope first-party directories to responsibilities, key files or symbols, main-path connections, and change locations after the behavior model is established. |
| `modules/<concept>.md` | Explain one durable concept named by the walkthrough, including details, representative cases, call/data shapes, commands, fields, caveats, and verification hooks needed to understand it. |
| `references/source-evidence.md` | Fixed generated evidence base: traversal log, coverage notes, claim/evidence/confidence/caveat rows, and source material later pages may use. |
| `references/quality-review.md` | Optional fixed generated audit note for source-heavy, high-risk, generated, or handoff-sensitive guides. |
| `glossary.md` | Three columns only: `Term | Plain meaning | Further reading`. |
| `change-log.md` | Meaningful guide changes and sync anchors. |

`references/` is not a lookup layer. Code location belongs in `code-map.md`; do not hide it in an audit artifact. Do not add extra files under `references/` for schemas, contracts, metrics, task catalogs, command lists, scripts, artifacts, or exact-name lookup. If a detail helps understanding, put it in the owning module. If it only proves a claim, put it in `references/source-evidence.md`.

## Modes

Modes name common situations, not detached jobs. Use [REFERENCE.md](REFERENCE.md) to open details only when the current mode needs them.

| Mode | Use when | What to do |
| --- | --- | --- |
| Seed | No real source/runtime/test/data contract yet | Status-labeled project memory; do not describe plans as implemented |
| Build | First repo docs or onboarding material | Follow [PAGE_RULES.md](PAGE_RULES.md#build-workflow), wire root agent rules from [ROOT_AGENT_RULES.md](ROOT_AGENT_RULES.md), run validator, deliver |
| Sync | Interaction, repo state, user uncertainty, surfaced conversation knowledge, or memory updates may make the guide stale or incomplete | Follow [SYNC_RULES.md](SYNC_RULES.md); decide `none`, `answer-only`, `foreground patch`, or `background sync` before answering |
| Cleanup / removal | User asks to delete generated repo docs | Remove the package and stale root pointers; do not recreate docs unless explicitly asked |
| Question refinement | A repo question shows the guide built the wrong model | Patch the smallest stable owning page, anchor in `change-log.md`, answer with a link |

## Sync Gate

When `repo-docs/` exists and a repo-docs trigger appears, ask: what would a new reader misunderstand if they read the guide as it stands?

The foreground gate must end in one decision:

| Decision | Use when |
| --- | --- |
| `none` | The turn is unrelated to guide-covered knowledge or the guide is absent/out of scope. |
| `answer-only` | The guide is current enough, or the gap is transient, non-durable, not answer-critical, and not a small local patch. Answer from inspected guide/source without editing docs. |
| `foreground patch` | The current answer or code change would mislead without a small owning-page update, the guide says the opposite, or a stable knowledge gap is small and belongs in the guide now. |
| `background sync` | The gap is durable but broader than the current answer needs, the answer remains correct, and the platform has a trackable handoff. |

Do not patch for one-off debug state, local environment quirks, or personal preference unless the user asks to preserve it.

## Build Summary

Detailed Build rules live in [PAGE_RULES.md](PAGE_RULES.md#build-workflow). The short version:

1. Inspect project instructions, README, entrypoints, scripts, tests, schemas, config, data, artifacts, and existing docs.
2. Choose one representative real behavior.
3. Build `references/source-evidence.md` as the evidence base with at least two traversal passes.
4. Draft the reader model, then write README and the walkthrough; build the code map from the now-understood behavior before writing deeper modules, glossary, and change log.
5. Wire root agent instructions from [ROOT_AGENT_RULES.md](ROOT_AGENT_RULES.md).
6. Run the validator and fix structure, links, evidence, references scope, and reading-experience issues.

For large repos or monorepos, scope the guide to one subsystem or workflow and say what is not covered.

## Writing Rules

Use [WRITING.md](WRITING.md) for voice and explanation rules. The short version:

- Start with the situation a reader can recognize, then explain the reason, mechanism, check, and caveat.
- Keep README and walkthrough openings low in code names.
- Never let a path, function, field, or metric carry the explanation.
- Follow the display-shape router in [PAGE_RULES.md](PAGE_RULES.md#markdown-display-protocol) when structure helps the reader scan.
- Use flowcharts only for phase handoffs, branching paths, or state changes.
- Put page-level evidence status at the end of narrative pages: `Evidence status: Confirmed unless noted.`

## Finish Checklist

Before delivery, confirm:

- The reader can start from `repo-docs/README.md` and reach the main walkthrough.
- `walkthroughs/one-real-run.md` follows one real behavior with numbered steps.
- Standard packages include `code-map.md`; it covers every first-party source directory inside the declared scope, names the important code inside each area, states exclusions, and routes deeper mechanism questions to modules.
- The walkthrough names a non-trivial pressure, a real boundary/failure/caveat when evidence exists, and one verification hook.
- Source links prove the explanation instead of replacing it.
- `references/source-evidence.md` exists and includes Pass 1/Pass 2 traversal rows, coverage/exclusion notes, a falsifying check, a likely reader follow-up, and a `Claim | Evidence | Confidence | Caveat | Used by` audit table.
- Optional `references/quality-review.md`, when present, stays an audit note rather than a second walkthrough.
- Modules carry the knowledge and details a reader needs to understand the repo; `references/` contains only fixed generated artifacts.
- Mechanism modules include a representative case for the key input, state change, output, decision, or boundary, unless the page states why a case would be misleading or unsupported by evidence.
- Project agent instruction Markdown contains the short `Repo docs` routing block, or the build explicitly explains why it was not written.
- `change-log.md` records meaningful guide work and includes `Synced through <sha>` when git is available.
- The validator ran, or the reason it could not run is stated.

## Verification

Before finishing, check structure, local links, source links, narrative flow, module ownership, fixed references scope, evidence maps, and quality review.

Run:

```bash
python scripts/validate_repo_docs.py <path-to-repo-docs> --repo-root <repo-root>
```

## Delivery

**First build:** tell the user what the reader can now do, where to start, the key pages, scope, validator result, and root agent-file status. Keep durable history in `change-log.md`, not in chat.

**Cleanup:** if the user asks to remove repo docs, delete the generated docs package and stale root-agent pointers. Do not recreate docs in the same turn unless explicitly asked.

**Widened sync closeout:** when the user explicitly asks to sync, tidy, hand off, or repair stale docs, follow [SYNC_RULES.md](SYNC_RULES.md) and summarize by changed layer, not as a substitute for per-turn sync decisions.
