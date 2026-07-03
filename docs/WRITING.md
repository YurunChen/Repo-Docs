# Repo-Docs Writing Rules

## Positioning

`repo-docs` is a Markdown documentation pack under `repo-docs/` in the repository. It explains the project in plain technical language, follows one real behavior end to end, deepens named concepts in `modules/`, and uses `references/` only for fixed generated artifacts: source evidence and optional quality review. The guide is maintained during coding conversations—not regenerated as a separate doc pass.

## Explanation Design

`repo-docs` should feel like a capable engineer explaining the repo at a whiteboard, then pointing to the exact code. The first job is understanding. The second job is verification. Evidence is the guardrail that keeps the easy explanation true; it is not the reader's first handle. Page ownership lives in [PAGE_RULES.md](PAGE_RULES.md); this file only governs how the explanation should sound and unfold.

A good guide lets a newcomer answer in about 15 minutes: what the repo is for, what one real run looks like, which ideas matter, how the important details work, and how to verify their understanding.

The style target is plain, alive, and technically sharp. Use Andrej Karpathy and Kaiming He as references for the feel: simple words, real mechanism, no pomp, no fake certainty, no long preamble. Explain the idea first. Then show the code.

OpenAI's Codex writing and Claude Code's best-practice docs show the pattern to copy. The opening says what changed in the work. The next section explains how the system actually runs. Verification is not decorative: logs, tests, citations, screenshots, and command output are how the reader knows what happened. Claude's docs also keep returning to one practical constraint at a time: give the agent a check, explore before coding, provide specific context, keep persistent instructions short. Use the same style here.

Anthropic's harness writeup is the closest model for long-form flow. It does not begin by cataloging components. It begins with a real problem, names the failure modes that kept showing up, introduces one mechanism to address them, reports what happened in runs, then admits where the mechanism still cost too much or missed bugs. Use that shape for repo docs whenever the reader needs to understand a system rather than look up a fact.

First-principles test: the guide is working when a newcomer can hold one real task in mind, explain why each phase exists, predict where a failure would surface, and run or inspect one check to verify the model. If a page is accurate but hard to understand, it has not met the bar yet.

Use Socratic interrogation as an internal modeling tool, not as a visible writing template. Before drafting and again before delivery, ask from the reader's side:

| Socratic question | What it should expose |
| --- | --- |
| What concrete situation is the reader in? | The user action, command, request, artifact, failure, or data record that makes the page necessary. |
| Why does this phase exist? | The pressure: ambiguity, validation, state handoff, trust boundary, expensive work, external failure, or another real force. |
| What would break if the repo skipped this step? | The failure, wrong output, lost state, invalid contract, or misleading result that makes the mechanism matter. |
| What concrete case would let the reader test the model? | The smallest real or clearly labeled input -> output, before -> after, allowed/denied, or normal/boundary example that makes the mechanism inspectable. |
| What evidence would prove this explanation wrong? | Source, test, config, data, artifact, or command output that must be inspected before the prose claims certainty. |
| Where do assumptions stop? | The boundary, caveat, fallback, unsupported path, or unknown that prevents overclaiming. |
| What would a careful newcomer ask next? | The next page, source-evidence audit, glossary row, verify command, or explicit out-of-scope note. |

Turn the answers into connected prose. Do not publish a Socratic Q&A unless the page is intentionally an FAQ or audit note. If a question has no inspected evidence, re-search the relevant code paths and inspect source, tests, config, data, commands, or artifacts. If evidence is still missing, mark the point as `Inferred` or `Unknown`, defer it explicitly, or leave it out.

Keep stable knowledge in the guide. Keep transient run state, one-off debugging notes, and chat history in chat unless the user explicitly asks to preserve them. Each sync may delete, merge, or shorten docs when that makes the reader's model cleaner.

Each page is an explanation unit answering one durable reader question. Module pages may include files, fields, commands, classes, schemas, call shapes, and artifacts when those details are necessary to understand the concept. Narrative pages carry connected prose split by story beats. For non-Seed repos, the first explanation unit is `walkthroughs/one-real-run.md`.

Use the discipline of a good engineering note while keeping the guide a living project document:

