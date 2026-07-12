# Repo-Docs Page Rules

## Reader Paths

The main guide should support these reader paths:

| Reader goal | What the guide should show |
| --- | --- |
| Understand quickly | thesis, why it exists, main workflow, and major concepts |
| Locate or change code | in-scope directory responsibilities, key files or symbols, tests, and the main change points |
| Reproduce or run | commands, config, expected outputs, artifact locations |
| Verify understanding | walkthrough verify command, tests named in prose |

Readers also arrive with different expertise, and scaffolding that helps a newcomer slows an expert who already holds the model. Treat plain-model and concept pages as skippable, not mandatory, and let the reading order match expertise:

| Reader | Entry point | Guidance level |
| --- | --- | --- |
| Newcomer | `walkthroughs/one-real-run.md` | connected narrative; plain model before code names |
| Intermediate | `modules/<concept>.md` | concept plus the details, source locators, examples, and checks needed to understand it |
| Expert | `code-map.md`, `modules/`, and source locators | fast source navigation after the behavior model, with evidence audit in `references/source-evidence.md` |

Offer this as a route in `README.md` only, not as repeated per-page banners. A short newcomer path and an expert fast-path that names its payoff, such as jumping directly to the relevant module, let a reader skip pages they do not need.

## Navigation Scent

Readers move through the package by following scent: at each link they judge, from the visible label and heading alone, whether the next page is worth the click. The label, not the destination, drives the decision, so a weak label sends readers down the wrong path or makes them give up.

- Every content page (`README.md`, `code-map.md`, walkthroughs, modules) should route the reader onward to the genuinely next-most-useful page. A page with no onward route is a dead end.
- Write onward links as natural in-prose links whose label names what the reader gains, not the filename and not the act of clicking. Prefer `see how the request becomes a result in modules/result-flow.md` over `see modules/result-flow.md` or `click here`.
- Scent is a property of how links are written, not a widget. Do not stamp a "Next" footer on every page; place the onward link where the reader actually needs it.
- The validator enforces this from the author side: it warns on content pages with no onward link and on low-scent labels (a bare filename or words like `here`, `this`, `see`). These checks add no text to the docs.

## Language Mode

`repo-docs` can write repo docs in Chinese or English. Treat language as a pack-level documentation contract.

| Situation | Language choice |
| --- | --- |
| User asks for Chinese | Write Chinese docs. |
| User asks for English | Write English docs. |
| Existing `repo-docs/` guide exists | Keep its primary language; convert when requested. |
| New guide, no explicit request | Use the user's current language. |
| Repo has established docs in one language | Prefer the repo convention if it helps future maintainers. |

Language quality rules:

- Preserve source terms exactly: paths, commands, config keys, API names, class/function names, metrics, error messages, and protocol fields.
- Translate surrounding explanation and reader guidance.
- Add parenthetical source terms only when helpful, such as `执行入口 (entrypoint)`.
- For Chinese docs, apply the `repo-docs-zh` overlay: Chinese carries the reader's mental model, while English source terms locate the code, fields, commands, and metrics.
- Prefer a single primary language because it is easier to keep synchronized.
- If bilingual docs are requested, define the structure explicitly, such as one bilingual page, `README.zh.md`/`README.md`, or a language-specific docs folder.

## Markdown Display Protocol

Markdown is the reading interface. Use it to control rhythm and reduce cognitive load.

| Element | Use for |
| --- | --- |
| Step headings (`##`) | Real behavior beats: `Step 1: input becomes a record` |
| Inline labels | Rare disambiguation only; prefer paths and checks woven into prose |
| Reader-state `###` headings | Long walkthroughs or one dense phase only |
| Blockquotes | Pull quotes from external docs when needed |
| Tables | Comparisons, before/after state, field lookup, phase relationships |
| Fenced code blocks | Commands, expected output, schemas, config, exact snippets |
| Mermaid / flowchart | Phase order, branches, state handoffs, or multi-path relationships—**when understanding needs a visual anchor**, always paired with prose |
| `<details>` | Long source details, full tables, long outputs |

When a page feels dense, first ask whether the reader needs a better heading, one small table, or a source detail folded into `<details>`. Do not add visual structure for decoration.

Display shape router:

| Reader need | Use |
| --- | --- |
| Understand cause, reason, pressure, or caveat | Short prose paragraphs |
| Compare concepts, states, choices, or before/after behavior | Table |
| Inspect fields, config keys, schemas, options, or parameters | Table or fenced block |
| Follow a sequence or lifecycle | Numbered list or short timeline |
| See a mechanism concretely | Representative case table or compact snippet |
| Reproduce behavior | Command block plus expected output or check |
| Hold several branches or state handoffs | Small Mermaid, flowchart, or ASCII diagram paired with prose |

