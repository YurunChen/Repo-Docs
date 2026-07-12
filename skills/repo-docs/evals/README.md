# Repo-Docs Skill Evals

These evals are lightweight regression checks for the `repo-docs` skill rules. They do not score an LLM. They materialize small repo-docs fixtures in a temporary directory, run the bundled validator, and assert the rule text that controls trigger precision.

Run from the repository root:

```bash
python skills/repo-docs/evals/run_eval.py
```

## Cases

| Case | Expected artifacts | Automated assertions | Human check |
| --- | --- | --- | --- |
| `standard-build` | README, walkthrough, code map, module, source evidence, glossary, change log | Validator exits with 0 errors; no extra `references/` pages | The guide teaches behavior first, then maps in-scope source responsibilities. |
| `standard-code-map-required` | Standard fixture with `code-map.md` removed | Validator fails with a missing required file error | Standard packages always preserve the code-navigation layer. |
| `code-map-missing-directory-section` | Code map lists a directory without its detail section | Validator warns with the uncovered directory path | Every summarized source area gets a navigable responsibility section or split-page link. |
| `code-map-missing-code-table` | Directory section lacks the important-code table | Validator warns with the affected directory path | Folder purpose is followed by concrete code and symbol locations. |
| `code-map-missing-coverage-section` | Code map omits its closing coverage section | Validator warns instead of accepting incidental coverage words elsewhere | Scope and exclusions stay explicit. |
| `walkthrough-missing-code-map-route` | Standard walkthrough does not link onward to the code map | Validator fails with a routing error | The published reading order remains behavior first, code location second. |
| `lite-build` | README, walkthrough, source evidence, change log | Validator exits with 0 errors under `--lite`; no module directory required | Lite shape does not invent concept pages. |
| `seed-build` | README, change log, glossary | Validator exits with 0 errors under `--seed` | Planned facts are not described as implemented. |
| `sync-decision-rules` | Skill rule files | `none`, `answer-only`, `foreground patch`, and `background sync` appear in `SKILL.md`, `SYNC_RULES.md`, and root-agent rules | Ordinary repo questions have an answer-only path. |
| `answer-only-docs` | Skill rule files | Sync rules explicitly say ordinary repo questions are not automatic doc edits | The trigger policy will not surprise users with unnecessary patches. |
| `stable-module-gap` | Skill rule files | Stable understanding gaps route to add/refine/merge modules | Knowledge has one durable reader home. |
| `display-shape-router` | Skill rule files | Entry and page rules preserve prose/structure routing and the wall-of-text guard | Reader understanding drives tables, lists, timelines, code blocks, and prose. |
| `strict-references` | A fixture with an extra reference page | Validator fails with a fixed references-scope error | Contract/schema/catalogue content belongs in modules. |
| `code-heavy-opening` | A fixture with a code-name-heavy opening | Validator returns 0 errors and emits the opening-density warning | The warning is useful and low noise. |
| `module-missing-case` | A mechanism module with payload/state language but no representative case | Validator returns 0 errors and emits the module-case warning | Mechanism pages should show the smallest useful case, not only categories. |
| `zh-overlay` | Chinese Lite package | Validator exits with 0 errors under `--lite`; Chinese routes preserve English source identifiers | Chinese carries the mental model while source terms stay exact. |

## Notes

- Fixtures are encoded in `run_eval.py` and materialized under a temporary directory so they cannot dirty the repository.
- Public case studies remain useful examples, but these evals are the fast regression suite for skill behavior.
- Add a new eval whenever a rule change would otherwise rely on reviewer memory.
