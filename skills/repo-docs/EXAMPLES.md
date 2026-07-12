# Repo-Docs Examples

Default output shapes and finished-page tone targets.

**Canonical logic:** package shape and page ownership live in [SKILL.md](SKILL.md) and [PAGE_RULES.md](PAGE_RULES.md). Voice and explanation rhythm live in [WRITING.md](WRITING.md). This file only shows finished shapes.

See [Walkthrough Default](#walkthrough-default), [Walkthrough Understanding Example](#walkthrough-understanding-example), [Evidence Map Example](#evidence-map-example), [Quality Review Example](#quality-review-example), [Module caveat example](#module-caveat-example), [Build Delivery Example](#build-delivery-example), and [Tone Target](#tone-target-a-full-narrative-page-english).

## Standard Non-Seed Structure

```text
repo-docs/
  README.md
  walkthroughs/
    one-real-run.md
  code-map.md
  modules/
  references/
    source-evidence.md
  glossary.md
  change-log.md
```

Triggered pages such as more walkthroughs, `flows.md`, and `evidence-ledger.md` appear only when a reader problem needs them: multiple real behaviors, several cases, phase/state relationships, or a separate evidence table that would otherwise clutter the explanation path.

## Build Delivery Example

Use this as the tone target for the **user-facing reply** after Build—not as a page inside `repo-docs/`.

### Small or Lite package (compact reader goals)

````markdown
已在 `repo-docs/` 建好首版文档包。读者可以先跟通一条真实运行路径，再按需查概念或字段名，而不必先扫目录树。

**读者目标：**

| 读者目标 | 从这里开始 | 读完后获得什么 |
| --- | --- | --- |
| 快速理解主流程 | [一条真实路径](repo-docs/walkthroughs/one-real-run.md) | 输入如何进入系统、如何变成结果 |
| 审计事实依据 | [证据底座](repo-docs/references/source-evidence.md) | 源码、测试、配置、命令和边界证据 |
| 回到入口页 | [repo-docs/README.md](repo-docs/README.md) | 项目模型、范围和后续阅读路径 |

**本次包含：**
- 主 walkthrough：输入进入 → 规范化记录 → 结果写出
- 证据底座：`references/source-evidence.md`
- 根目录已新增 `AGENTS.md`，说明何时同步文档

**范围：** Lite 结构；尚无独立 concept 页。
**检查：** `validate_repo_docs.py` — 0 errors。
````

### Standard package with several pages (reader-goal table)

Use the same reader-goal shape as the README so the reader sees goals before files.

````markdown
`repo-docs/` is ready. You can follow one input from entry to written result, then drill into concepts and their details when needed.

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand the main behavior | [Follow one real run](repo-docs/walkthroughs/one-real-run.md) | The end-to-end behavior trace |
| Locate the implementation | [Use the code map](repo-docs/code-map.md) | Directory responsibilities, key files or symbols, and the main change points |
| Clarify the normalized record | [Read the concept model](repo-docs/modules/normalized-record.md) | Why later code reads a stable record, including its important fields |
| Audit the evidence base | [Check source evidence](repo-docs/references/source-evidence.md) | Source, tests, configs, commands, artifacts, caveats, and page consumers |
| Decode repeated terms | [Use the glossary](repo-docs/glossary.md) | Project meanings in one place |

**Scope:** Covers the inbox path only; admin CLI not documented separately.
**Checks:** validator 0 errors; created root `AGENTS.md`.
````

## README Skeleton

````markdown
# Project Name Repo Docs

This project [what it does in one or two sentences]. [Why that matters / what real behavior proves it.] Follow [one real run from input to output](walkthroughs/one-real-run.md) to see the behavior before the code names make sense. The concept pages explain important fields, commands, shapes, and caveats when those details matter.

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand the main behavior | [Follow one real run](walkthroughs/one-real-run.md) | A concrete input-to-output trace and the project model behind it |
| Locate the implementation | [Use the code map](code-map.md) | In-scope directory responsibilities, important code, tests, and likely change points |
| Clarify core concepts | [Open the concept pages](modules/) | Reader-facing explanations, important details, and examples for ideas introduced by the walkthrough |
| Audit the evidence base | [Check source evidence](references/source-evidence.md) | Source, tests, configs, commands, artifacts, caveats, and page consumers |
| Decode repeated terms | [Use the glossary](glossary.md) | Project-specific meanings in one place |

Evidence status: Confirmed unless noted.
````

README always carries this reader-goal table. Use rows that match the generated pages.

## Code Map Skeleton

Use this after the walkthrough has established the behavior. Keep the map scoped and navigational; modules remain the home for detailed mechanisms and representative cases.

````markdown
# Code Map

This map covers [declared first-party source scope]. Read [how one real request becomes a result](walkthroughs/one-real-run.md) first if the main behavior is not clear yet.

| Path | Responsibility | Key code | Connection to the main path |
| --- | --- | --- | --- |
| `src/input/` | Turns external input into the stable record used downstream. | `normalize.py`, `schema.py` | Owns the first handoff in the walkthrough. |
| `src/process/` | Applies the business steps to the stable record. | `steps.py:run_steps` | Produces the values passed to result writing. |
| `tests/` | Verifies the main behavior and its rejection boundary. | `test_pipeline.py` | Proves the full path and invalid-input case. |

## `src/input/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `src/input/normalize.py` | Converts raw input into the stable internal record. | `normalize_input()` | CLI and API entrypoints; verified by `tests/test_input_normalization.py`. |
| `src/input/schema.py` | Defines the fields later phases may trust. | `InputRecord` | Normalization and processing modules. |

## Coverage

Covered: first-party source used by the documented input-to-result path. Generated assets and vendored dependencies are summarized rather than listed file by file. The admin path is deferred because it does not participate in this workflow.

Read [why the normalized record exists](modules/normalized-record.md) for mechanism detail, or return to [the full runtime sequence](walkthroughs/one-real-run.md).

Evidence status: Confirmed unless noted.
````

## Walkthrough Default

Default shape for `walkthroughs/one-real-run.md`: connected prose, numbered steps, and the page ownership defined in [PAGE_RULES.md](PAGE_RULES.md).

````markdown
# [Human behavior title]

[Opening: the concrete scenario you are following, the first input, why this path has real pressure, what output or state counts as success, the reader model in one or two paragraphs, and optional links to concept pages you will need later.]

## Step 1: [first behavior]

[What this phase receives, why it needs to exist, what it changes, and what downstream code relies on. Write in normal prose with cause and effect. Weave paths and functions into sentences. When this phase introduces a durable concept, link to the matching module in the same paragraph. For example, link to why the normalized record exists if that concept is still fuzzy after this step.]

## Step 2: [next behavior]

[Connected prose for the next phase.]

[Closing: end state after the run, one verify command for the whole path, links to concept pages or source-evidence audit if still useful.]

```bash
pytest path/to/tests -q
```

Evidence status: Confirmed unless noted.
````

## Walkthrough Understanding Example

The walkthrough is an understanding path, not a call-stack transcript. Source names prove the model after the reader has a handle.

The opening should name the hard part before the steps begin:

````markdown
This walkthrough follows one terminal request: a user sends `--message`, the model replies, and Aider tries to turn that reply into checked source edits. The hard part is that a model reply is only text. Aider has to preserve the launch settings, parse the reply into a concrete edit format, reject or reflect malformed edits, and only then commit or run checks.
````

**Weak: technically true, hard to understand first**

````markdown
## Step 3: the coder sends a message

`send_message()` appends the user message to `cur_messages`, formats all messages, checks token limits, and calls `send()`.
````

**Better: pressure first, mechanism second, source after the model lands**

````markdown
## Step 3: the request becomes a model turn

At this point the system has enough context to ask the model, but the reply is still not safe to treat as edits. The coder first builds the message list, checks the token window, sends the request, and stores the reply so the next phase can either parse it into edits or reflect a format error back to the model. That boundary keeps model I/O separate from file writes.

The lifecycle lives in `aider/coders/base_coder.py:send_message`; edit parsing starts only after this phase has recorded the assistant reply.
````

The stronger version gives the reader a task, a pressure, a state change, and a consequence before it asks them to care about function names.

## Walkthrough Expanded Shape (Long Pages Only)

Use this only when the walkthrough is long (roughly past 120 lines) or one step needs a dense before/after table or several locators. Do not use it as the default for short or medium pages. Keep numbered `## Step N: [behavior]` headings; weave mechanism, paths, and checks into connected prose—do not stamp repeated reader-state `###` subheadings.

````markdown
## Step N: [human action or event]

[What the reader sees or does, in plain language. Then the mechanism in connected
prose—weave `path/to/file`, functions, and checks into sentences. If a before/after
record shape helps, place a small table inside the flow:]

| Before | After |
| --- | --- |
| ... | ... |

[Continue the causal chain. Link to `modules/<concept>.md` when a durable concept
first matters. Save page-end verification for the walkthrough close unless this
phase needs its own distinct check.]

```bash
pytest path/to/tests -q
```
````

## Module Doc Skeleton

Shape module headings from the concept and reader problem. This is one compact example, not a required template.

````markdown
# [Readable Concept]

## [Reader-facing concept question]

[Reader question or statement.] [Explain the concept without code names first. Say what confusion this page removes and where the reader saw the concept in the first real run.]

## [How the repo makes it concrete]

[Explain how this repo represents and uses the concept: structure, key APIs, source locator, then the smallest inspected snippet or command needed to make the mechanism concrete.]

```python
# Minimal usage example from inspected source
...
```

If edit order matters for understanding, say why here in one short caveat.

## [Where to go next]

Return to [the first real run](../walkthroughs/one-real-run.md) where this concept first appears. If the next concept matters, link it with a label that says what the reader will learn. For audit detail, link to [the source evidence](../references/source-evidence.md).

Evidence status: Confirmed unless noted.
````

## Evidence Map Example

Use this shape for `references/source-evidence.md` in every Build package. Create it as soon as the representative behavior is chosen, then update it during Pass 1, Pass 2, and any extra evidence pass.

````markdown
# Source Evidence For [Workflow]

This is audit material. Read [the walkthrough](../walkthroughs/one-real-run.md) first if the behavior is not clear yet.

Evidence was collected over commit `<sha>`.

Working behavior: [the chosen command, request, task, user action, failure, or data record].

## Evidence Traversal Log

| Pass | Purpose | Inspected evidence | What changed in the model |
| --- | --- | --- | --- |
| Pass 1 | Map the main path. | Entrypoint, input shape, main handoffs, output state. | Established how one observable request becomes a result. |
| Pass 2 | Socratic challenge and fill the model. | Validation, failure path, retries, config precedence, tests, adjacent modes, falsifying checks. | Added the hard part, boundary, reader follow-ups, caveats, and out-of-scope paths. |
| Pass 3 | Resolve a weak claim. | [Source/test/config/artifact inspected after drafting exposed a gap.] | Revised or downgraded the affected claim before narrative writing continued. |

Coverage note: this map checks adjacent paths that affect the main reader model. It does not trace unrelated UI, benchmark, migration, or admin paths.

| Claim | Evidence | Confidence | Caveat | Used by |
| --- | --- | --- | --- | --- |
| [Behavior claim in reader language.] | [source/test/config/artifact link] | Confirmed | [Scope or verification caveat.] | README, walkthrough |
| [Claim that could mislead if overbroad.] | [falsifying or boundary evidence] | Confirmed / Inferred | [What the guide answers, defers, or labels unknown.] | walkthrough, quality review |
| [Revised claim after a later inspection.] | [new evidence that changed the model] | Confirmed / Inferred | [Why the earlier wording was too broad.] | module, walkthrough |

Evidence status: Confirmed unless a row says otherwise.
````

## Quality Review Example

Use this for `references/quality-review.md` in case studies, generated examples, source-heavy packages, or handoff-sensitive builds. Keep it short; if the answer teaches new mechanism, move that explanation back into the walkthrough or module.

````markdown
# Quality Review For [Workflow] Guide

This is an audit note for the guide. It checks whether the guide transfers a usable reader model and whether the main claims are evidence-backed.

## Reader Simulation

| Reader question | Answer from the guide |
| --- | --- |
| What real path is followed? | [One command, request, task, user action, failure, or data record.] |
| What is hard or non-trivial? | [The pressure, stated without source names first.] |
| What changes at each phase? | [The remembered state, output, decision, or handoff.] |
| Where would I change this behavior? | [The directory, important file or symbol, and nearest verification point from `code-map.md`.] |
| Where do assumptions stop? | [A real boundary, failure, retry, validation, caveat, or out-of-scope path.] |
| What would prove this explanation wrong? | [The falsifying source, test, config, artifact, or missing evidence.] |
| What would a careful newcomer ask next? | [Next page, source evidence, glossary row, verify command, deferred topic, or unknown.] |
| How can I verify it? | [Evidence map, test, command, artifact, config, or source locator.] |

| Review question | Result | Evidence | Follow-up |
| --- | --- | --- | --- |
| Can a reader state the hard part in one sentence? | Yes / Mostly / No. | [page or evidence link] | [Next sync action.] |
| Does the evidence map prove at least two modeling passes? | Yes / No. | [Evidence Traversal Log](source-evidence.md#evidence-traversal-log) | [Update when scope changes.] |
| Does the guide answer the strongest likely follow-up? | Yes / Deferred / Unknown. | [page, source evidence, caveat, or missing evidence] | [Where to answer or label it.] |
| What remains out of scope or partially verified? | [Named adjacent paths or checks.] | [scope note or caveat] | [When to add another walkthrough.] |

Evidence status: Confirmed unless noted.
````

## Root AGENTS.md Skeleton

Create at the **repository root** when no existing project agent instruction Markdown governs the repo and you are adding or materially updating `repo-docs/`. If files such as `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, `GEMINI.md`, or `.cursor/rules/*.md` already govern the repo, patch those files instead of creating a second source of rules.

````markdown
# Agent Instructions

## Repo docs

The living project guide is in `repo-docs/`. Start with `repo-docs/README.md`; when `repo-docs/walkthroughs/one-real-run.md` exists, use it as the main behavior trace.

Repo-docs sync triggers before the final response: repo questions; architecture, onboarding, or "how does this work" answers; behavior-bearing code/config/data/script/test edits; user uncertainty or correction about stable project behavior; stable project knowledge discovered or clarified in conversation; and knowledge about to be written to memory.

When a trigger happens, run a foreground repo-docs sync gate before answering: use the `repo-docs` skill in Sync mode when available, or manually read the relevant guide pages, inspect current source, and decide `none`, `answer-only`, `foreground patch`, or `background sync`. Ordinary repo questions may be `answer-only` when the guide is current enough and the answer can cite inspected guide/source evidence. Patch the smallest owning guide page before the final response only when the current answer or edit would otherwise mislead, the guide says the opposite, or the missing stable knowledge is a small local patch.

If the needed guide work is broader and not required for the current answer to be correct, delegate it to a background `repo-docs` sync agent when the platform supports a real tracked handoff. The handoff must name the trigger, durable facts or changed source areas, candidate guide pages, verification to run, and the expected `repo-docs/change-log.md` update. If no background agent is available, answer from inspected source and mention the pending docs gap when it matters.

When behavior-bearing code, config, data, scripts, or tests change, compare the change with the guide before finishing unless the user asked not to touch docs. Record meaningful guide updates in `repo-docs/change-log.md` with verification and `Synced through <sha>` when git is available.
````

## Mini Style Example

Use this as the style target. It names a concrete behavior first, then introduces source names only after the reader has a simple model.

This is a fictional sample. In real repo docs, replace every path, function, field, command, test name, and expected output with inspected project evidence. Put the page-level evidence note at the end of each narrative page; add local `Confirmed` / `已确认` labels only when confidence differs nearby.

The style target is practical: say what changed in the work, explain the mechanism, give the check. This is closer to Codex and Claude Code docs than to an architecture survey.

For longer explanations, let the paragraph unfold like an engineering post: a real situation appears, the design reason becomes visible, the project makes one tradeoff, and the check shows whether it worked.

**Style target — architecture as behavior:**

> The first problem appears before processing starts: the user input is too loose for the runner to use directly. The repo handles that by turning the input into a stable task record. After that point, the runner and checker read the same contract, so a failure can usually be traced to either the normalized task or the check that consumed it.

Source locators follow once the reader has this model.

### Concrete Expression Example

**Checker as a second pass:**

> A generator can produce an output that looks finished while the main action is still broken. The checker gives the repo a second pass: it opens the result, performs the action a user would try, and records the first place the behavior diverges from the contract.

**Config as runtime choice:**

> The config changes which runner starts. If `mode` is set to `batch`, the CLI reads every task from the input file; if it is set to `single`, it reads one task id and stops after that run.

These read as truthful because they name an action, an observation, and the limit of the claim.

### README First Screen

````markdown
# Import Tool Repo Docs

This project turns an input file into a written result. The core idea is simple: raw input first becomes a normalized record. The runner reads that record, applies the configured steps, and writes the result.

Follow [one input from load to result](walkthroughs/one-real-run.md) for the full path. Field names and valid shapes are explained in [normalized records](modules/normalized-record.md).
````

### Walkthrough Step (Flat Default)

Use this inside a walkthrough `##` phase, not the expanded `###` template.

````markdown
## Step 1: input becomes a record

The system receives one input item and turns it into a record that later code can inspect. The input is whatever the caller provided; the record is the stable version inside the system. At this point, no result has been written. This step protects later code from raw input differences.

After normalization, the system holds a record with id, source, created time, and cleaned payload. Record shape is owned by `src/inputs/normalize.py` and `normalize_input(...)`; every later step trusts that output. If the record shape or why it exists is still fuzzy, read [normalized records](../modules/normalized-record.md).
````

### Module Concept Page (Flat Default)

````markdown
# Normalized records

Why does the repo create a normalized record before it runs the main logic? A normalized record is the stable handoff between input code and processing code. It keeps later logic from depending on raw file, request, or row formatting. You saw this in [one-real-run.md](../walkthroughs/one-real-run.md) when raw input became one record shape.

`normalize_input(...)` in `src/inputs/normalize.py` builds the record dict; `src/inputs/schema.py` defines the fields processing code reads. Callers pass raw input plus source metadata; the function returns a dict later steps can consume without knowing the original wire format.

```python
# From tests/test_input_normalization.py, representative call
record = normalize_input(source="upload", payload={"name": "  demo  "})
# record => {"id": "...", "source": "upload", "name": "demo", "created_at": ...}
```

Change field names or normalization rules in `src/inputs/normalize.py` and `src/inputs/schema.py` before touching downstream processing code. Later steps assume the normalized record shape.

Evidence status: Confirmed unless noted.
````

### Module Detail Section

````markdown
## The normalized record shape

The normalized record is the stable handoff between raw input handling and downstream processing. A reader needs the field shape here because the next phase assumes these names and meanings.

| Field | Meaning | Used by |
| --- | --- | --- |
| `id` | Stable record identifier | result writer |
| `source` | Input origin such as CLI, upload, or API | routing logic |
| `payload` | Cleaned input data | processing steps |
| `created_at` | Record creation time | audit or run output |

The rejection boundary is in `src/inputs/schema.py`: records without `id`, `source`, or `payload` are invalid before processing starts.

Evidence status: Confirmed unless noted.
````

### Glossary row

Three columns: **Term | Plain meaning | Further reading**. Use rows for project-special common words, confusable concept families, external terms as used here, and lightweight repeated names. Keep code out unless one lightweight pointer is needed; mechanism and important details belong in modules.

````markdown
| Term | Plain meaning | Further reading |
| --- | --- | --- |
| Normalized record | Stable handoff after input parsing. Later code reads this record, not the raw input. Often confused with the original file, request, or row. | — |
| OTLP | Trace export format this repo uses. It is different from Prometheus scraping. | Inferred — [OTLP spec](https://opentelemetry.io/docs/specs/otlp/) |
| Session | The active run state this repo carries between retrieval, model call, and result writing. It is not a login session. | [Session assembly](modules/session-assembly.md) |
````

### Module caveat example

When edit order or assumptions matter for **understanding** the mechanism, weave a short caveat into the module page—do not create a separate change-plan page.

````markdown
# Normalized records

A normalized record is the stable handoff between input code and processing code. Later steps read the record, not the raw input.

The conversion lives in `src/inputs/normalize.py` and `src/inputs/schema.py`. If you are tracing why a field is missing in output, confirm the record first; downstream code assumes normalization already happened.

```python
record = normalize_input(raw_input)
result = process_record(record)
```

You saw this handoff in [one-real-run.md](../walkthroughs/one-real-run.md) when raw input became a normalized record. Field names and valid shapes are part of [normalized records](../modules/normalized-record.md).

Evidence status: Confirmed unless noted.
````

## Chinese Full-Page Style Example

Use these as tone targets for `repo-docs-zh`. They are intentionally written as finished pages, not skeletons. The Chinese prose should build the reader's model first; source names appear only after the model lands, as locators or exact evidence.

### `walkthroughs/one-real-run.md`

Fictional tone target—not real project evidence. Replace paths, functions, fields, tests, and outputs with inspected evidence in real docs.

````markdown
# 一条真实路径：输入如何变成结果

这一页只跟一条输入走到底。这个项目的主要动作，是把原始输入变成稳定记录，再让处理代码读取这个记录并写出结果。路径可以记成三步：输入进入 → 生成记录 → 写出结果。若「规范化记录」这个概念还抽象，读完本页后看 [规范化记录](../modules/normalized-record.md)。

## 输入先变成记录

系统收到输入后，第一件事不是写结果，而是把它整理成记录。输入是入口，记录是交接物；只要记录形状稳定，后面的处理步骤就可以专心做自己的事，而不是处理输入来源的差异。这一步还没有产生结果，只是把后面步骤要读取的东西固定下来。

归一化之后，系统手里有的是带有 `id`、`source`、`payload`、`created_at` 的记录。记录形状由 `src/inputs/normalize.py` 里的 `normalize_input(...)` 负责；后面所有步骤都信任这一步的输出。字段名和合法形状放在 [规范化记录](../modules/normalized-record.md) 里解释。

## 处理步骤读取记录并写出结果

记录固定下来之后，处理代码才开始计算结果。它读的是记录字段，不再回头看原始输入。处理步骤在 `src/process/steps.py`。

跑下面命令可验证整条路径。

```bash
pytest tests/test_pipeline.py -q
```

证据状态：除特别标注外，本页基于当前源码已确认。
````

### `modules/normalized-record.md`

````markdown
# 规范化记录

为什么项目不直接拿原始输入做处理，而要先创建一个规范化记录？记录是输入代码和处理代码之间的交接物：它把后面需要的信息整理成稳定结构，让后续步骤只面对一套字段。记录是结果的输入，不是结果本身。在 [一条真实路径](../walkthroughs/one-real-run.md) 里，输入进入后先被整理成记录；那一步还没有写出结果。

`normalize_input(...)` 在 `src/inputs/normalize.py` 里把原始输入整理成记录 dict；字段定义在 `src/inputs/schema.py`。调用方传入 source、payload 等原始输入，返回供处理代码读取的稳定结构。

```python
# 来自 tests/test_input_normalization.py 的代表性用法
record = normalize_input(source="upload", payload={"name": "  demo  "})
# record => {"id": "...", "source": "upload", "name": "demo", "created_at": ...}
```

若你在追「为什么输出里缺某个字段」，先确认记录是否已包含该字段；后续处理代码默认规范化已在 `src/inputs/normalize.py` 和 `src/inputs/schema.py` 完成。

证据状态：除特别标注外，本页基于当前源码已确认。
````

## Explanation Pass Example

Use this as an internal coverage checklist, or render it when scoping which concepts still need a readable home.

| Reader moment | Reader concept | Owning module | Details to explain there | Verification |
| --- | --- | --- | --- | --- |
| User runs/imports/calls ... | How a run starts | `modules/entrypoint.md` if the walkthrough gets dense | command shape, config knobs, expected first output | `...` |
| System parses ... | How input becomes usable state | `modules/data-shape.md` if this concept needs explanation | valid/invalid shapes, required fields, rejection boundary | `...` |
| System writes ... | What artifact the reader can inspect | `modules/output.md` if output behavior is non-obvious | artifact names, contents, lifecycle, caveats | `...` |

## Markdown Display Patterns

- Each durable fact lives in one best home; other pages link to it.
- Walkthrough: numbered `## Step N: [behavior]` headings; link to the matching `modules/<concept>.md` in the step where that concept appears; add a small flowchart when branches are hard to follow in prose alone; one verify block at page end.
- README: opening prose followed by a stable `## Reader Routes` table with reader goals, links, and payoffs, including a source-evidence audit row.
- Code map: scoped directory table followed by important-file tables, explicit exclusions, and links back to the walkthrough or deeper modules.
- Module: concept-shaped H2 sections; include necessary details, representative snippets, source locators, examples, and caveats where they clarify understanding.
- References: fixed generated artifacts only: source evidence and optional quality review.
- Mermaid and tables support prose; the paragraph still carries the reasoning. Use a flowchart when it teaches the model, not when it only repeats the file tree.
- Every behavior claim points to a test, command, artifact, schema, or source locator.

## Relationship Map Trigger Example

Create `flows.md` only when the reader needs to compare several paths or states:

- startup flow vs request flow
- success path vs failure path
- input path vs output path
- state before feedback vs state after feedback

Do not create `flows.md` when `one-real-run.md` already explains the only meaningful path.

## Voice: From AI-Tell To Human Narration

These pairs apply the writing standard. The "before" lines are technically correct but read like a generated report; the "after" lines read like a maintainer thinking out loud while showing you the code. Use them as tone targets, not as text to copy.

**Broad praise to a concrete statement**
- Before: The pipeline is a powerful and robust system that seamlessly handles incoming events.
- After: Every incoming event goes through the same three steps, so a malformed payload fails in one place instead of halfway down the pipeline.

**"Not X but Y" to a direct positive statement**
- Before: This is not a queue but a log; consumers do not pop items but read by offset.
- After: Consumers read by offset and the log keeps the item, so two consumers can read the same record without racing.

**File index to behavior with reasoning**
- Before: `router.py` routes requests, `handler.py` handles them, and `store.py` stores results.
- After: A request lands in the router, which picks a handler by path; the handler does the work and hands the result to the store. When a route returns 404, the router is the first place to look, because it chooses the handler before any handler runs.

**Clipped facts to narration with a transition**
- Before: Validation runs first. Then normalization. Then processing. Then write.
- After: Validation runs first so the rest of the chain can assume a well-formed input. Normalization then collapses the format variants into one shape, which keeps the processing step short: it only ever sees normalized fields.

**Bare locator to an articulated locator**
- Before: Result building is in `result.py`.
- After: Result building lives in `result.py:build_result`, where the normalized record and output fields meet; if those two disagree, every downstream report reads the wrong value even when the API returns 200.

## Tone Target: A Full Narrative Page (English)

Default walkthrough shape. Headings name behavior phases; paths and checks live in prose.

````markdown
# How an input becomes a result

An input arrives, and a moment later the system has written a result. This page follows one input from arrival to output. The system turns raw input into a normalized record, runs processing steps on that record, and stores the result. If [result assembly](../modules/result-assembly.md) is still fuzzy, read that concept page after this walkthrough.

## The input becomes a record

Raw input is whatever the caller provided. The system converts it into one normalized record so everything downstream shares one shape. After this step, no later code reads the raw input again; a field missing here is missing for every step that follows.

Conversion lives in `ingest/normalize.py:to_record`; that is where the input becomes the single record shape processing code reads.

## The record runs through the steps

Each step adds or checks one part of the result. The writer only receives the normalized record and step outputs, so output formatting stays separate from input parsing. Steps live in `process/steps.py`; result assembly is `results/write.py:build_result`.

After the run, the system holds one result artifact for downstream readers. Verify the full path:

```bash
pytest tests/test_pipeline.py -q
```

If edit order matters: say why in the module paragraph (for example, normalize before processing).

Evidence status: Confirmed unless noted.
````