Wall-of-text guard: prose explains why; structure shows what. If a paragraph carries more than one reason, one state transition, or one comparison, split it or convert the comparison, case, sequence, command, or lookup into a table, list, timeline, or fenced block. Long continuous prose is not a quality signal.

## Canonical Output Rule

Do not frame output as a file-count exercise. Use this rule:

```text
project spine -> real trace -> code map -> readable concept pages -> evidence audit -> glossary -> change log
```

The first-read route for most non-Seed repos should be:

```text
README.md
-> walkthroughs/one-real-run.md
-> code-map.md
-> modules
-> references/source-evidence.md when auditing evidence
-> glossary.md
```

Each named page serves a durable reader job. The output should feel concise because reader jobs are clear, not because files were skipped.

| Reader job | Preferred home |
| --- | --- |
| Understand the project idea and reading route | `README.md` |
| Understand the project model | `README.md` and `walkthroughs/one-real-run.md` |
| Replay one real behavior | `walkthroughs/one-real-run.md` |
| Locate responsibilities and likely change points in source | `code-map.md` |
| Understand a concept introduced by the walkthrough, including its important details | `modules/<concept>.md` |
| Audit evidence or residual quality risk | `references/source-evidence.md` or `references/quality-review.md` |
| Resolve project terminology | `glossary.md` |
| Compare several workflows or phases | `flows.md` |
| Preserve durable doc/project history | `change-log.md` |

The canonical non-Seed shape is defined in [SKILL.md](SKILL.md); this section governs which reader job each page serves and when triggered pages appear.

Additional walkthroughs, module pages, split `code-map/` pages, and `flows.md` are governed by reader-problem triggers: multiple workflows, independently navigated source areas, multiple runtime phases, state transitions, rule cases, failure modes, or concepts that need deeper explanation. Use trigger language rather than file-count language.

Merge pages when they explain the same reader concept. Do not merge merely to reduce file count.

`change-log.md` is part of the standard package and should stay compact: record meaningful changes to code, docs, data, experiments, or project understanding.

## Build Workflow

Build starts from evidence and ends with a guide a future reader can use without rediscovering the repo.

1. Read project instructions, README, entrypoints, scripts, tests, schemas, config, data, artifacts, and existing docs.
2. Choose one representative real behavior that reveals the repo shape. Treat this as a working candidate and refine it when evidence changes the model.
3. Create `references/source-evidence.md` immediately after choosing the representative behavior. This is a fixed generated intermediate artifact for the guide, not a reader-facing lookup page.
4. Run at least two evidence passes, updating `references/source-evidence.md` after each meaningful source inspection:
   - Pass 1 maps the main path: real entrypoints, real inputs, output or state changes, major handoffs, and first source locators.
   - Pass 2 challenges and fills the model with a Socratic reader interrogation: why each phase exists, what would break without it, what evidence could falsify the explanation, where assumptions stop, and which source area the first path skipped but depends on. It also inventories first-party source directories inside the declared scope so the code map can mark each area covered, excluded with a reason, or deferred.
   Add more passes only when the model still has unexplained gaps.
