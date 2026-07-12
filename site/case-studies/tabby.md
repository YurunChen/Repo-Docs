# Case: TabbyML/tabby

This case applies the `repo-docs` build shape to an inspected Tabby checkout, a self-hosted AI coding assistant.

The generated pack follows one real behavior: the server starts an Axum router, exposes `/v1/completions`, receives editor segments, chooses a prompt path, optionally gathers retrieval snippets, builds a model prompt, returns a completion response, and logs the event.

Generated files:

- [README.md](generated/tabby/repo-docs/README.md)
- [walkthroughs/one-real-run.md](generated/tabby/repo-docs/walkthroughs/one-real-run.md)
- [code-map.md](generated/tabby/repo-docs/code-map.md)
- [modules/completion-pipeline.md](generated/tabby/repo-docs/modules/completion-pipeline.md)
- [modules/retrieval-context.md](generated/tabby/repo-docs/modules/retrieval-context.md)
- [modules/completion-contract.md](generated/tabby/repo-docs/modules/completion-contract.md)
- [references/source-evidence.md](generated/tabby/repo-docs/references/source-evidence.md)
- [references/quality-review.md](generated/tabby/repo-docs/references/quality-review.md)
- [glossary.md](generated/tabby/repo-docs/glossary.md)
- [change-log.md](generated/tabby/repo-docs/change-log.md)

Evidence status: Confirmed from inspected working-tree source unless noted.
