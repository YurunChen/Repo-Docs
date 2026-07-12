#!/usr/bin/env python3
"""Lightweight regression evals for the repo-docs skill."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_repo_docs.py"


STANDARD_FILES = {
    "README.md": """# Widget Runner Guide

Widget Runner turns one request into a saved report. The first path follows a user asking the CLI to check a widget order, because that path shows input validation, state handoff, and the report artifact.

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand the main run | [Follow the order check](walkthroughs/one-real-run.md) | How the request becomes a report. |
| Locate the implementation | [Use the code map](code-map.md) | Directory responsibilities, key files, and the main change points. |
| Understand validation | [Read the validation module](modules/order-validation.md) | Why invalid orders stop before report writing. |
| Audit evidence | [Check source evidence](references/source-evidence.md) | Source, tests, commands, artifacts, caveats, and page consumers. |

Evidence status: Confirmed unless noted.
""",
    "code-map.md": """# Code Map

Use this page after the walkthrough when you know the order-check behavior and need to locate its implementation. It maps the documented source scope, not every generated or unrelated file in the repository.

| Path | Responsibility | Key code | Connection to the main path |
| --- | --- | --- | --- |
| `src/` | Implements order validation and report writing. | `orders.py`, `reports.py` | Receives the CLI payload and produces the report. |
| `tests/` | Proves accepted and rejected order behavior. | `test_orders.py` | Verifies the guard and output artifact. |

## `src/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `src/orders.py` | Rejects empty orders before state changes. | `OrderValidator` | The CLI order-check path. |
| `src/reports.py` | Writes accepted orders to the report artifact. | `write_report()` | The checked-order result. |

`OrderValidator` is a source locator for this map, not a project concept for the glossary.

## `tests/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `tests/test_orders.py` | Verifies accepted and rejected orders. | `test_empty_order` | The order-check behavior and report boundary. |

## Coverage

Covered: the first-party `src/` implementation and `tests/` verification areas for the order-check path. Generated reports and the unrelated export mode are excluded.

Read [why empty orders stop before report writing](modules/order-validation.md), or return to [how one order becomes a report](walkthroughs/one-real-run.md).

Evidence status: Confirmed unless noted.
""",
    "walkthroughs/one-real-run.md": """# One Real Run

Scenario: a user runs the order check command with one order payload. The input is an order id and item count. The hard part is that the runner must reject empty orders before writing a report. Success is a report artifact that records accepted orders only.

## Step 1: The request becomes a checked order

The run starts with a user-visible command and turns the payload into a checked order. This phase exists because an empty order would make the report look successful while carrying no item data. The guard in `src/orders.py` rejects that boundary before writing.

## Step 2: The checked order becomes a report

After validation, the writer stores the report path for downstream checks. The important state change is that accepted item counts become report rows, while invalid orders leave no artifact.

## Verification

Run `python -m pytest tests/test_orders.py` and inspect `reports/order.txt`.

Use [the code map to locate the implementation](../code-map.md), read [the validation concept](../modules/order-validation.md), or audit [source evidence](../references/source-evidence.md).

Evidence status: Confirmed unless noted.
""",
    "modules/order-validation.md": """# Order Validation

Order validation is the rule that stops an empty order before report writing.

The walkthrough first uses it when the incoming payload needs a trustworthy item count. The pressure is simple: report rows should only describe accepted orders. The guard lives in `src/orders.py`.

| Case | Result |
| --- | --- |
| `item_count > 0` | report can be written |
| `item_count = 0` | validation error |

```bash
python -m pytest tests/test_orders.py
```

Return to [the run](../walkthroughs/one-real-run.md). Audit [source evidence](../references/source-evidence.md).

Evidence status: Confirmed unless noted.
""",
    "references/source-evidence.md": """# Source Evidence

## Evidence Traversal Log

| Pass | Purpose | Inspected evidence | What changed in the model |
| --- | --- | --- | --- |
| Pass 1 | Main path | `src/orders.py`, `src/reports.py` | The request becomes a checked order before report writing. |
| Pass 2 | Challenge and fill | `tests/test_orders.py`, sample report output | Empty orders are the boundary that would falsify a happy-path-only explanation. |

Coverage: CLI order checking and report writing are covered. The alternate export mode is out of scope for this guide.

Falsifying check: if `tests/test_orders.py` allows zero-item orders to write a report, this explanation is wrong.

Next reader question: how report formatting works. That is deferred until formatting becomes part of the main behavior.

