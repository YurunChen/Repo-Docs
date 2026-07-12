# Repo-Docs Sync Rules

## Sync Scenario Map

Use the smallest scenario that matches the turn. When a trigger appears, run a foreground sync gate before the final response: inspect enough guide and source context to decide whether the guide would mislead. The gate must produce one explicit decision: `none`, `answer-only`, `foreground patch`, or `background sync`.

Ordinary repo questions are not automatic doc edits. Answer from inspected guide and source when the guide is current enough, the gap is not durable, or the missing detail is not answer-critical and not a small local patch.

Do not run widened content sync just because a normal repo question or code edit happened. Use a background sync agent for broader, non-answer-critical documentation work when the platform supports it, so the user is not blocked by a doc sweep.

| Scenario | Trigger | Goal | Scope |
| --- | --- | --- | --- |
| Foreground Sync Gate | Any repo-docs trigger appears. | Decide quickly whether the current answer/code path would mislead without a guide update. | Relevant guide page, current source evidence, and one decision: `none`, `answer-only`, `foreground patch`, or `background sync`. |
| Answer-only | A repo question touches guide-covered knowledge, but the guide is current enough or the gap is not answer-critical/small/local. | Answer accurately without editing docs. | Relevant guide page and current source evidence. |
| Per-turn Understanding Sync | A repo question, architecture/onboarding answer, user correction, user uncertainty, or behavior-bearing source/config/data/test change touches guide-covered knowledge and the guide gap is answer-critical or small/local. | Prevent the current answer and guide from misleading the user or next reader. | Relevant guide page, current source evidence, and `change-log.md` only when the patch is meaningful. |
| Background Repo-Docs Sync | A durable guide gap exists, but the required update is broader than a small local patch and is not required for the current answer to be correct. | Keep user interaction moving while still making `repo-docs/` converge. | Background agent handoff with trigger, durable facts or changed source areas, candidate guide pages, verification, and expected `change-log.md` update. |
| Conversation / Memory Promotion Sync | Stable project knowledge surfaces, is discovered, or is clarified in conversation; the agent is about to write or update memory; or the user asks to preserve/sync handoff knowledge. | Keep durable project knowledge in the guide before leaving only a chat or memory pointer. | Compare each durable fact with `repo-docs/`; patch the smallest owning guide page in foreground when answer-critical or small/local, otherwise answer-only or launch a background sync handoff; use root agent files only for future-agent operating rules. |
| Widened Docs Sync | The user explicitly asks to sync, tidy, clean up docs, update memory, prepare a handoff, finish a milestone, repair stale docs, or make the repo ready for a newcomer. | Align the whole knowledge system with current code and decisions. | Prefer a background sync agent when available; otherwise inventory memory when available, root agent files, README, `repo-docs/`, nearby docs, and affected cross-project docs. |

Store facts by ownership:

- Project behavior, architecture, operations, APIs, data, and current decisions -> `repo-docs/` or README.
- Future-agent operating constraints and routing rules -> `AGENTS.md` / `CLAUDE.md`.
- Meaningful guide changes and historical sync anchors -> `repo-docs/change-log.md`.
- Personal preferences and cross-project reminders -> agent memory when available.
- One-off debug state, temporary run output, and local quirks -> chat unless the user asks to preserve them.

## Follow-up Question Loop

