# Case: Aider-AI/aider

This case applies the `repo-docs` build shape to [Aider-AI/aider](https://github.com/Aider-AI/aider), a popular terminal pair-programming assistant.

The generated pack follows one real behavior: a terminal CLI request starts Aider, builds a coder session, sends a user message, parses the model reply into edits, and then moves through commit, lint, command, and test handling when those settings are enabled.

Generated files:

- [README.md](generated/aider/repo-docs/README.md)
- [walkthroughs/one-real-run.md](generated/aider/repo-docs/walkthroughs/one-real-run.md)
- [code-map.md](generated/aider/repo-docs/code-map.md)
- [modules/session-assembly.md](generated/aider/repo-docs/modules/session-assembly.md)
- [modules/edit-lifecycle.md](generated/aider/repo-docs/modules/edit-lifecycle.md)
- [references/source-evidence.md](generated/aider/repo-docs/references/source-evidence.md)
- [references/quality-review.md](generated/aider/repo-docs/references/quality-review.md)
- [glossary.md](generated/aider/repo-docs/glossary.md)
- [change-log.md](generated/aider/repo-docs/change-log.md)

Evidence status: Confirmed from local Aider source inspection unless noted.