| Claim | Evidence | Confidence | Caveat | Used by |
| --- | --- | --- | --- | --- |
| Empty orders stop before report writing. | `tests/test_orders.py` | Confirmed | Formatting is out of scope. | walkthrough, code map, module |
""",
    "glossary.md": """# Glossary

| Term | Plain meaning | Further reading |
| --- | --- | --- |
| Order validation | The rule that rejects empty orders before a report is written. | [Order validation](modules/order-validation.md) |
""",
    "change-log.md": """# Change Log

| Timestamp | Request | Actions | Verification | Result |
| --- | --- | --- | --- | --- |
| 2026-07-02 10:00 CST | Build eval fixture | Added guide pages for Widget Runner. | Validator fixture. Synced through 0000000 | Ready. |
""",
}


LITE_FILES = {
    key: value
    for key, value in STANDARD_FILES.items()
    if key
    in {
        "README.md",
        "walkthroughs/one-real-run.md",
        "references/source-evidence.md",
        "change-log.md",
    }
}
LITE_FILES["README.md"] = """# Widget Runner Lite Guide

Widget Runner turns one request into a saved report. This Lite guide follows the order check path because the project has one small concept surface and does not need a separate module.

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand the main run | [Follow the order check](walkthroughs/one-real-run.md) | How the request becomes a report. |
| Audit evidence | [Check source evidence](references/source-evidence.md) | Source, tests, commands, artifacts, caveats, and page consumers. |

Evidence status: Confirmed unless noted.
"""
LITE_FILES["walkthroughs/one-real-run.md"] = """# One Real Run

Scenario: a user runs the order check command with one order payload. The input is an order id and item count. The hard part is that the runner must reject empty orders before writing a report. Success is a report artifact that records accepted orders only.

## Step 1: The request becomes a checked order

The run starts with a user-visible command and turns the payload into a checked order. This phase exists because an empty order would make the report look successful while carrying no item data. The guard in `src/orders.py` rejects that boundary before writing.

## Step 2: The checked order becomes a report

After validation, the writer stores the report path for downstream checks. The important state change is that accepted item counts become report rows, while invalid orders leave no artifact.

## Verification

Run `python -m pytest tests/test_orders.py` and inspect `reports/order.txt`.

Audit [source evidence](../references/source-evidence.md).

Evidence status: Confirmed unless noted.
"""


SEED_FILES = {
    "README.md": """# Seed Project Guide

This project is still a seed. Confirmed: the repository has a README. Planned: the first runnable path will turn one request into one checked output. Unknown: the final artifact shape.
""",
    "glossary.md": """# Glossary

| Term | Plain meaning | Further reading |
| --- | --- | --- |
| Seed project | A project whose real source/runtime contract is not implemented yet. | — |
""",
    "change-log.md": """# Change Log

| Timestamp | Request | Actions | Verification | Result |
| --- | --- | --- | --- | --- |
| 2026-07-02 10:00 CST | Seed eval fixture | Recorded confirmed, planned, and unknown facts. | Validator fixture. | Ready. |
""",
}


ZH_LITE_FILES = {
    "README.md": """# Widget Runner 中文指南

Widget Runner 会把一次请求变成一份可检查的报告。首读路径跟随一次订单检查，因为它能显示输入校验、状态交接和报告产物。

## 阅读路径

| 读者目标 | 从这里开始 | 读完后获得什么 |
| --- | --- | --- |
| 理解主流程 | [跟随订单检查](walkthroughs/one-real-run.md) | 请求如何变成报告。 |
| 审计证据 | [查看证据底座](references/source-evidence.md) | 源码、测试、命令、产物和边界证据。 |

证据状态：除特别标注外，本页基于当前源码已确认。
""",
    "walkthroughs/one-real-run.md": """# 一次真实运行

场景：用户运行订单检查命令，并传入一个订单 payload。输入是订单 id 和 item count。难点是运行器必须在写报告前拒绝空订单。成功输出是一份只记录有效订单的报告。

## Step 1: 请求变成已检查订单

系统先把用户可见的命令转换成已检查订单。这个阶段存在，是因为空订单会让报告看起来成功，但没有真实 item 数据。边界由 `src/orders.py` 里的校验保护。

## Step 2: 已检查订单变成报告

通过校验后，写入器保存报告路径，供后续检查读取。关键变化是有效 item count 进入报告行，无效订单不会留下产物。

## 验证方法

运行 `python -m pytest tests/test_orders.py`，再检查 `reports/order.txt`。

审计细节见 [证据底座](../references/source-evidence.md)。

证据状态：除特别标注外，本页基于当前源码已确认。
""",
    "references/source-evidence.md": """# 证据底座

## Evidence Traversal Log