| Explanation move | How repo-docs should use it |
| --- | --- |
| Start with the thing the reader recognizes | Begin with a user action, command, request, artifact, failure, or data record. |
| Give the simple model | Say what is happening in normal technical language before using source names. |
| Name the pressure | Say why this phase exists: loose input, ambiguous output, state handoff, invalid data, external failure, expensive work, trust boundary, or another concrete force. |
| Show why it exists | Explain the design reason, constraint, tradeoff, or bug it avoids. Do not pretend you know the author's private intent. |
| Point to code only after the model lands | Source locators should confirm the explanation, not replace it. |
| End with action | Say what to inspect, what assumption the mechanism depends on, and how to verify understanding. |

When a section feels vague, rewrite it around one concrete design reason:

| Weak center | Better center |
| --- | --- |
| "Architecture overview" | "How a request becomes a written result." |
| "Module responsibilities" | "Where the handoff happens and what can break." |
| "Robust system design" | "What check catches a wrong output." |
| "Configuration surface" | "Which knob changes runtime behavior." |

The main document should orient the reader enough to choose the next useful page. Use Markdown as a clear technical note, not as a course UI or a compliance form.

## Writing Style

Write like a real person who understands the code.

The tone should be direct and calm. Short sentences are fine. A little rhythm is good. The page should sound like an engineer saying, "Here is the idea; here is where it happens; here is how you would check you understood it." It should not sound like an LLM trying to sound comprehensive.

"娓娓道来" means the explanation unfolds one reason at a time. It is not looseness, and it is not extra preamble. A strong section can often follow this path: observable situation, design reason, choice, concrete behavior, verification, limitation. If a section starts with a list of modules, it usually skipped the situation and reason.

Use this order at page and section level:

1. Conclusion: what the reader should understand.
2. Reason: why this part exists or why the reader should care.
3. Pressure: what concrete difficulty, ambiguity, trust boundary, or failure risk the mechanism handles.
4. Mechanism: what receives input, changes state, returns output, or protects an invariant.
5. Path: the actual code/data/config flow that proves it.
6. Implication: what assumption the mechanism depends on, how to verify it, or what breaks if the model is wrong.
7. Caveat: what is inferred, unknown, or intentionally out of scope.

For walkthrough steps, do not start the first paragraph with a function, class, method, or file path. Start with the human-observable phase or the system pressure. A sentence like "`send_message()` appends..." is usually a call-stack transcript; rewrite it as "At this point the system has enough context to ask the model, but the reply is still not safe to treat as edits."

For narrative pages, use paragraphs for reasoning. A good paragraph has one point, one reason, and a concrete hook into behavior or source. Use bullets and tables for comparison or lookup. Do not build the whole page out of bullets. Do not turn every walkthrough step into the same stack of `###` reader-state headings when prose and inline locator labels would keep continuity.

Do not treat long prose as the default shape. Prose explains why; structure shows what. When the reader needs to compare, inspect fields, follow a sequence, reproduce a command, or see a concrete input become an output, use a table, bullet list, numbered list, timeline, fenced block, or small diagram. If a paragraph is carrying several comparisons or transitions, the paragraph is doing display work that Markdown structure should do.

Use first-person only when the repo or project history actually supports it. Otherwise write from the project: "the runner does this because", "the current check catches", "this leaves". The style should feel human without inventing an authorial diary.

Do not let source confidence labels become the prose rhythm. Default evidence status belongs at the **end** of narrative pages; [QUALITY_RULES.md](QUALITY_RULES.md) defines the label family. Use local labels only where confidence changes or where a statement would be surprising without explicit evidence.

Concrete engineering prose is the default. This is the expression strategy behind the Anthropic harness post: it uses everyday engineering verbs, attaches judgments to observations, introduces terms after the reader has a concrete problem in mind, and keeps uncertainty visible. Apply that at sentence level:

| Weak expression | Better expression |
| --- | --- |
| "The system improves robustness." | "The parser rejects a missing `task_id` before the runner starts, so the writer never sees a half-built session." |
| "This module handles orchestration." | "This module starts the run, waits for each step to finish, and writes the artifact path that later checks read." |
| "The architecture is extensible." | "A new checker only needs to implement the same input and result shape; the runner already loops over that list." |
| "The project uses a checker." | "The generator writes the output. A separate checker opens it, runs the checks, and records the bugs it found." |