5. Draft the understanding brief from `references/source-evidence.md` before writing pages. The brief must name a real scenario, input, output, hard part, boundary or failure, falsifying check, likely reader follow-up, and the evidence for each claim.
6. Write `README.md` and `walkthroughs/one-real-run.md` from the understanding brief and evidence base. If the brief cannot name those fields, re-inspect source before writing the walkthrough.
7. Write `code-map.md` after the walkthrough has established the behavior. Cover every in-scope first-party source directory, identify the important files or symbols inside each area, connect them to the main path, and state what is excluded. Use the [Code Map Gate](#code-map-gate) for Standard, Lite, Seed, and large-repo scope.
8. Add modules for concepts, mechanisms, contracts, commands, data shapes, or caveats the walkthrough cannot explain cleanly inline. When a stable knowledge gap or understanding gap appears, resolve it by adding a focused module, refining the owning module, or merging overlapping modules so the reader still has one durable home for that concept. For mechanism-heavy modules, draft one representative case before polishing the prose: what goes in, what changes or gets decided, what comes out, and what boundary or failure variant matters.
9. Do not create extra `references/` pages. Schemas, metrics, tool parameters, task catalogs, scripts, artifacts, baseline methods, command lists, and exact-name lookup belong in the owning module when they matter to understanding. Source navigation belongs in `code-map.md`.
10. Run an understandability review before delivery. For case studies, generated examples, source-heavy docs, or handoff-sensitive work, write it as `references/quality-review.md`, the second fixed generated artifact.
11. Add `glossary.md` and `change-log.md`.
12. Wire the guide into the project's agent instruction Markdown using [ROOT_AGENT_RULES.md](ROOT_AGENT_RULES.md).
13. Run the validator and fix structure, link, evidence, references-scope, and reading-experience problems.

For large repos or monorepos, scope the guide to one subsystem or workflow and say what is not covered.

Build is not finished until the next coding agent can maintain the guide without rediscovering the policy. The project agent instruction Markdown is the handoff point: it should point to `repo-docs/README.md`, name the main walkthrough, and tell future agents to read the guide plus current source for repo questions and run the sync decision gate before answering.

## Code Map Gate

**Behavior first, code map second.** The walkthrough gives paths meaning; `code-map.md` then turns that model into source navigation. A code map answers “where does this responsibility live?” and “where should I start this kind of change?” It does not replace the walkthrough with a file inventory or repeat a module's mechanism explanation.

Use this gate by package mode:

| Mode | Code-map rule |
| --- | --- |
| Standard | Required. Cover every first-party source directory inside the guide's declared scope. |
| Lite | Add `code-map.md` when the repo has multiple first-party implementation areas or a reader cannot locate the main change points from the walkthrough alone. |
| Seed | Omit it until implemented source responsibilities can be confirmed. |
| Large repo / monorepo | Map the selected subsystem or workflow boundary, then name each adjacent first-party source area as covered, excluded with a reason, or deferred. Do not imply whole-repo coverage. |

Build the page in this order:

1. Open with the declared source scope and the behavior a reader should understand first.
2. Add a compact directory table: `Path | Responsibility | Key code | Connection to the main path` (Chinese: `路径 | 职责 | 关键代码 | 与主流程的关系`). Each responsibility must make sense without relying on the path name.
3. Add one section per in-scope first-party source directory. Use a compact table such as `Important code | Function | Key symbols | Called by / used by`, and include the nearest test or verification point when it materially helps a reader choose where to edit.
4. End with an explicit coverage note. Name generated, vendored, cached, fixture-only, asset-only, or unrelated areas that were intentionally summarized or excluded, and why.
5. Route deeper “why/how” questions to the owning module and route the runtime sequence back to the walkthrough.
6. End with the normal page-level evidence status.

Coverage depth follows repo size:

- Small repository: cover every first-party source directory and every meaningful implementation file; group only generated, vendored, fixture-only, or repetitive files.
- Medium repository: cover every first-party top-level source directory and the important nested directories, files, symbols, and tests that own the documented behaviors.
- Large repository or monorepo: cover every first-party source directory inside the declared subsystem boundary; list adjacent areas with explicit exclusion or deferral reasons.

List a file or symbol because it helps a reader locate a responsibility or change, not merely because it exists. Keep detailed fields, algorithms, contracts, and representative cases in the owning module. When the map grows beyond roughly 120 lines or independently developed subsystems have separate readers, keep `code-map.md` as the index and split details into `code-map/<subsystem>.md`.

### Lite shape

For a small or single-purpose repo with few durable concepts, the package can be smaller than the standard shape while keeping the Build evidence base:

```text
repo-docs/
  README.md
  walkthroughs/
    one-real-run.md
  references/
    source-evidence.md
  change-log.md
```

This is the same explanation path with fewer pages. Validate it with `python scripts/validate_repo_docs.py <path> --lite`. Promote to the full structure when the repo grows a concept worth its own module page.

When the Lite code-map gate fires, add `code-map.md` beside `README.md`; it does not require promoting the package merely because a small repo has multiple implementation areas.

## Large And Monorepo Scope

A large repository or a monorepo with several independent services does not need one package that documents everything. Scope the work before writing.

- Pick the target: the subsystem the user asked about, or the highest-traffic real workflow. Document that first; do not try to cover every package in one pass.
- Use one walkthrough per independent surface, named by behavior (`checkout-request.md`, `ingest-to-index.md`), not by service or module.
- Allow partial coverage. Record what is intentionally not yet documented in a short `README.md` coverage note with `Planned` or `Unknown` status, so the gap is visible instead of implied complete.
- For a monorepo, prefer one `repo-docs/` per independently developed package when packages have separate readers and lifecycles; use a single shared package only when one team reads across all of them.
- Stop when the reader can trace the targeted workflow end to end. Reading the whole tree is not the goal; a usable model of the chosen path is.

## Explanation Pass

Use the explanation pass during Build, after choosing the representative behavior and while `references/source-evidence.md` is being updated. The purpose is to keep the evidence ledger and narrative pages useful for a human reader while source inspection sharpens the model.

Reader understanding:

```text
observable behavior -> plain concept -> why it matters -> source locator -> verification
```

After choosing the representative behavior, create `references/source-evidence.md` as a living evidence ledger. Start with the traversal-log heading and the claim table, then update rows during source inspection. Build it with at least two passes over the evidence: first map the main behavior path, then revisit the repo with a Socratic reader interrogation to find missed guards, failures, tests, config precedence, artifacts, dependencies, falsifying evidence, and assumptions that could change the reader's model. The page acts as the evidence base for README, walkthroughs, the code map, modules, glossary, and quality review:

| Brief field | Requirement |
| --- | --- |
| Scenario | A real project behavior, not a generic architecture theme. |
| Input | The first observable command, request, data record, UI action, config, or failure case. |
| Success / output | The end state, response, file, commit, artifact, metric, or test result the reader can use as the target. |
| Hard part | The pressure this path handles, backed by inspected code, tests, config, or artifacts. |
| Boundary / failure | One real guard, retry, validation, parser rejection, fallback, or caveat when source evidence exists. |
| Falsifying check | The evidence, test, config, or artifact that would prove the explanation wrong or incomplete. |
| Next reader question | The skeptical follow-up a careful newcomer would ask, and whether the guide answers, defers, or labels it unknown. |
| Evidence | The source, test, command output, config, data, artifact, external input, or caveat proving each claim. |

Keep `references/source-evidence.md` as audit material: traversal log, claim, evidence, confidence, caveat, source family, and page consumers. Add, revise, merge, split, or downgrade rows as inspection changes the model. The walkthrough should link to it as proof when needed, while the walkthrough still carries the explanation.

Add an `## Evidence Traversal Log` section before the claim table:

| Pass | Purpose | Inspected evidence | What changed in the model |
| --- | --- | --- | --- |
| Pass 1 | Main path | Entrypoint, input, output/state, first handoffs | The initial behavior model. |
| Pass 2 | Socratic challenge/fill | Failures, retries, validation, config precedence, tests, artifacts, adjacent dependencies, in-scope source directories, falsifying checks | Boundaries, caveats, reader follow-ups, source-area coverage, and scope corrections. |

Add Pass 3+ only when needed. Also include a short coverage note naming adjacent paths that were checked but not traced, and why they are out of scope for the current guide.

The evidence map should be detailed enough that another agent can audit the walkthrough without rediscovering the path from scratch. Include omitted-but-adjacent paths when they explain scope, such as alternate CLI modes, UI surfaces, benchmark harnesses, or disabled branches, and label them as out of scope rather than silently ignoring them.

If writing a walkthrough or module exposes a weak claim, stop writing and re-inspect the relevant project evidence. Search the owning source path first, then tests, schemas, config, sample data, command output, or artifacts. Add the new evidence to the map or mark the claim as `Inferred` / `Unknown`; do not repair weak evidence with smoother wording.

If the hard part is inferred rather than directly shown by a test or explicit source branch, mark the claim as `Inferred` in prose or keep the wording modest. Never invent a cleaner input, output, error, command, or test just to make the story easier to tell.

Rules:

- Every narrative page should be readable before the reader knows function names, field names, or file layout.
- Every important walkthrough step should translate code behavior into plain language before giving a source locator.
- Every walkthrough step carries cause, effect, and the observation that matters before source details—in connected prose.
- Put details where they help understanding. A module may include fields, commands, schemas, tool parameters, metrics, artifacts, task cases, config contracts, call shapes, and data shapes when those details clarify the concept.
- Do not split a page only because it contains many source names. Split only when the reader is trying to understand two different concepts.
- Evidence status stays visible but quiet: one page-level default at the **end** of narrative pages; local labels only where confidence differs.
- `modules/` pages should exist only when they make a concept easier to understand than leaving it inside the walkthrough. They are reader-facing explanation pages built around one concept, its working details, representative examples, source locators woven into prose, and—when useful—a caveat or verify command that confirms understanding.
- Modules are not generated by count. They are generated when they lower cognitive load or answer a durable reader question.
- During sync, when user questions or source inspection reveal a stable knowledge gap or understanding gap, choose the module action that gives the reader one durable home: add a focused module, refine the existing owning module, or merge modules that explain the same concept.

## Project Model

Do not create a separate project-understanding page by default. Put the project model where the reader naturally needs it: a short first model in README, then concrete explanation inside the main walkthrough and concept pages.

A readable project model answers only what helps the reader move forward:

- What problem or workflow does this repo make easier?
- What real behavior proves the current shape?
- What concept should the reader remember before seeing code names?
- Which source path proves the behavior when they need to verify understanding?
- What caveat matters for the mental model?

Keep this explanation short. If it starts to look like a paper summary, fold it back into the walkthrough or concept page that needs it.

## Quality Review

Use `references/quality-review.md` when the guide is a case study, generated example, source-heavy package, or handoff-sensitive first build. This page is not a marketing summary. It is an audit note that records why the guide should be understandable and where risk remains.

For those heavier packages, include a `## Reader Simulation` section before or after the review table. Answer from the generated guide alone, as if the reviewer cannot open the source yet. The point is to catch documents that cite evidence correctly but still fail to transfer a usable model.

Default simulation table:

| Reader question | Answer from the guide |
| --- | --- |
| What real path is followed? | The command, request, task, user action, failure, or data record the guide tracks. |
| What is hard or non-trivial? | The pressure the repo must handle, stated without source names first. |
| What changes at each phase? | The state, output, decision, or handoff a reader should remember. |
| Where would I change this behavior? | The in-scope directory, important file or symbol, and nearest verification point named by `code-map.md`. |
| Where do assumptions stop? | A real boundary, failure, retry, validation, caveat, or out-of-scope path. |
| What would prove this explanation wrong? | The falsifying source, test, config, artifact, or missing evidence that would change the model. |
| What would a careful newcomer ask next? | The next guide page, source-evidence audit, glossary row, verify command, deferred topic, or unknown. |
| How can I verify it? | The evidence map, test, command, artifact, config, or source locator that checks the model. |

Default table:

| Review question | Result | Evidence | Follow-up |
| --- | --- | --- | --- |

Ask at least these questions:

- Can a reader state the hard part of the main path in one sentence?
- Can the walkthrough still explain the flow if source links are hidden?
- Can a reader use `code-map.md` to locate the owning source area and a verification point without scanning the repository tree?
- Does each step start with observable behavior, pressure, or effect before source names?
- Is there at least one real boundary, failure, retry, validation, or caveat path when evidence exists?
- Are claims backed by `references/source-evidence.md`, tests, commands, configs, data, or artifacts?
- Does the review name one falsifying check and one likely reader follow-up?
- Does the evidence map prove at least two traversal passes and name adjacent paths checked but not traced?
- What remains out of scope or only partially verified?

Keep the review short. If it starts to become a second walkthrough, fold the explanation back into the owning page and leave only the audit result here.

## Document Types

Design document types by reader state, not by source-tree structure:

| Reader state | Reader needs | Default page |
| --- | --- | --- |
| "I do not understand this project yet." | Natural first model and next step. | `README.md` |
| "I want to understand the project idea." | A plain model of the problem, main behavior, and caveats. | README and the main walkthrough |
| "Show me one real thing working." | A worked example with observable behavior and state changes. | `walkthroughs/one-real-run.md` |
| "Where does this responsibility live, and where should I start changing it?" | Scoped directory responsibilities, important files or symbols, related tests, and explicit exclusions. | `code-map.md` |
| "I understand the behavior, but this concept is still fuzzy." | Concept explanation, necessary details, representative evidence, and where to read next. | `modules/*.md` |
| "I need the exact shape to understand the concept." | Fields, commands, schemas, tools, metrics, artifacts, call shapes, and examples. | `modules/*.md` |
| "These project terms blur together." | Plain meaning for this project, with little or no code. | `glossary.md` |

Every page should provide information scent for the next useful page. If the reader may be lost, tell them where to restart.

The full package should preserve the explanation order defined above. Do not skip from user intent directly to source paths. Do not force a reader to cross the whole source tree before they have a concept model.

### Main guide: `README.md`

Use this to lower the first 15 minutes of confusion. Keep the shape aligned with [SKILL.md](SKILL.md#page-ownership): README orients, the walkthrough teaches one real behavior, modules deepen concepts and details, and references audit evidence or quality.

Opening prose (under the title) should cover, in order:

1. What the project does.
2. What behavior or user problem it exists to study.
3. What one real example will show the reader, with a link to the walkthrough.

Every README uses one stable `## Reader Routes` section after the opening model. The section is a reader-goal table with these columns:

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |

Use 3-6 rows. Each row starts from what the reader wants, links to one useful page, and names the payoff. Include the main walkthrough row in every Build package. Add rows for concept pages, glossary, source evidence, and quality review when those pages exist and serve a real reader goal.

Put caveats in a short closing note with compact bullets when needed.

Reader paths should be obvious from the table:

- New readers follow the main walkthrough.
- Readers locating or changing code use `code-map.md` after they understand the main behavior.
- Details needed for understanding live in `modules/`.
- Evidence audit lives in `references/source-evidence.md`.
- Repeated terms live in `glossary.md`.

For seed projects, use it as a project brief. Keep it honest about the empty state and make the next implementation decisions easy to find.

### Walkthroughs: `walkthroughs/`

Use walkthroughs to explain the repo through real behavior, not through module order. A walkthrough follows a command, request, task, user action, failure, rule case, or data record from the moment a reader can observe it to the resulting state, output, or result value. For non-Seed repos, create `walkthroughs/one-real-run.md` before writing deep module pages. If the repo has no real observable path yet, use Seed mode and record the path as `Planned` in `README.md`; do not present it as `one-real-run.md`.

The default `one-real-run.md` should read as one continuous explanation split into numbered steps. Shape, beats, and ownership follow [SKILL.md](SKILL.md#page-ownership) and the page-type rules here.

```text
title + opening prose (scenario + input + pressure + success/output + plain model + optional onward links)
-> ## Step 1: [behavior name]
-> ## Step 2: [behavior name]
-> ...
-> closing (end state + one verify command + onward links + evidence status)
```

The opening should make the walkthrough feel like a real task being inspected, not an architecture tour. It does not need a table, but it must answer these reader questions in prose:

| Opening question | What the reader should learn |
| --- | --- |
| Scenario | What concrete command, request, task, failure, user action, or data record are we following? |
| Input | What enters the system first? |
| Pressure | Why is this task not a trivial pass-through? Name the ambiguity, state handoff, external dependency, invalid input risk, output trust problem, or other force the repo must handle. |
| Success / output | What result, state, file, response, metric, commit, or artifact counts as the path running through? |

The pressure must be explicit enough that a reader could repeat it back. A vague task statement such as "a request becomes edits" is not enough. Write a plain sentence like "The hard part is..." or "This is tricky because..." when the difficulty might otherwise stay implicit.

Each `## Step N: ...` section carries plain model and mechanism in connected prose. The first paragraph of each step should give the reader the phase handle: what it receives, why it exists, what it changes, and what downstream code relies on. Weave paths, functions, and checks into the prose as proof when they help. Link to the matching `modules/<concept>.md` in the step where that concept first needs deeper explanation. Put **one** page-level verification block at the end unless a step needs a different check. Route to `references/source-evidence.md` only when the reader needs to audit the evidence base.

See [EXAMPLES.md](EXAMPLES.md) for the default flat walkthrough and the optional expanded shape for long pages.

Write the walkthrough with real project names: commands, files, functions, config keys, data records, test names, artifacts, routes, or UI actions. For each step, say what it receives, what it changes, and what downstream code relies on. When several branches or handoffs are hard to hold in prose alone, add a small Mermaid or ASCII flowchart after the plain-model sentence for that step. The diagram teaches the shape; prose still carries why and how to verify.

For non-trivial repos, include at least one real boundary path when source evidence exists: validation rejection, parse failure, retry, fallback, reflected error, lint/test feedback, stale cache, permission denial, or another guard. The goal is not to document every failure mode. The goal is to show where the system stops trusting happy-path assumptions.

Optionally, on the newcomer walkthrough only, note one path a reader might expect but the code does not take, and why. This makes the design reasoning visible. Use it sparingly: dead-end narration adds reading load, so keep it to one line and never put it on audit pages or fast-path pages where an expert would only be slowed by it.

Walkthrough count rules:

| Repo shape | Default walkthroughs | Add more when |
| --- | --- | --- |
| Small repo | 1: `one-real-run.md` | A second workflow is materially different. |
| Medium repo | 2-3 | There are distinct user paths, failure modes, data paths, or rule cases. |
| Large repo | Several focused walkthroughs | Each one explains a real behavior, not a module. |

Common names include `one-real-run.md`, `first-request.md`, `failure-case.md`, `rule-case.md`, and `data-to-output.md`. Choose names from behavior, not architecture.

### Glossary: `glossary.md`

Use this for names the reader will see repeatedly and may misunderstand without a project-specific meaning. Three columns only:

| Term | Plain meaning | Further reading |

**Plain meaning** carries the project-specific meaning in reader language. It can mention what the term is often confused with, but it should not become a code mapping. **Further reading** is optional: one inferred external URL for large generic concepts, one guide page, or `—`.

Prefer glossary rows for four term types:

| Term type | Include when |
| --- | --- |
| Project-special common word | A common word such as session, context, run, task, or memory has a specific boundary in this repo. |
| Confusable concept pair or family | Several terms look similar but mean different jobs, states, or phases in the repo. |
| External concept as used here | A broad term such as agent, benchmark, workspace, protocol, or provider needs the repo's local meaning before source details. |
| Lightweight repeated name | A repeated name helps the reader keep reading, but does not need its own module. |

Rules:

- Plain meaning must let the reader continue the guide without opening **Further reading**.
- At most one URL per row; mark `Inferred` / `推断（外部来源：…）`.
- Mechanism depth and necessary details belong in `modules/<concept>.md`.
- Do not add paths, functions, fields, commands, error codes, schemas, artifacts, package names, or file names only because they repeat. Put them in the owning module when they help understanding, or in `references/source-evidence.md` when they only prove a claim.
- Do not turn glossary into a link farm or duplicate module explanations.

### Flows: `flows.md`

Every non-Seed `repo-docs/` package must explain at least one real workflow. The worked example lives in `walkthroughs/one-real-run.md`; `flows.md` is the map for relationships between several meaningful workflows, runtime phases, state transitions, or output/evaluation paths. Do not create `flows.md` just to retell the same path as `one-real-run.md`. Use it for sequences:

- startup flow
- request/task flow
- data mutation flow
- evaluation or output flow
- error/debug flow

Prefer 6-10 steps per flow. Use Mermaid when a visual makes the sequence easier to understand. Keep each Mermaid diagram small, grounded in inspected source, and paired with plain-language prose. Keep `flows.md` as a map of relationships between walkthroughs, phases, states, or outputs; if it grows past roughly 120 lines, split detailed flows into `flows/<topic>.md` and link to them.

For seed projects, write flow content only as a planned flow with `Planned` / `计划中` status and verification checks beside the flow.

### Change log: `change-log.md`

Use this for past project work:

| Timestamp | Request | Actions | Verification | Result |
| --- | --- | --- | --- | --- |

Use `YYYY-MM-DD HH:MM TZ` rather than date-only headings. This keeps repeated same-day documentation changes distinguishable.

Record meaningful user requests and execution results when they change code, docs, data, experiments, or project understanding. Keep trivial chat in chat. Keep `change-log.md` recent and readable; when it grows past roughly 8 entries or 120 lines, move older entries to `change-log.archive.md` and link to the archive.

To make later syncs incremental, every sync or material question-driven patch should record **`Synced through <commit-sha>`** (or `同步至 <commit-sha>`) in the latest entry. The next sync scopes with `git diff <last-sha>..HEAD` instead of re-reading the whole repository. The validator warns when `change-log.md` has substance but no sync anchor, and when cited source paths changed after the last anchor (`--repo-root`).

### Module docs

Create or patch a module when a reader needs to understand a durable idea more deeply than the walkthrough can carry inline. A module is the knowledge page for that idea. It should be self-contained enough that the reader does not need a separate lookup reference to understand the mechanism.

First-principles module test:

```text
reader confusion -> core model -> representative case -> mechanism -> concrete details -> boundary -> verification
```

Module case gate: if the module explains a mechanism whose reader model depends on an input, state change, output, decision, selection, persistence, or boundary, include a compact case near the first mechanism explanation. The case should show the smallest truthful input, the action or transition, the resulting output/state/artifact, and one boundary or failure variant when source evidence exists. If a case would be misleading, unavailable, or unsafe to show, say that explicitly and point to the verification hook instead.

Before writing a module, identify the reader's actual gap. Common gaps are:

- They know the happy path but not why this mechanism exists.
- They see fields, commands, or tool calls but do not know what they mean.
- They confuse two similar concepts.
- They do not know where the system trusts or rejects input.
- They need a concrete normal case and failure/boundary case.
- They need to know which source or test would prove the model wrong.

Shape the module around the reader's question, not around source-tree order. A strong module usually contains:

1. The concept in one plain sentence.
2. Where the reader saw it in the walkthrough.
3. The pressure it handles: ambiguity, trust boundary, state handoff, invalid input, retrieval/ranking, evaluation, persistence, external dependency, or another real force.
4. The mechanism: what enters, what changes, what is stored or returned, and what downstream code relies on.
5. The important details: fields, commands, config keys, tool arguments, schemas, metrics, artifacts, call shapes, data shapes, or lifecycle steps that are necessary for understanding.
6. One representative case, preferably input -> output, before -> after, allowed vs denied, or normal plus boundary/failure variants when evidence exists.
7. The caveat: what is inferred, unsupported, intentionally out of scope, or easy to misread.
8. A verification hook: a test, command, artifact, source locator, or check that confirms the reader understood the mechanism.

Use tables, code blocks, and field lists inside modules when they make the concept clearer. Do not move details out merely because there are many identifiers or code-shaped values. Split only when one module is trying to explain two different concepts.

Code blocks in modules are not mini source dumps. Use one when the reader needs to see a call shape, data shape, branch, lifecycle handoff, command, or payload to understand the concept. Keep it tied to prose and evidence.

For seed projects, planned concepts belong in `README.md` or `change-log.md` until source evidence exists.

Before writing a module doc, hold this brief in mind:

| Brief field | Question |
| --- | --- |
| Reader question | What real confusion or decision brings the reader here? |
| Key insight | What should the reader understand after one minute? |
| Where this appears in a walkthrough | Which real command/request/task/failure makes this concept visible? |
| Important details | Which fields, commands, shapes, config, metrics, or artifacts are necessary to understand the concept? |
| Concrete example | What one input/output, before/after, allowed/denied, or normal/boundary case makes the concept easy to remember? |
| Source locator | Which source path proves the behavior? |
| Verification hook | What command, test, or observation confirms the reader understood the mechanism? |

Module docs should include examples when a concept would otherwise stay abstract. Use examples for:

- rule or permission concepts: allowed vs denied cases
- calculations or result values: inputs, denominator/base, and resulting value
- data contracts: valid vs invalid payloads
- public interfaces: realistic call/input and observable effect
- transformations: input -> output, before -> after, or raw -> normalized
- state and lifecycle: state before, triggering event, state after
- retrieval, ranking, routing, or selection: query/context -> chosen result and non-result
- failure modes: what fails, how it is surfaced, and what remains unchanged

Prefer one compact table or snippet over long prose. Examples must come from inspected project evidence. Use real project evidence when safe. If privacy, benchmark integrity, or access limits prevent showing actual values, use neutral placeholders and label them as placeholders; do not present them as real observations. Do not let a module pass with only categories, stages, or source names when the reader still needs to see a concrete input become an output.

### Cleanup / removal mode

Use this mode when the user asks to delete repo docs, remove generated docs content, or stop using `repo-docs` for the current project.

Do the cleanup as a documentation-state change:

1. Remove the generated `repo-docs/` package or the user-specified subset.
2. Remove root `AGENTS.md` / `CLAUDE.md` guide-maintenance rules that still point to the deleted docs.
3. Remove stale guide links from nearby docs when they no longer resolve.
4. Do not recreate replacement repo docs in the same turn unless the user explicitly requests a new guide.
5. Verify with a scoped search that stale guide paths and policies are gone.

If the user asks to delete only one page or one section, do not remove the whole package. Clean only the requested scope and repair links that would break.

### Agent instruction files

When `repo-docs/` is created or materially updated, search for existing project agent instruction Markdown and make it point future agents back to the guide.

Look for files such as `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/*.md`, or another nearby Markdown file whose filename or heading clearly says it is for coding agents. Patch the files that already govern this repo or package. If none exists, create `AGENTS.md`.

Keep the block short and operational:

- Where the living guide lives.
- That repo questions, behavior-changing edits, user uncertainty, stable project knowledge discovered or clarified in conversation, and knowledge about to be written to memory are explicit Sync triggers before the final response.
- That triggered work should run a foreground sync gate: use the `repo-docs` skill in Sync mode when available, with a manual equivalent when the skill is unavailable.
- That future repo questions and behavior-changing edits should check `repo-docs/` and patch stale pages before the final response when the current answer or edit would otherwise mislead.
- That broader, non-answer-critical guide work may be delegated to a background `repo-docs` sync agent when the platform supports a real tracked handoff.
- That stable project knowledge discovered or clarified during conversation must be added to the smallest owning guide page when it is missing from `repo-docs/`; a user does not need to explicitly ask for memory sync.
- Which repo-specific questions should refine it.
- Which docs to update before answering when guide content is missing or stale.
- Which changes deserve `change-log.md` entries.

Update existing agent instruction files in place. Do not duplicate the guide into them.

### References

Use `references/` only for fixed generated intermediate or audit artifacts:

- `references/source-evidence.md` records the evidence traversal, claim/evidence rows, caveats, falsifying checks, and source locators.
- `references/quality-review.md` checks whether the guide transfers a usable reader model and where risk remains.

Do not create any other `references/` pages. Schemas, contracts, metrics, tool parameters, task catalogs, scripts, artifacts, baseline methods, command lists, and exact-name lookup belong in the owning module when they matter to understanding. If a module becomes too large, split it by concept, not by "details versus explanation."

For `quality-review.md`, use an audit-note opening instead:

> This is an audit note. It checks whether the guide transfers a usable reader model and where risk remains.

References should optimize for auditability. Modules should optimize for understanding.