| Pass | Purpose | Inspected evidence | What changed in the model |
| --- | --- | --- | --- |
| Pass 1 | Main path | `src/orders.py`, `src/reports.py` | 请求会先变成已检查订单。 |
| Pass 2 | Challenge and fill | `tests/test_orders.py` | 空订单是边界路径。 |

覆盖范围：覆盖订单检查和报告写入。导出模式不在本指南范围内。

证伪检查：如果 `tests/test_orders.py` 允许空订单写报告，本解释就是错误的。

下一问：报告格式如何组成；当前暂缓。

| Claim | Evidence | Confidence | Caveat | Used by |
| --- | --- | --- | --- | --- |
| 空订单不会写报告。 | `tests/test_orders.py` | Confirmed | 报告格式不在范围内。 | walkthrough |
""",
    "change-log.md": """# 变更记录

| Timestamp | Request | Actions | Verification | Result |
| --- | --- | --- | --- | --- |
| 2026-07-02 10:00 CST | 中文 eval fixture | 添加中文 Lite 指南。 | Validator fixture. Synced through 0000000 | Ready. |
""",
}


def write_files(root: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def run_validator(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_fixture(
    name: str,
    files: dict[str, str],
    *args: str,
    expect_code: int = 0,
    contains: str | None = None,
    not_contains: str | None = None,
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"repo-docs-eval-{name}-") as tmp:
        root = Path(tmp) / "repo-docs"
        write_files(root, files)
        result = run_validator(root, *args)
        output = result.stdout + result.stderr
        expect(result.returncode == expect_code, f"{name}: expected exit {expect_code}, got {result.returncode}\n{output}")
        if contains:
            expect(contains in output, f"{name}: expected output to contain {contains!r}\n{output}")
        if not_contains:
            expect(not_contains not in output, f"{name}: expected output not to contain {not_contains!r}\n{output}")


def assert_rule_text() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    sync = (SKILL_ROOT / "SYNC_RULES.md").read_text(encoding="utf-8")
    root_rules = (SKILL_ROOT / "ROOT_AGENT_RULES.md").read_text(encoding="utf-8")
    page_rules = (SKILL_ROOT / "PAGE_RULES.md").read_text(encoding="utf-8")
    reference = (SKILL_ROOT / "REFERENCE.md").read_text(encoding="utf-8")
    zh = (SKILL_ROOT.parent / "repo-docs-zh" / "SKILL.md").read_text(encoding="utf-8")

    for decision in ("none", "answer-only", "foreground patch", "background sync"):
        expect(decision in skill, f"SKILL.md missing sync decision {decision!r}")
        expect(decision in sync, f"SYNC_RULES.md missing sync decision {decision!r}")
        expect(decision in root_rules, f"ROOT_AGENT_RULES.md missing sync decision {decision!r}")

    expect("Ordinary repo questions are not automatic doc edits" in sync, "SYNC_RULES.md must protect answer-only repo questions")
    expect("`code-map.md`" in sync, "SYNC_RULES.md must keep source-location navigation current")
    expect("Representative case before abstraction" in skill, "SKILL.md must include the representative case law")
    expect("Shape follows reader need" in skill, "SKILL.md must include the display-shape law")
    expect("`code-map.md`" in skill, "SKILL.md must define the standard code-map page")
    expect("code location lives in `code-map.md`" in skill, "SKILL.md must give code location one durable home")
    expect("Module case gate" in page_rules, "PAGE_RULES.md must define the module case gate")
    expect("Code Map Gate" in page_rules, "PAGE_RULES.md must define when and how to build the code map")
    expect("Behavior first, code map second" in page_rules, "PAGE_RULES.md must keep code navigation after the behavior model")
    expect("Display shape router" in page_rules, "PAGE_RULES.md must include the display shape router")
    expect("Wall-of-text guard" in page_rules, "PAGE_RULES.md must include the wall-of-text guard")
    expect("adding a focused module, refining the owning module, or merging overlapping modules" in page_rules, "PAGE_RULES.md must route stable gaps to module add/refine/merge")
    expect("Do not create any other `references/` pages" in page_rules, "PAGE_RULES.md must forbid extra references pages")
    for term_type in (
        "Project-special common word",
        "Confusable concept pair or family",
        "External concept as used here",
        "Lightweight repeated name",
    ):
        expect(term_type in page_rules, f"PAGE_RULES.md missing glossary term type {term_type!r}")
    expect("ROOT_AGENT_RULES.md" in reference, "REFERENCE.md must route root agent rules")
    expect("fixed generated artifacts" in zh, "repo-docs-zh overlay must use fixed references wording")
    expect("project-special common words" in zh, "repo-docs-zh overlay must describe glossary term categories")
    expect("代码地图" in zh, "repo-docs-zh overlay must define the Chinese code-map experience")


def main() -> int:
    validate_fixture(
        "standard-build",
        STANDARD_FILES,
        not_contains="glossary.md has no entry for `OrderValidator`",
    )
    validate_fixture("lite-build", LITE_FILES, "--lite")
    validate_fixture("seed-build", SEED_FILES, "--seed")
    validate_fixture("zh-overlay", ZH_LITE_FILES, "--lite")

    missing_code_map = dict(STANDARD_FILES)
    missing_code_map.pop("code-map.md")
    validate_fixture(
        "standard-code-map-required",
        missing_code_map,
        expect_code=1,
        contains="Missing required file: code-map.md",
    )

    missing_directory_section = dict(STANDARD_FILES)
    missing_directory_section["code-map.md"] = missing_directory_section["code-map.md"].replace(
        """## `tests/`

| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `tests/test_orders.py` | Verifies accepted and rejected orders. | `test_empty_order` | The order-check behavior and report boundary. |

""",
        "",
    )
    validate_fixture(
        "code-map-missing-directory-section",
        missing_directory_section,
        expect_code=0,
        contains="missing per-directory sections for: tests/",
    )

    missing_code_table = dict(STANDARD_FILES)
    missing_code_table["code-map.md"] = missing_code_table["code-map.md"].replace(
        """| Important code | Function | Key symbols | Called by / used by |
| --- | --- | --- | --- |
| `tests/test_orders.py` | Verifies accepted and rejected orders. | `test_empty_order` | The order-check behavior and report boundary. |
""",
        "Tests for this area are described elsewhere.\n",
        1,
    )
    validate_fixture(
        "code-map-missing-code-table",
        missing_code_table,
        expect_code=0,
        contains="directory sections without an important-code table: tests/",
    )

    missing_coverage_section = dict(STANDARD_FILES)
    missing_coverage_section["code-map.md"] = missing_coverage_section["code-map.md"].replace(
        """## Coverage

Covered: the first-party `src/` implementation and `tests/` verification areas for the order-check path. Generated reports and the unrelated export mode are excluded.

""",
        "",
    )
    validate_fixture(
        "code-map-missing-coverage-section",
        missing_coverage_section,
        expect_code=0,
        contains="no explicit `## Coverage` section",
    )

    walkthrough_missing_code_map = dict(STANDARD_FILES)
    walkthrough_missing_code_map["walkthroughs/one-real-run.md"] = walkthrough_missing_code_map[
        "walkthroughs/one-real-run.md"
    ].replace("Use [the code map to locate the implementation](../code-map.md), ", "")
    validate_fixture(
        "walkthrough-missing-code-map-route",
        walkthrough_missing_code_map,
        expect_code=1,
        contains="Main walkthrough should route onward to code-map.md",
    )

    bad_reference = dict(STANDARD_FILES)
    bad_reference["references/schema-catalog.md"] = "# Schema Catalog\n\nThis lookup page should be a module instead.\n"
    validate_fixture(
        "strict-references",
        bad_reference,
        expect_code=1,
        contains="outside the fixed references scope",
    )

    code_heavy = dict(LITE_FILES)
    code_heavy["README.md"] = """# Code Heavy Guide

`src/app.py` calls `build_index()` before `src/store.py` reads `config.yaml`, then `run_task()` writes `out/result.json` and `check_result()` compares `tests/test_app.py`.

## Reader Routes

| Reader goal | Start here | What this page gives you |
| --- | --- | --- |
| Understand the run | [Follow the run](walkthroughs/one-real-run.md) | The task flow. |
| Audit evidence | [Check source evidence](references/source-evidence.md) | Source, tests, commands, artifacts, caveats, and page consumers. |
"""
    validate_fixture(
        "code-heavy-opening",
        code_heavy,
        "--lite",
        expect_code=0,
        contains="opening has many code-shaped names",
    )

    missing_case = dict(STANDARD_FILES)
    missing_case["modules/order-validation.md"] = """# Order Validation

Order validation is the contract that decides whether a payload can change report state. The route depends on item count and the writer depends on the decision.

Read [the run](../walkthroughs/one-real-run.md) or audit [source evidence](../references/source-evidence.md).

Evidence status: Confirmed unless noted.
"""
    validate_fixture(
        "module-missing-case",
        missing_case,
        expect_code=0,
        contains="no obvious representative case",
    )

    assert_rule_text()
    print("repo-docs evals passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