Use this as a sincerity test: after a paragraph, ask what the reader can now see, run, inspect, or doubt more precisely. If the answer is "they know the project is important", rewrite it. For a mechanism page, also ask whether a reader can name one representative input, output, and boundary condition without opening the source; if not, add or tighten the case.

Reading experience rules:

- Make every sentence carry a concrete point, caveat, observation, or transition.
- Prefer accurate small statements over broad statements such as "this is important" or "the system is robust".
- Replace abstract nouns with the action that happens in the repo when possible.
- When a sentence contains a value judgment, attach a visible reason or remove the judgment.
- Keep prose fluent. Avoid overusing dashes, quotation marks, parenthetical asides, and decorative emphasis.
- Avoid formulaic contrast patterns such as "not X but Y" and "not only X but also Y"; state the positive claim directly.
- Use examples from inspected source when a concept would otherwise feel abstract.
- Let the paragraph explain why the reader should care before introducing dense names.
- Prefer human words over framework words: say "what changes" before "state transition", say "where it starts" before "entrypoint architecture", say "what can break" before "risk surface".

Polished writing stays concrete. Replace inflated language with:

- statements about importance, impact, or "the evolving landscape" that the repo itself supports
- precise adjectives tied to an inspected constraint or behavior
- direct verbs such as "is", "reads", "writes", "checks", and "computes"
- lists that separate real concepts, states, or reader jobs
- paragraph endings that give a concrete next step or caveat
- headings followed by substance that advances the explanation
- current-state narration in current-state docs
- narrative transitions that carry reasoning: "this leaves one gap", "a natural next design is", "the current code confirms this by"

Prefer:

- exact actors and verbs: script reads config, runner builds session, writer saves output
- grounded caveats: "Unknown: no test currently covers this branch"
- compact examples tied to real code or data
- one short paragraph before a table when the table needs context
- fewer headings when the prose already carries the reader—but add a heading when it marks a real transition the reader needs
- one default evidence note per page or section, with local labels only for confidence changes
- a runnable check or inspectable artifact whenever the page asks the reader to trust a behavior

Good repo docs can have flow and texture while remaining inspectable. Trace elegant sentences to source evidence or mark them as inference.

Avoid these low-information patterns:

- starting a narrative page with a file list
- stating the project contribution before explaining the design reason that makes it plausible
- using "not X but Y" or "not only X, but also Y" as the main explanation
- turning a likely design reason into a statement that the original author definitely had that thought
- using vague praise such as "powerful", "important", "robust", or "novel" without code, data, test, artifact, or prior-work evidence
- repeating the same reader-state `###` subheadings under every walkthrough step when one `##` phase heading and connected prose would read better
- ending a walkthrough with separate `What changes`, `Change risk`, and `Verification` sections that repeat what the steps already said

## Evidence Discovery

Use repo evidence to answer the mental-model questions. These are common evidence sources:

| Evidence source | What it can prove |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `README*`, `CONTEXT.md` | Project contract, conventions, and current documentation policy. |
| Scripts, CLIs, package metadata, entrypoints | How a real run starts and what knobs are user-facing. |
| Runners, controllers, request handlers, sessions | Runtime flow, state lifecycle, and source paths that prove behavior. |
| Schemas, config, data files | Stable contracts, valid shapes, and behavior-defining inputs. |
| Tools, stores, rule/checker code, output writers | Side effects, validation, persistence, and produced artifacts. |
| Tests, sample outputs, logs, generated artifacts | Expected behavior, edge cases, and verification signals. |
| Existing docs and reports | Intent and historical caveats that still need source verification. |

Begin with the repo's purpose and one real execution path, then pull evidence where it explains that path or a reader decision.

When drafting reveals a weak claim, return to evidence discovery instead of smoothing the prose. Search for the owning code path, tests, schema, config, sample data, command output, or artifact that could prove or falsify the claim; update the evidence map before updating the narrative.
