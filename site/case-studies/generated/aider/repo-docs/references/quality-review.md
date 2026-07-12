# Quality Review

## Reader Simulation

| Reader question | Answer from the guide |
| --- | --- |
| What real path is followed? | A terminal `aider` session creates a configured `Coder`, sends one user message, parses a diff-style SEARCH/REPLACE reply, checks file authority and dirty state, writes the edit, and optionally commits/lints/tests. |
| What is hard or non-trivial? | Aider must keep model output under user and repo control: parse before writing, ask before expanding edit scope, protect dirty work, reflect malformed edits, and avoid committing unrelated dirty files. |
| What changes at each phase? | CLI state becomes session policy; a user message becomes provider messages; provider output becomes `partial_response_content`; parsed edits become authorized file writes; written files become optional commits and lint/test feedback. |
| Where would I change this behavior? | [`code-map.md`](../code-map.md) routes startup and session policy to `aider/`, edit gating to `aider/coders/`, and focused verification to `tests/basic/`. |
| Where do assumptions stop? | The guide does not trace GUI, watch mode, model registry internals, repo-map ranking, voice, browser, or architect/editor mode. It also does not claim provider behavior because tests stub `coder.send`. |
| What would prove this explanation wrong? | The focused edit tests would fail, especially successful diff application, dry-run no-write behavior, dirty target pre-commit, or excluding unrelated dirty files from Aider edit commits. |
| What would a careful newcomer ask next? | How model defaults choose an edit format, how repo-map context is ranked, and how architect mode delegates to editor coders. Those are deferred as separate walkthroughs. |
| How can I verify it? | Run the focused pytest commands in `references/source-evidence.md`, then run the repo-docs validator. |

## Review Table

| Review question | Result | Evidence | Follow-up |
| --- | --- | --- | --- |
| Can a reader state the hard part in one sentence? | Yes. The README and walkthrough both state that Aider treats model output as a proposal that must pass parse, permission, dirty-work, and verification gates. | [`README.md`](../README.md), [`walkthroughs/one-real-run.md`](../walkthroughs/one-real-run.md) | None for this scope. |
| Can the walkthrough explain the flow if source links are hidden? | Mostly yes. Each step begins with behavior and reason before source anchors. | [`walkthroughs/one-real-run.md`](../walkthroughs/one-real-run.md) | If the guide expands to model selection, add a second walkthrough rather than overloading this one. |
| Is there a real boundary or failure path? | Yes. Non-matching SEARCH blocks become reflected feedback; dry-run preserves files. | [`modules/edit-lifecycle.md`](../modules/edit-lifecycle.md), [`references/source-evidence.md`](source-evidence.md) | Add a dedicated failed-edit walkthrough only if future readers ask about reflection/debugging. |
| Are claims backed by current source or tests? | Yes for the scoped path. | [`references/source-evidence.md`](source-evidence.md) | Provider behavior remains intentionally unverified. |
| Does the evidence map show two passes and adjacent paths? | Yes. Pass 1 maps the path; Pass 2 records boundaries and tests; coverage notes list adjacent untraced surfaces. | [`references/source-evidence.md#evidence-traversal-log`](source-evidence.md#evidence-traversal-log), [`references/source-evidence.md#coverage-notes`](source-evidence.md#coverage-notes) | None. |
| What residual risk remains? | Line anchors may drift as source changes, and the guide only covers the default CLI edit lifecycle. | Current source inspection and scoped exclusions. | Future behavior-changing edits should update the smallest owning guide page and change log. |

Evidence status: Confirmed unless noted.
