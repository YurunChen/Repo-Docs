---
name: repo-docs-zh
description: Generate and maintain repo-docs with Chinese as the primary reader language while preserving source identifiers for lookup. Use when the user asks for Chinese repo docs, mentions repo-docs-zh, wants repo documentation in Chinese, or wants an existing repo-docs package localized for Chinese readers.
---

# Repo-Docs ZH

## Position

This is the Chinese-language overlay for `repo-docs`. Structure, page ownership, evidence rules, sync behavior, and validation come from `../repo-docs/SKILL.md`. This overlay only changes language and Chinese reader experience.

Before acting, read:

1. `../repo-docs/SKILL.md`
2. `../repo-docs/REFERENCE.md` as the topic router only when detailed rules are needed
3. The routed topic file only when needed
4. `../repo-docs/EXAMPLES.md` only for output shape or tone examples needed by the task

## Core Principle

Chinese repo-docs are not English docs translated line by line. They should rebuild the reader's conceptual handles in Chinese.

Chinese carries understanding: what this thing is, why it exists, what happens, what details matter, and how to check it. English identifiers locate the source: paths, commands, fields, API names, class/function names, metric names, package names, and dataset names.

`references/source-evidence.md` is still the fixed Build evidence base in Chinese packages. Write claims, caveats, and reader-facing notes in Chinese; keep paths, commands, fields, source identifiers, and exact evidence locators in their source form.

If writing exposes a weak claim or insufficient evidence, pause drafting and return to the project evidence. Re-inspect the relevant source path, tests, config, schema, data, command output, or artifact; if the evidence is still missing, label the claim as `推断` / `未确认`, defer it explicitly, or leave it out.

## Language Rules

- Use Chinese for titles, explanations, reading paths, examples, caveats, and change-log entries.
- Keep source identifiers exact in their source form: paths, commands, keys, API names, class/function names, metric names, error strings, package names, and dataset names.
- First introduce repeated project terms as `中文名（English term）` or `中文名（source identifier）`; later prefer the Chinese name.
- README route section heading is `## 阅读路径`.
- Glossary columns are exactly `术语 | 项目里的意思 | 延伸阅读`.
- Glossary rows should focus on four term types: project-special common words, confusable concept families, external terms as used in this repo, and lightweight repeated names that do not deserve a module.
- Narrative page evidence note: `证据状态：除特别标注外，本页基于当前源码已确认。`

## Chinese Handles And Source Locators

Use a Chinese reader handle before a source locator.

| Type | Use in Chinese docs |
| --- | --- |
| 读者句柄 | The narrative subject, such as “导入流程”, “会话层”, “结果汇总”, “运行脚本”. |
| 源码定位符 | Paths, functions, classes, fields, commands, artifact paths. Link directly with a Chinese label when one locator supports one claim. |
| 机制细节名 | Metrics, schema keys, tool parameters, artifact file names. Put them in the owning module when they help the reader understand the concept. |
| 外部术语 | Terms like benchmark, agent, workspace, protocol, memory. First mention gets a Chinese handle; later prefer Chinese when the term appears in the inspected repo. |

Default locator rule:

- Prefer a Chinese visible label that links to the source file over showing the raw path as visible text.
- Use inline code only for short identifiers that matter to the mechanism.
- Use `references/source-evidence.md` for grouped source evidence instead of creating separate source-map pages.
- Never make a long path the visible link text in narrative prose.

Good:

- 运行脚本负责选择运行模式和输入来源。
- 会话层先取上下文，再记录本轮真实产生的输出。
- 汇总器从最终状态读取完成情况和错误原因。

Bad:

- `packages/app/scripts/run_example.sh` 是入口。
- `Session.run_task(...)` handles context and scheduled observations.
- `ResultCollector.collect(...)` records output status.

## Readability Rules

- A paragraph should still make sense after removing backticked identifiers. If not, rewrite around Chinese actions first.
- Let Chinese prose carry the concept first, then use source identifiers where they make the mechanism inspectable.
- Give the reader a concrete handle first: a user action, visible state change, reader concept, or question they already have.
- 中文技术文档的真人感是具体、直接、敢标未确认；不要为了“有灵魂”加入第一人称、金句或情绪化评价。
- 成稿前做一次去 AI 表达：删掉“此外”“值得注意”“至关重要”“关键作用”“彰显”等空转词，少用破折号和粗体小标题。
- 避免让“不仅……而且……”或“不是……而是……”承担主解释；改成正面机制句。
- Put fields, command shapes, schemas, artifacts, and metrics in the owning module when they are needed to explain the concept.
- 讲一个机制时，如果读者理解它需要知道输入、状态变化、输出、决策或边界，就先问读者需要看到哪一个最小 case：输入是什么、动作或状态变化是什么、输出/产物是什么、边界或失败分支是什么。缺 case 时不要只补抽象解释；要补可读的代表性输入/输出形状，或明确说明为什么 case 会误导、缺证据或不宜展示。
- prose 负责解释为什么，结构负责展示是什么。读者需要比较、查字段、看顺序、复现命令或看到输入如何变输出时，优先用 table、列表、时间线、fenced block 或小图；不要把大段连续文字当成质量信号。
- 按读者问题选择展示策略，而不是按模板固定写法：因果解释用 prose；对比、before/after、字段查找用 table；命令、数据形状、调用形状用 fenced block；生命周期或顺序关系用短时间线 / 有序列表；分支、阶段、状态交接、多路径关系难以用 prose 承载时再用 Mermaid / flowchart。
- Flowcharts support prose; they do not replace it.
- A walkthrough step links to the module where a durable concept first matters.

## Page Shape Notes

- README: Chinese opening prose followed by a stable `## 阅读路径` reader-goal table. Use columns `读者目标 | 从这里开始 | 读完后获得什么`, including one row that routes evidence audit to `references/source-evidence.md`.
- Walkthrough: numbered `## Step N: 行为名` headings; prose explains mechanism; verification appears once near the end.
- Module: use Chinese concept headings shaped by the reader problem. Preserve the module job: concept first, representative case for mechanism-heavy pages, representative source locator later, onward route, and the evidence note. If the reader's easiest path is a question sequence, lifecycle, comparison, timeline, input/output case, or concept-first flow, use that structure.
- References: fixed generated artifacts only: `source-evidence.md` and, when needed, `quality-review.md`. Understanding and details belong in walkthroughs or modules.

## Agent Instruction Block

Use the main `repo-docs` English `Repo docs` block for `AGENTS.md` and other agent instruction Markdown. Chinese mode changes the reader-facing guide language; the agent instruction remains the main `repo-docs` block.

When a project uses Chinese reader-facing `repo-docs/`, add one short project-specific routing sentence immediately after the living-guide sentence:

```markdown
This repo's `repo-docs/` guide is reader-facing Chinese documentation. When updating reader-facing guide pages, use `repo-docs-zh` when available; keep Chinese reader handles in the prose and preserve exact source identifiers for lookup.
```

Do not translate the whole agent instruction block into Chinese. The extra sentence only tells future agents to apply this overlay for reader-facing guide pages.

## Build Delivery

After first build, reply in Chinese with:

1. what readers can now understand or follow;
2. where to start: `repo-docs/README.md` -> main walkthrough;
3. key pages and their jobs;
4. scope, uncovered areas, validator result, and root agent-file status.

Keep the reply short. Durable guide history belongs in `repo-docs/change-log.md`.