Canonical pipeline: [Sync gate](SKILL.md#sync-gate) — **interaction-driven**, not a post-hoc doc sprint.

During the user ↔ coding agent conversation, when a repo question appears and `repo-docs/` is relevant:

1. Read `repo-docs/README.md`, the main walkthrough, `code-map.md` when source ownership or change location matters, and any relevant module, source-evidence, quality-review, or glossary pages.
2. Inspect the source-of-truth code, data, config, tests, or artifacts behind the answer.
3. Decide one outcome:
   - `none`: the question is unrelated to guide-covered knowledge.
   - `answer-only`: the guide is current enough, or the gap is transient, non-durable, not answer-critical, and not a small local patch.
   - `foreground patch`: the guide would mislead the answer, says the opposite, or misses a small stable owning-page fact.
   - `background sync`: the gap is durable but broader than the current answer needs, and a real tracked handoff exists.
4. For `foreground patch`, patch the smallest narrative home **in this turn**; record meaningful work in `change-log.md` with `Synced through <sha>` when git is available.
5. For `background sync`, launch or hand off to a background `repo-docs` sync agent and continue the user-facing answer. The final response should say that a background docs sync was started or could not be started when that status matters.
6. For `answer-only`, answer with the conclusion and cite the existing guide section or inspected source. Do not edit docs just because the question was asked.

## Project Change Sync

Canonical pipeline: [Sync gate](SKILL.md#sync-gate) — judged **per turn** while coding with the user.

If this conversation changed code, data, config, scripts, tests, or architecture and `repo-docs/` exists, compare the change with the guide before the final response unless the user asked to leave docs untouched. Use `answer-only` when the guide remains current or the changed detail is outside guide scope. Patch before the final response when the changed behavior is covered by the guide and the current answer or edit would otherwise mislead the next reader. Use a background sync agent for broader follow-up guide work that is not required for answer correctness. Do not leave a known answer-critical guide break for a later "sync session" when the thread already shows which reader model broke.

## Background Sync Delegation

Background delegation is for user-latency control, not for skipping sync judgment. The current agent still performs the foreground sync gate: identify the trigger, inspect enough guide/source context to classify the gap, and decide whether a foreground patch is required.

Use background sync when all are true:

- The gap is durable and belongs in `repo-docs/`.
- The current answer or code edit remains correct without waiting for the full doc update.
- The update is broader than a small owning-page patch, such as widened inventory, several guide pages, cross-project docs, large evidence review, or cleanup of repeated memory.
- The platform can actually run or track a background agent, thread, job, or handoff. A vague TODO is not background sync.

Do not background the sync when:

- The current answer depends on the corrected guide fact.
- The guide currently says the opposite of the answer in the touched area.
- The missing or stale content is a small local patch that belongs in the owning guide page now.
- The user explicitly asks to complete docs before proceeding.
- No background agent or trackable handoff mechanism is available and silently deferring would hide the gap.

Background handoff contract:

```text
Task: repo-docs background sync
Trigger: <repo question | behavior change | user uncertainty | memory promotion | widened sync>
Durable facts or changed source areas: <specific facts/files/commands/tests>
Current guide pages to inspect first: <README, walkthrough, code-map, module, source-evidence, quality-review, glossary, change-log>
Likely owning pages: <smallest pages to patch>
Must preserve: <answer-critical facts already given to user, user constraints, language>
Verification: <validator/link check/test/source inspection>
History: update repo-docs/change-log.md with trigger, changed pages, verification, and Synced through <sha> when git is available
Return: summary of changed files, verification result, unresolved gaps
```

If a background sync is launched, the foreground answer should mention only the useful status: what the user can proceed with now, and that docs sync is running or queued. Do not make the user wait for a broad sync unless they asked for that.

## Documentation Content Sync Alignment

Use this **widened-scope** strategy only when the user explicitly asks to sync, tidy, clean up docs, update memory, prepare a handoff, finish a milestone, repair stale docs, or make the repo ready for a newcomer. Day-to-day guide maintenance still uses the [Sync gate](SKILL.md#sync-gate) inside the coding conversation when a repo question or behavior-bearing edit makes the guide relevant.

Act as a knowledge-base editor: review the whole knowledge system, merge repeated facts, correct stale facts, remove obsolete notes, and keep every reader-facing layer aligned with current code.

### Knowledge layers

Different layers serve different readers:

| Layer | Audience | Responsibility | Healthy shape |
| --- | --- | --- | --- |
| Agent memory, when available | The agent across sessions | Personal preferences, cross-project references, recent lessons, and compact reminders. | Thin, current, pointer-heavy. |
| Root `AGENTS.md` / `CLAUDE.md` | Future agents working inside this repo | Hard constraints, commands, environment rules, red lines, routing tables, and guide maintenance policy. | Short, operational, rule-oriented. |
| `README.md` and `repo-docs/` | Human teammates, downstream users, and future agents | Onboarding, architecture, operations, integration, APIs, repo docs, and references. | Thick authority layer with current facts. |

Root agent files are rule manuals. Put details in `repo-docs/`; keep root instructions for facts that prevent future agents from breaking project constraints. Put historical narratives in `change-log.md`, `change-log.archive.md`, git history, or a project changelog.

### Promotion rule

Agent memory often grows by appending. Docs converge by editing current facts in place. Use promotion to keep memory thin:

| Memory item | Destination |
| --- | --- |
| Same lesson appears repeatedly | Owning guide page, module doc, or root rule. |
| Item explains how the system works | `repo-docs/`, with memory reduced to a pointer if useful. |
| Item records a project fact that is now current | Current-state docs plus `change-log.md` when the change is meaningful. |
| Durable conversation fact, user-uncertainty answer, or source-discovered explanation missing from `repo-docs/` | Smallest owning guide page when answer-critical or small/local; otherwise answer-only or background sync handoff. |
| Item is a personal or cross-project preference | Agent memory. |

The deciding question: will the next maintainer, teammate, downstream integrator, or future agent need this knowledge to understand or operate the project? If yes, make docs the source of truth.

When stable project knowledge surfaces in conversation, is discovered while answering user uncertainty, or is about to be written to memory, compare each durable fact with `repo-docs/` even if the user did not ask for memory sync. If no current guide page owns it, patch the smallest page only when the fact is answer-critical or small/local; otherwise use `answer-only` with inspected evidence or background sync when the platform has a real trackable handoff and the current answer remains correct while it runs. Use root `AGENTS.md` / `CLAUDE.md` only for operational rules that future agents must follow.

### Size and freshness check

Run size checks before content sync:

| File or area | Target | Action when large |
| --- | --- | --- |
| `AGENTS.md` / `CLAUDE.md` | About 300 lines or 15KB | Compress to rules, command tables, red lines, and doc pointers. Move detailed mechanisms into docs. |
| Memory index, when present | At most 200 lines and 25KB | Promote stable knowledge into docs; leave compact pointers and recent lessons. |
| Single memory file | About 100 lines | Split recent lessons or promote stable mechanism content. |
| Single docs page | About 1500 lines | Split by concept, workflow, module, or audit type; add an index page. |

Also compare memory size against docs size when memory exists. Healthy projects have docs as the heavier authority layer and memory as the lighter routing layer.

### Inventory pass

Before deciding which guide pages to update, enumerate the knowledge surface:

1. List agent memory files when the current platform has a memory layer.
2. For each project touched by the conversation, list the project root.
3. List `repo-docs/` and confirm missing guide pages explicitly.
4. Find nearby Markdown files outside `repo-docs/`, excluding dependency and git folders.
5. Read `README.md`, root `AGENTS.md` / `CLAUDE.md`, current guide pages, and relevant docs.
6. Review the current conversation for durable facts, decisions, and changed behavior.

Keep an internal file inventory with each file marked as evaluated, changed, or left current.

### Impact mapping

Think from the changed behavior outward:

| Change | Docs to align |
| --- | --- |
| New API, route, tool, or external surface | README route map, relevant walkthrough, `code-map.md`, owning module, runbook/root command table when applicable. |
| New or renamed environment variable | Runbook, root instructions, setup docs, integration guide when downstream users see it. |
| New data store, table, schema, task format, or artifact | Owning module, relevant walkthrough, reproduction path, source evidence. |
| New feature crossing several concepts | README, walkthrough, `code-map.md`, affected modules, runbook, change log, handoff notes. |
| Cross-project contract change | Upstream and downstream modules/docs, SDK/API usage modules, integration examples. |
| Completed plan or replaced decision | Current docs updated in place; durable history recorded in `change-log.md` or archive. |
| Terminology or rule change | Glossary, affected module docs, root rules when it changes agent behavior. |

For a new capability, cover four reader questions: how to use it, how it works, how to operate it, and how to know it shipped.

### Editing principles

- Prefer reducing, merging, and editing current facts in place.
- Add new text where it changes a reader decision or prevents a future mistake.
- Keep root agent files operational: constraints, commands, environment, permissions, routing, red lines, and guide policy.
- Keep docs reader-facing: onboarding, architecture, operations, integration, examples, contracts, and source evidence.
- Use absolute calendar dates, not relative phrases such as "today" or "recently".
- Keep API shapes, environment tables, glossary entries, and command examples current in the owning module or runbook.
- For memory, promote stable knowledge into docs and leave compact pointers when useful.
- For cross-project changes, run the inventory and impact mapping for each affected project.

### Sync checklist

- [ ] The foreground sync gate ran for each trigger; widened content sync ran only when explicitly triggered or delegated as background follow-up.
- [ ] Background sync, when used, had a concrete handoff and did not hide an answer-critical guide break.
- [ ] Size checks ran for root agent files, docs pages, and memory indexes when present.
- [ ] Stable memory or conversation knowledge missing from `repo-docs/` graduated into the smallest owning guide page or root rule.
- [ ] Root agent instructions contain operational rules and guide policy.
- [ ] README and docs explain how to understand, run, integrate, and operate the project.
- [ ] Changed APIs/routes appear in the owning module or walkthrough.
- [ ] Added, removed, renamed, or responsibility-changing first-party source directories, entrypoints, and important files appear in `code-map.md` with the nearest useful verification point.
- [ ] Changed environment variables appear in setup/runbook docs and root instructions.
- [ ] Changed data models or schemas appear in the owning module and source evidence.
- [ ] Cross-project effects are reflected in every affected project.
- [ ] Relative-time language such as today, yesterday, recently, 今天, 昨天, 最近 has been replaced with absolute dates.
- [ ] Local links, paths, commands, tool names, and environment variables resolve against the current repo.
- [ ] The final summary lists actual changed files and any unresolved item.

### Closeout summary

For **widened-scope sync**, handoff, and milestone closeouts—not first-time **Build** handoff (see [SKILL.md](SKILL.md#delivery)). After edits, summarize by changed layer:

```text
## Sync Complete

### Memory
- Updated: ...
- Added: ...
- Removed: ...

### Documentation
- <project>/README.md — ...
- <project>/repo-docs/... — ...
- <project>/AGENTS.md — ...

### Unresolved
- ...
```

### Change impact map

| Change type | Docs to check |
| --- | --- |
| New or renamed entrypoint/script | `README.md`, relevant walkthrough, `code-map.md`, `flows.md` for multi-phase changes, relevant concept page |
| Runtime/session/control-flow change | relevant walkthrough, `code-map.md`, `flows.md` or `flows/<topic>.md`, runtime concept page when needed, README route map |
| New tool or changed tool args | tool module when needed, walkthrough if behavior changes, glossary if term changed |
| Data/schema/task/config change | data/task/config module when needed, local caveat if uncertainty remains, `change-log.md` when user-facing |
| Rule or metric change | rule/evaluation module when needed, main guide confidence/summary |
| Memory method change | memory module when needed, artifact/output module if outputs changed |
| Output/log artifact change | logging/artifacts module when needed, run/debug sections |
| Concept moved/deleted/merged | corresponding `modules/*.md`, README route map, links from other docs, `change-log.md` |
| Terminology changed | `glossary.md`, main guide, affected module docs, source evidence, or quality review |
| User-facing docs generated or reorganized | `README.md`, affected docs, repo-root agent instruction files, `change-log.md`, `change-log.archive.md` if archiving |
| Research experiment or baseline change | research overview/main guide, entrypoint docs, metrics/artifacts module, reproduction path |

### Sync checklist

- [ ] If `repo-docs/` exists and source/data/config/test behavior changed in a guide-covered or reader-visible way, guide impact was checked before final response; answer-critical or small stale owning pages were patched, while broader non-answer-critical work was delegated to a trackable background sync when available.
- [ ] Every changed source area maps to a current doc or a local caveat beside the affected topic.
- [ ] Module docs explain current concepts that readers actually need.
- [ ] Main guide includes quick understanding, reproduce/run, and verify paths.
- [ ] Non-Seed repos include `walkthroughs/one-real-run.md`, linked from README.
- [ ] Standard packages include `code-map.md`, linked from README; every in-scope first-party source directory is mapped or explicitly excluded/deferred with a reason.
- [ ] Walkthroughs use numbered `## Step N: [behavior]` sections and connected prose; no template `###` stack under every step; no duplicate closing sections that repeat the steps.
- [ ] README orients the reader without repeating the walkthrough's full explanation.
- [ ] Module docs deepen concepts without copying walkthrough paragraphs; link back instead.
- [ ] If module pages exist, the README route map points readers to the useful concept pages.
- [ ] Repo-root agent instruction files mention `repo-docs/` guide synchronization when they exist.
- [ ] `change-log.md` entries include `Synced through <sha>` after meaningful sync work when git is available.
- [ ] `change-log.md` entries use precise local timestamps with date, time, and timezone.
- [ ] `change-log.md` is recent enough to scan; older entries are archived when needed.
- [ ] If `flows.md` exists, it maps relationships between multiple paths, phases, states, or outputs instead of duplicating the main walkthrough; detailed flows live under `flows/<topic>.md` when useful.
- [ ] Module docs contain the concepts, details, representative examples, source locators, caveats, and verify hooks needed to understand the mechanism; `references/` contains only fixed generated artifacts: source evidence and optional quality review.
- [ ] Local Markdown links resolve.
- [ ] Current facts are edited in place; historical notes are used for durable history.
- [ ] Documentation content sync alignment ran when the user asked for sync, tidy, handoff, milestone closeout, memory refresh, or stale-doc repair.
- [ ] Cleanup/removal requests removed stale guide paths, links, and root guide-maintenance policies instead of leaving future agents pointed at missing docs.
