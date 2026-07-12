#!/usr/bin/env python3
"""Validate a generated repo-docs package.

Conservative checks for structure, links, routing, sync anchors, glossary coverage,
sync freshness hints, and drift toward mechanical templates.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

REQUIRED_NON_SEED_FILES = [
    "README.md",
    "walkthroughs/one-real-run.md",
    "code-map.md",
    "references/source-evidence.md",
    "glossary.md",
    "change-log.md",
]
REQUIRED_NON_SEED_DIRS = ["modules", "references"]
REQUIRED_SEED_FILES = [
    "README.md",
    "change-log.md",
    "glossary.md",
]
REQUIRED_LITE_FILES = [
    "README.md",
    "walkthroughs/one-real-run.md",
    "references/source-evidence.md",
    "change-log.md",
]
LOCAL_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IMAGE_LINK_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
STEP_PATTERN = re.compile(r"^#{2,4}\s+(step\s+\d+|第\s*\d+\s*步|步骤\s*\d+)", re.IGNORECASE | re.MULTILINE)
NUMBERED_STEP_H2_PATTERN = re.compile(r"^##\s+(Step\s+\d+|第\s*\d+\s*步|步骤\s*\d+)\s*[:：]", re.IGNORECASE | re.MULTILINE)
MERMAID_PATTERN = re.compile(r"```mermaid[\s\S]*?```", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
FENCE_PATTERN = re.compile(r"```[\s\S]*?```")
INLINE_CODE_PATTERN = re.compile(r"`([^`\n]+)`")
LINK_WITH_TEXT_PATTERN = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
READER_ROUTES_HEADING_PATTERN = re.compile(r"^##\s+(Reader Routes|阅读路径)\s*$", re.MULTILINE)
READER_ROUTES_TABLE_HEADER_PATTERN = re.compile(
    r"\|\s*(Reader goal|读者目标)\s*\|\s*(Start here|从这里开始)\s*\|\s*(What this page gives you|读完后获得什么)\s*\|",
    re.IGNORECASE,
)
CODE_MAP_TABLE_HEADER_PATTERN = re.compile(
    r"\|\s*(Path|路径)\s*\|\s*(Responsibility|职责)\s*\|\s*(Key code|关键代码)\s*\|\s*"
    r"(Connection to the main path|与主流程的关系)\s*\|",
    re.IGNORECASE,
)
CODE_MAP_PATH_ROW_PATTERN = re.compile(r"^\|\s*`([^`]+/)`\s*\|([^\n]+)$", re.MULTILINE)
CODE_MAP_DIRECTORY_HEADING_PATTERN = re.compile(r"^##\s+`([^`]+/)`\s*$", re.MULTILINE)
CODE_MAP_IMPORTANT_CODE_TABLE_PATTERN = re.compile(
    r"\|\s*(Important code|重要代码)\s*\|\s*(Function|功能)\s*\|\s*(Key symbols|关键符号)\s*\|\s*"
    r"(Called by / used by|调用方\s*/\s*使用方)\s*\|",
    re.IGNORECASE,
)
CODE_MAP_COVERAGE_HEADING_PATTERN = re.compile(r"^##\s+(Coverage|覆盖范围|覆盖)\s*$", re.MULTILINE | re.IGNORECASE)
CODE_MAP_SPLIT_LINK_PATTERN = re.compile(r"\]\((?:\./)?code-map/[^)]+\.md(?:#[^)]+)?\)", re.IGNORECASE)
GENERATED_PAGES_PATTERN = re.compile(r"^Generated pages:\s*$|^生成页面：\s*$", re.MULTILINE | re.IGNORECASE)
CONFIDENCE_LABEL_PATTERN = re.compile(r"\b(Confirmed|Inferred|Planned|Unknown)\b|已确认|推断|计划中|未确认")
SOURCEY_OPENING_TOKEN_PATTERN = re.compile(
    r"`[^`\n]+`|"
    r"[\w.@-]+(?:/[\w.@-]+)+\.[A-Za-z0-9]{1,8}(?::\d+(?:-\d+)?)?|"
    r"\b[A-Za-z_][A-Za-z0-9_]{2,}\("
)
BROAD_VALUE_WORD_PATTERN = re.compile(
    r"\b(robust|powerful|seamless|extensible|scalable|efficient|comprehensive|"
    r"important|innovative|advanced|flexible|reliable)\b|"
    r"鲁棒|强大|无缝|可扩展|高效|全面|重要|先进|灵活|可靠|完善",
    re.IGNORECASE,
)
# Link labels that carry no information scent: they name the act of clicking or
# the file, not what the reader gains by following the link.
LOW_SCENT_LABELS = {
    "here", "this", "that", "see", "click", "click here", "read", "read more",
    "more", "link", "page", "doc", "docs", "这里", "看这里", "点击", "详情", "见此",
}
# A source locator looks like a relative path with at least one slash and a file
# extension, optionally followed by :line or :line-range. This stays narrow to
# keep false positives low; bare filenames without a slash are not checked.
SOURCE_LOCATOR_PATTERN = re.compile(r"^[\w.@-]+(?:/[\w.@-]+)+\.[A-Za-z0-9]{1,8}(?::\d+(?:-\d+)?)?$")
READER_STATE_H3_PATTERN = re.compile(
    r"^###\s+("
    r"What You Are Looking At|What To Notice|What Changes|Source Locator|Verification|"
    r"你正在看什么|发生了什么变化|源码定位|验证方法"
    r")",
    re.MULTILINE | re.IGNORECASE,
)
MODULE_TEMPLATE_H2_PATTERN = re.compile(
    r"^##\s+("
    r"Reader Question|In [Cc]ode|Where You Saw This|One Concrete Example|What To Notice|Source Locator|"
    r"Change Risk|Verification|Change Risk And Verification|If you change this|"
    r"读者问题|在代码中|你在哪里见过|一个真实例子|源码定位|改动风险|验证方法|改动风险与验证|如果你要改"
    r")",
    re.MULTILINE | re.IGNORECASE,
)
REDUNDANT_WALKTHROUGH_H2_PATTERN = re.compile(
    r"^##\s+("
    r"What changes|Change risk|Verification|What you are looking at|"
    r"发生了什么变化|改动风险|验证方法|你正在看什么"
    r")",
    re.MULTILINE | re.IGNORECASE,
)
INLINE_LABEL_PATTERN = re.compile(
    r"\*\*(Source locator|Verification|源码定位|验证方法)。\*\*",
    re.IGNORECASE,
)
PATH_IN_PROSE_PATTERN = re.compile(
    r"`[^`\n]*(?:/|\\)[^`\n]*\.(?:py|js|ts|tsx|go|rs|java|rb|md|json|ya?ml|toml)[^`\n]*`",
    re.IGNORECASE,
)
SYNC_ANCHOR_PATTERN = re.compile(
    r"Synced through\s+([0-9a-f]{7,40})|同步至\s+([0-9a-f]{7,40})",
    re.IGNORECASE,
)
REPO_DOCS_RULE_PATTERN = re.compile(r"repo-docs|repo docs|repo 文档|项目理解文档", re.IGNORECASE)
SYNC_RULE_HINT_PATTERN = re.compile(
    r"understanding sync|sync check|change-log|stale|patch|同步|更新|过期|变更|维护",
    re.IGNORECASE,
)
WALKTHROUGH_TASK_SIGNAL_PATTERN = re.compile(
    r"\b(scenario|input|pressure|success|output|task|request|command|artifact|user action)\b|"
    r"场景|真实任务|输入|压力|难点|成功|输出|产物|请求|命令|用户操作",
    re.IGNORECASE,
)
WALKTHROUGH_PRESSURE_SIGNAL_PATTERN = re.compile(
    r"\b(hard part|tricky|difficult|not trivial|cannot simply|pressure|risk|"
    r"ambiguous|ambiguity|untrusted|trust boundary|invalid|failure|fails|"
    r"must preserve|has to preserve|has to parse|has to reject|has to verify)\b|"
    r"难点|困难|不只是|不能直接|风险|压力|不可信|信任边界|无效|失败|必须|需要.*(解析|拒绝|验证|保留)",
    re.IGNORECASE,
)
BOUNDARY_SIGNAL_PATTERN = re.compile(
    r"\b(fail|failure|error|retry|fallback|reject|invalid|validation|caveat|limit|"
    r"limitation|edge case|reflect|permission|guard)\b|"
    r"失败|错误|重试|回退|拒绝|无效|校验|验证|边界|限制|异常|权限|保护",
    re.IGNORECASE,
)
# Generic mechanism signals only. Keep this WARN-only and do not add
# project names, method names, page names, or repo-specific domains here.
MODULE_CASE_TRIGGER_PATTERN = re.compile(
    r"\b(transform|transformation|contract|schema|payload|shape|input|output|state|"
    r"transition|lifecycle|route|routing|retriev\w*|select\w*|rank\w*|persist\w*|"
    r"decision|permission|boundary|allowed|denied)\b|"
    r"转换|合同|契约|结构|形状|输入|输出|状态|变化|流转|生命周期|路由|检索|选择|排序|持久|决策|权限|边界|允许|拒绝",
    re.IGNORECASE,
)
MODULE_CASE_SIGNAL_PATTERN = re.compile(
    r"\b(case|example|for example|e\.g\.|before\s*->\s*after|input\s*->\s*output|"
    r"allowed\s+vs\s+denied|normal|boundary|failure|timeline)\b|"
    r"示例|例子|案例|输入/输出|前后|允许|拒绝|正常|边界|失败|时间线",
    re.IGNORECASE,
)
EVIDENCE_MAP_NAMES = {"source-evidence.md"}
EVIDENCE_TRAVERSAL_PATTERN = re.compile(
    r"\bPass\s*1\b[\s\S]*\bPass\s*2\b|第\s*1\s*(轮|遍)[\s\S]*第\s*2\s*(轮|遍)",
    re.IGNORECASE,
)
EVIDENCE_COVERAGE_PATTERN = re.compile(
    r"\b(coverage|covered|out of scope|excluded|adjacent|not traced|not covered|scope)\b|"
    r"覆盖|范围|未覆盖|不覆盖|相邻|不追踪",
    re.IGNORECASE,
)
EVIDENCE_TABLE_HEADER_PATTERN = re.compile(
    r"\|\s*Claim\s*\|\s*Evidence\s*\|\s*Confidence\s*\|\s*Caveat\s*\|\s*Used by\s*\||"
    r"\|\s*(声明|结论)\s*\|\s*证据\s*\|\s*置信(?:度)?\s*\|\s*(边界|备注|注意事项|限制|Caveat)\s*\|\s*(用于|使用页面|被用于|页面)\s*\|",
    re.IGNORECASE,
)
READER_SIMULATION_PATTERN = re.compile(r"reader simulation|simulated reader|读者模拟|模拟读者", re.IGNORECASE)
READER_SIMULATION_NEEDLES = [
    "main path",
    "real path",
    "hard part",
    "non-trivial",
    "phase",
    "boundary",
    "failure",
    "verify",
    "verification",
    "主路径",
    "真实路径",
    "难点",
    "阶段",
    "边界",
    "失败",
    "验证",
]
FALSIFYING_SIGNAL_PATTERN = re.compile(
    r"\b(falsif\w*|prove this explanation wrong|prove .* wrong|would prove|"
    r"wrong or incomplete|counterevidence|contradict\w*|missing evidence|"
    r"what would break|break without)\b|"
    r"证伪|反证|证明.*错误|推翻|证据不足|没有.*会坏|缺少.*证据",
    re.IGNORECASE,
)
NEXT_READER_SIGNAL_PATTERN = re.compile(
    r"\b(careful newcomer|reader follow-up|next reader question|ask next|"
    r"follow-up|next question|strongest likely follow-up|defer\w*|unknown)\b|"
    r"下一问|追问|后续问题|读者.*问|未确认|未知|暂缓",
    re.IGNORECASE,
)
SOURCE_FIRST_STEP_PATTERN = re.compile(
    r"^##\s+(?:Step\s+\d+|第\s*\d+\s*步|步骤\s*\d+)[:：][^\n]*\n+"
    r"(?:\s*\n)*\s*(?:`[^`]+`|[A-Za-z_][A-Za-z0-9_]*\(\)|[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*\(\))",
    re.IGNORECASE | re.MULTILINE,
)
AGENT_INSTRUCTION_NAME_PATTERN = re.compile(r"^(AGENTS|CLAUDE|GEMINI)(?:\.override)?\.md$", re.IGNORECASE)
AGENT_HEADING_PATTERN = re.compile(r"(?m)^#{1,3}\s+.*(agent|coding agent|instructions|指令|规则)", re.IGNORECASE)
SOURCE_FILE_IN_TOKEN = re.compile(
    r"\.(py|js|ts|tsx|go|rs|java|rb|json|ya?ml|toml|md)\b",
    re.IGNORECASE,
)
LOWERCASE_IDENTIFIER = re.compile(r"^[a-z_][a-z0-9_]*$")


@dataclass
class Finding:
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a repo-docs package")
    parser.add_argument("repo_docs", type=Path, help="Path to repo-docs directory")
    parser.add_argument("--seed", action="store_true", help="Validate Seed-mode structure")
    parser.add_argument(
        "--lite",
        action="store_true",
        help="Validate Lite-mode structure for small or single-purpose repos",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repo root used to verify that cited source locators actually exist",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def link_target_exists(source: Path, target: str, root: Path, repo_root: Path | None = None) -> bool:
    target = target.strip()
    if not target or target.startswith("#"):
        return True
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return True
    path_part = unquote(target.split("#", 1)[0])
    if not path_part:
        return True
    candidate = (source.parent / path_part).resolve()
    allowed_roots = [root.resolve()]
    if repo_root is not None:
        allowed_roots.append(repo_root.resolve())
    for allowed_root in allowed_roots:
        try:
            candidate.relative_to(allowed_root)
        except ValueError:
            continue
        return candidate.exists()
    return False


def check_structure(root: Path, seed: bool, lite: bool) -> list[Finding]:
    findings: list[Finding] = []
    if seed:
        required_files = REQUIRED_SEED_FILES
    elif lite:
        required_files = REQUIRED_LITE_FILES
    else:
        required_files = REQUIRED_NON_SEED_FILES
    for relative in required_files:
        if not (root / relative).is_file():
            findings.append(Finding("ERROR", f"Missing required file: {relative}"))
    if not seed and not lite:
        for relative in REQUIRED_NON_SEED_DIRS:
            directory = root / relative
            if not directory.is_dir():
                findings.append(Finding("ERROR", f"Missing required directory: {relative}/"))
            elif not any(directory.glob("*.md")):
                findings.append(Finding("WARN", f"No markdown pages found in {relative}/"))
    return findings


def check_links(root: Path, repo_root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for path in markdown_files(root):
        text = read_text(path)
        links = LOCAL_LINK_PATTERN.findall(text) + IMAGE_LINK_PATTERN.findall(text)
        for target in links:
            if not link_target_exists(path, target, root, repo_root):
                relative = path.relative_to(root)
                findings.append(Finding("ERROR", f"Broken local link in {relative}: {target}"))
    return findings


def check_non_seed_routing(root: Path, lite: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    readme = root / "README.md"
    walkthrough = root / "walkthroughs" / "one-real-run.md"

    if readme.is_file():
        text = read_text(readme)
        if "walkthroughs/one-real-run.md" not in text and "one-real-run.md" not in text:
            findings.append(Finding("ERROR", "README.md does not link to the main walkthrough"))
        if not READER_ROUTES_HEADING_PATTERN.search(text):
            findings.append(Finding("ERROR", "README.md should include `## Reader Routes` or `## 阅读路径`"))
        if not READER_ROUTES_TABLE_HEADER_PATTERN.search(text):
            findings.append(
                Finding(
                    "ERROR",
                    "README.md should use reader-goal table columns: Reader goal | Start here | What this page gives you",
                )
            )
        if GENERATED_PAGES_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "README.md should route via `## Reader Routes`; convert the Generated pages list to reader-goal rows",
                )
            )
        if "references/source-evidence.md" not in text and "source-evidence.md" not in text:
            findings.append(Finding("ERROR", "README.md should route evidence audit to references/source-evidence.md"))
        if (not lite or (root / "code-map.md").is_file()) and "code-map.md" not in text:
            findings.append(Finding("ERROR", "README.md should route code location to code-map.md"))

    if walkthrough.is_file():
        text = read_text(walkthrough)
        if (root / "code-map.md").is_file() and "code-map.md" not in text:
            findings.append(Finding("ERROR", "Main walkthrough should route onward to code-map.md"))
        has_step = bool(STEP_PATTERN.search(text))
        has_locator = contains_any(
            text,
            [
                "Source Locator",
                "Source locator",
                "源码定位",
                "**Source locator.**",
                "**源码定位。**",
                "source-map.md",
            ],
        ) or bool(PATH_IN_PROSE_PATTERN.search(text))
        source_link_targets = [
            target
            for target in LOCAL_LINK_PATTERN.findall(text)
            if SOURCE_FILE_IN_TOKEN.search(target) or "/" in target and target.startswith("..")
        ]
        has_locator = has_locator or bool(source_link_targets)
        if not has_step:
            findings.append(Finding("WARN", "Main walkthrough should use numbered Step headings such as `## Step 1: ...`"))
        if not has_step and not has_locator:
            findings.append(Finding("WARN", "Main walkthrough has no obvious steps or path-like source references"))
        if not has_locator:
            findings.append(Finding("WARN", "Main walkthrough does not reference source paths in prose or locator labels"))
        if not contains_any(text, ["Verification", "验证方法", "验证", "pytest", "npm test", "cargo test", "go test"]):
            findings.append(Finding("WARN", "Main walkthrough does not include verification language"))
        opening = walkthrough_opening_text(text)
        if has_step and not WALKTHROUGH_TASK_SIGNAL_PATTERN.search(opening):
            findings.append(
                Finding(
                    "WARN",
                    "Main walkthrough opening lacks obvious task framing; name the scenario, input, pressure, and success/output before the steps",
                )
            )
        if has_step and not WALKTHROUGH_PRESSURE_SIGNAL_PATTERN.search(opening):
            findings.append(
                Finding(
                    "WARN",
                    "Main walkthrough opening does not state the hard part clearly; add an explicit pressure sentence before the steps",
                )
            )
        if has_step and not BOUNDARY_SIGNAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "Main walkthrough has no obvious failure, boundary, retry, validation, or caveat signal; include one real guard path when source evidence exists",
                )
            )
        if SOURCE_FIRST_STEP_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "A walkthrough step appears to start with a function or source name; start with the phase pressure/effect, then use source names as proof",
                )
            )
        inline_labels = len(INLINE_LABEL_PATTERN.findall(text))
        if inline_labels >= 3:
            findings.append(
                Finding(
                    "WARN",
                    f"Main walkthrough repeats inline labels ({inline_labels}x); weave paths and checks into prose instead",
                )
            )
        numbered_steps = len(NUMBERED_STEP_H2_PATTERN.findall(text))
        if has_step and numbered_steps == 0:
            findings.append(
                Finding(
                    "WARN",
                    "Main walkthrough step headings should include a behavior name after a colon, e.g. `## Step 1: input becomes a record`",
                )
            )
        fragmented = len(READER_STATE_H3_PATTERN.findall(text))
        if fragmented >= 3:
            findings.append(
                Finding(
                    "WARN",
                    "Main walkthrough repeats reader-state ### subheadings; use numbered Step headings and prose instead",
                )
            )
        redundant_closing = len(REDUNDANT_WALKTHROUGH_H2_PATTERN.findall(text))
        if redundant_closing >= 2:
            findings.append(
                Finding(
                    "WARN",
                    "Main walkthrough has multiple closing/meta ## sections that likely repeat the steps; merge into prose or one closing block",
                )
            )
        if "<details" in text.lower() and STEP_PATTERN.search(text):
            findings.append(Finding("WARN", "Main walkthrough uses <details>; confirm the main explanation path is not hidden"))

    flows = root / "flows.md"
    if flows.is_file():
        text = read_text(flows).lower()
        relationship_terms = ["relationship", "phase", "state", "multiple", "workflow", "关系", "阶段", "状态", "多条"]
        if not any(term in text for term in relationship_terms):
            findings.append(Finding("WARN", "flows.md exists but does not read like a relationship map"))
        if not walkthrough.is_file():
            findings.append(Finding("ERROR", "flows.md exists but the main walkthrough is missing"))

    return findings


def check_code_map(root: Path) -> list[Finding]:
    path = root / "code-map.md"
    if not path.is_file():
        return []

    findings: list[Finding] = []
    text = read_text(path)
    if not CODE_MAP_TABLE_HEADER_PATTERN.search(text):
        findings.append(
            Finding(
                "ERROR",
                "code-map.md should use Path | Responsibility | Key code | Connection to the main path columns",
            )
        )
    directory_rows = {path_value: row_tail for path_value, row_tail in CODE_MAP_PATH_ROW_PATTERN.findall(text)}
    directory_headings = list(CODE_MAP_DIRECTORY_HEADING_PATTERN.finditer(text))
    heading_paths = {match.group(1) for match in directory_headings}
    split_paths = {
        path_value
        for path_value, row_tail in directory_rows.items()
        if CODE_MAP_SPLIT_LINK_PATTERN.search(row_tail)
    }
    missing_sections = sorted(set(directory_rows) - heading_paths - split_paths)
    if not directory_rows:
        findings.append(
            Finding(
                "WARN",
                "code-map.md has no directory rows beneath its summary table",
            )
        )
    elif missing_sections:
        findings.append(
            Finding(
                "WARN",
                f"code-map.md is missing per-directory sections for: {', '.join(missing_sections)}",
            )
        )

    missing_code_tables: list[str] = []
    for index, heading in enumerate(directory_headings):
        section_end = directory_headings[index + 1].start() if index + 1 < len(directory_headings) else len(text)
        coverage = CODE_MAP_COVERAGE_HEADING_PATTERN.search(text, heading.end())
        if coverage is not None and coverage.start() < section_end:
            section_end = coverage.start()
        section = text[heading.end() : section_end]
        if not CODE_MAP_IMPORTANT_CODE_TABLE_PATTERN.search(section):
            missing_code_tables.append(heading.group(1))
    if missing_code_tables:
        findings.append(
            Finding(
                "WARN",
                f"code-map.md has directory sections without an important-code table: {', '.join(missing_code_tables)}",
            )
        )

    coverage_heading = CODE_MAP_COVERAGE_HEADING_PATTERN.search(text)
    if coverage_heading is None:
        findings.append(
            Finding(
                "WARN",
                "code-map.md has no explicit `## Coverage` section; distinguish covered source from generated, vendored, unrelated, excluded, or deferred areas",
            )
        )
    elif directory_headings and coverage_heading.start() < directory_headings[-1].start():
        findings.append(Finding("WARN", "code-map.md should place its Coverage section after all directory sections"))
    if "walkthroughs/one-real-run.md" not in text and "one-real-run.md" not in text:
        findings.append(Finding("ERROR", "code-map.md should route back to the main walkthrough"))
    return findings


def last_sync_sha(change_log_text: str) -> str | None:
    matches = list(SYNC_ANCHOR_PATTERN.finditer(change_log_text))
    if not matches:
        return None
    match = matches[-1]
    return match.group(1) or match.group(2)


def narrative_markdown_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for relative in ("README.md", "walkthroughs/one-real-run.md", "code-map.md"):
        path = root / relative
        if path.is_file():
            paths.append(path)
    modules = root / "modules"
    if modules.is_dir():
        paths.extend(sorted(modules.glob("*.md")))
    return paths


def cited_source_paths(root: Path) -> set[str]:
    cited: set[str] = set()
    for path in narrative_markdown_paths(root):
        text = FENCE_PATTERN.sub("", read_text(path))
        for match in INLINE_CODE_PATTERN.finditer(text):
            token = match.group(1).strip().split(":", 1)[0].replace("\\", "/")
            if SOURCE_LOCATOR_PATTERN.match(token) or ("/" in token and SOURCE_FILE_IN_TOKEN.search(token)):
                cited.add(token)
    return cited


def git_diff_paths(repo_root: Path, since_sha: str) -> set[str] | None:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{since_sha}..HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def paths_overlap(cited: str, changed: str) -> bool:
    if cited == changed:
        return True
    if cited.startswith(changed + "/") or changed.startswith(cited + "/"):
        return True
    return False


def check_change_log_anchor(root: Path) -> list[Finding]:
    path = root / "change-log.md"
    if not path.is_file():
        return []
    text = read_text(path)
    if len(text.strip()) < 80:
        return []
    if SYNC_ANCHOR_PATTERN.search(text):
        return []
    return [
        Finding(
            "WARN",
            "change-log.md has no Synced through <sha> / 同步至 <sha> anchor; add one after each sync for incremental updates",
        )
    ]


def check_sync_freshness(root: Path, repo_root: Path) -> list[Finding]:
    change_log = root / "change-log.md"
    if not change_log.is_file():
        return []
    sha = last_sync_sha(read_text(change_log))
    if not sha:
        return []
    changed = git_diff_paths(repo_root, sha)
    if changed is None or not changed:
        return []
    cited = cited_source_paths(root)
    stale = sorted({cited_path for cited_path in cited if any(paths_overlap(cited_path, diff_path) for diff_path in changed)})
    if not stale:
        return []
    preview = ", ".join(stale[:8])
    suffix = "..." if len(stale) > 8 else ""
    return [
        Finding(
            "WARN",
            f"source changed since last sync anchor ({sha[:7]}); review narrative pages citing: {preview}{suffix}",
        )
    ]


def check_glossary_coverage(root: Path) -> list[Finding]:
    glossary = root / "glossary.md"
    if not glossary.is_file():
        return []
    glossary_text = read_text(glossary).lower()
    counts: dict[str, int] = {}
    for path in narrative_markdown_paths(root):
        if path.name in {"README.md", "code-map.md"}:
            continue
        text = FENCE_PATTERN.sub("", read_text(path))
        for match in INLINE_CODE_PATTERN.finditer(text):
            token = match.group(1).strip()
            if "/" in token or SOURCE_FILE_IN_TOKEN.search(token):
                continue
            if LOWERCASE_IDENTIFIER.match(token):
                continue
            if len(token) < 3 or len(token) > 48:
                continue
            counts[token] = counts.get(token, 0) + 1

    findings: list[Finding] = []
    for term, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        if count < 2:
            continue
        if term.lower() in glossary_text:
            continue
        findings.append(
            Finding(
                "WARN",
                f"glossary.md has no entry for `{term}` (appears {count}x in narrative pages); add a row if readers confuse it",
            )
        )
    return findings[:5]


def contains_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def check_explanation_structure(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for path in sorted((root / "modules").glob("*.md")) if (root / "modules").is_dir() else []:
        text = read_text(path)
        relative = path.relative_to(root)

        has_code_shape = contains_any(
            text,
            ["In code", "在代码中", "source locator", "源码定位"],
        ) or "```" in text
        has_usage_example = "```" in text
        if has_code_shape and not has_usage_example:
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} explains a code shape but has no minimal fenced example or command",
                )
            )

        if MODULE_CASE_TRIGGER_PATTERN.search(text) and not MODULE_CASE_SIGNAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} explains a mechanism with inputs/outputs or boundaries but has no obvious representative case; add an input/output, before/after, normal/boundary, or allowed/denied example when evidence supports it",
                )
            )

        inline_labels = len(INLINE_LABEL_PATTERN.findall(text))
        if inline_labels >= 3:
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} repeats inline labels ({inline_labels}x); weave paths into prose instead",
                )
            )

        template_h2 = len(MODULE_TEMPLATE_H2_PATTERN.findall(text))
        if template_h2 >= 5:
            findings.append(
                Finding(
                    "WARN",
                    f"{relative}: {template_h2} template-like module ## headings; use clearer concept-first headings",
                )
            )

    for path in sorted((root / "references").glob("*.md")) if (root / "references").is_dir() else []:
        text = read_text(path)
        relative = path.relative_to(root)
        headings = "\n".join(HEADING_PATTERN.findall(text))
        if contains_any(headings, ["Why", "How it works", "Reader Question", "为什么", "如何工作", "读者问题"]):
            findings.append(Finding("WARN", f"{relative} contains explanation headings; consider moving them to walkthroughs/ or modules/"))

    for path in markdown_files(root):
        text = read_text(path)
        if "```mermaid" in text.lower():
            without_diagrams = MERMAID_PATTERN.sub("", text)
            if not contains_any(without_diagrams, ["diagram", "shows", "notice", "relationship", "state", "phase", "图", "关系", "注意", "阶段", "状态"]):
                relative = path.relative_to(root)
                findings.append(Finding("WARN", f"{relative} has a Mermaid diagram without obvious explanatory prose"))

    return findings


def check_quality_review(root: Path) -> list[Finding]:
    references = root / "references"
    if not references.is_dir():
        return []

    findings: list[Finding] = []
    evidence_maps = [path for path in sorted(references.glob("*.md")) if path.name in EVIDENCE_MAP_NAMES]
    quality_review = references / "quality-review.md"

    if evidence_maps and not quality_review.is_file():
        return findings

    if quality_review.is_file():
        text = read_text(quality_review)
        if not READER_SIMULATION_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "references/quality-review.md has no Reader Simulation section; answer the guide from a reader's point of view",
                )
            )
        simulation_hits = sum(1 for needle in READER_SIMULATION_NEEDLES if needle.lower() in text.lower())
        if simulation_hits < 4:
            findings.append(
                Finding(
                    "WARN",
                    "references/quality-review.md does not cover enough reader-simulation questions: path, hard part, phases, boundary, verification",
                )
            )
        if not FALSIFYING_SIGNAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "references/quality-review.md does not name what would falsify or materially weaken the guide's explanation; re-inspect source/tests/config/artifacts or label the gap",
                )
            )
        if not NEXT_READER_SIGNAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    "references/quality-review.md does not name a likely next reader question or follow-up",
                )
            )
    return findings


def check_evidence_maps(root: Path) -> list[Finding]:
    references = root / "references"
    if not references.is_dir():
        return []

    findings: list[Finding] = []
    for path in sorted(references.glob("*.md")):
        if path.name not in EVIDENCE_MAP_NAMES:
            continue
        text = read_text(path)
        relative = path.relative_to(root)
        if not EVIDENCE_TRAVERSAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} does not record at least Pass 1 and Pass 2; written evidence maps should prove two evidence traversals",
                )
            )
        if not EVIDENCE_COVERAGE_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} has no obvious coverage or out-of-scope note; name adjacent paths checked but not traced",
                )
            )
        if not EVIDENCE_TABLE_HEADER_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} should use a Claim | Evidence | Confidence | Caveat | Used by table for auditability",
                )
            )
        if not FALSIFYING_SIGNAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} does not name a falsifying check or boundary evidence that would change the explanation; re-inspect source/tests/config/artifacts or label the gap",
                )
            )
        if not NEXT_READER_SIGNAL_PATTERN.search(text):
            findings.append(
                Finding(
                    "WARN",
                    f"{relative} does not name a likely next reader question, deferred topic, or unknown",
                )
            )
    return findings


def check_source_truth_hints(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    confirmed_pattern = re.compile(r"\bConfirmed\b|已确认")
    skip_patterns = [
        "Evidence status: Confirmed unless",
        "Confirmed unless",
        "证据状态：除特别标注外",
        "| `Confirmed` |",
    ]

    for path in markdown_files(root):
        relative = path.relative_to(root)
        for lineno, line in enumerate(read_text(path).splitlines(), start=1):
            if not confirmed_pattern.search(line):
                continue
            if any(pattern in line for pattern in skip_patterns):
                continue
            has_locator = "`" in line or "](" in line or re.search(r"\b(src|tests?|scripts?|config|data|docs?|materials?)/", line)
            if not has_locator:
                findings.append(Finding("WARN", f"{relative}:{lineno} uses Confirmed/已确认 without an obvious source locator"))
    return findings


def first_content_lines(text: str, limit: int = 80) -> str:
    lines = []
    for line in FENCE_PATTERN.sub("", text).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    return "\n".join(lines)


def readme_opening_text(text: str) -> str:
    """Return prose before the Reader Routes table."""
    without_fences = FENCE_PATTERN.sub("", text)
    routes_heading = READER_ROUTES_HEADING_PATTERN.search(without_fences)
    opening = without_fences[: routes_heading.start()] if routes_heading else without_fences
    return first_content_lines(opening, limit=30)


def walkthrough_opening_text(text: str) -> str:
    """Return prose before the first numbered walkthrough step."""
    without_fences = FENCE_PATTERN.sub("", text)
    first_step = STEP_PATTERN.search(without_fences)
    opening = without_fences[: first_step.start()] if first_step else without_fences
    return first_content_lines(opening, limit=40)


def sourcey_opening_count(text: str) -> int:
    """Count source-shaped tokens in an opening without following Markdown links."""
    text = re.sub(r"(?<!!)\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return len(SOURCEY_OPENING_TOKEN_PATTERN.findall(text))


def section_text(text: str, heading_pattern: str) -> str:
    match = re.search(heading_pattern, text, re.IGNORECASE | re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


def check_reading_experience(root: Path) -> list[Finding]:
    """Warn when page structure gets in the way of explanation."""
    findings: list[Finding] = []
    narrative_paths: list[Path] = []
    for relative in ("README.md", "walkthroughs/one-real-run.md", "code-map.md"):
        path = root / relative
        if path.is_file():
            narrative_paths.append(path)
    modules = root / "modules"
    if modules.is_dir():
        narrative_paths.extend(sorted(modules.glob("*.md")))

    for path in narrative_paths:
        relative = path.relative_to(root)
        text = read_text(path)
        if relative == Path("README.md"):
            opening = readme_opening_text(text)
        elif relative.parts[0] == "walkthroughs":
            opening = walkthrough_opening_text(text)
        else:
            opening = first_content_lines(text)
        label_count = len(CONFIDENCE_LABEL_PATTERN.findall(FENCE_PATTERN.sub("", text)))
        h3_count = len(re.findall(r"^###\s+", text, re.MULTILINE))
        if relative.parts[0] == "walkthroughs" and h3_count >= 6:
            findings.append(
                Finding(
                    "WARN",
                    f"{relative}: many ### subheadings; keep numbered Step headings and connected prose",
                )
            )
        if relative.parts[0] in {"walkthroughs", "modules"} and label_count > 8:
            findings.append(
                Finding("WARN", f"{relative}: many confidence labels; prefer page-level evidence status and local labels only for confidence changes")
            )
        if relative == Path("README.md") and label_count > 5:
            findings.append(
                Finding("WARN", f"{relative}: many confidence labels in the main guide; keep evidence visible but quiet")
            )
        if relative == Path("README.md") or relative.parts[0] == "walkthroughs":
            code_name_count = sourcey_opening_count(opening)
            if code_name_count >= 6:
                findings.append(
                    Finding(
                        "WARN",
                        f"{relative}: opening has many code-shaped names ({code_name_count}); start with the reader situation before source locators",
                    )
                )

        readme_meta_h2 = re.compile(
            r"^##\s+(Project Model|First Path|Current Scope|项目模型|首读路径|当前范围)",
            re.MULTILINE,
        )
        if relative == Path("README.md") and len(readme_meta_h2.findall(text)) >= 2:
            findings.append(
                Finding(
                    "WARN",
                    f"{relative}: multiple orienting ## sections; merge thesis, model, and first path into opening prose per PAGE_RULES.md",
                )
            )

        prose = FENCE_PATTERN.sub("", text)
        broad_words = BROAD_VALUE_WORD_PATTERN.findall(prose)
        if len(broad_words) > 6:
            findings.append(
                Finding(
                    "WARN",
                    f"{relative}: many broad value words; prefer concrete actions, observations, checks, or caveats",
                )
            )
    return findings


def check_reference_scope(root: Path) -> list[Finding]:
    """References are fixed generated artifacts, not a second knowledge layer."""
    references = root / "references"
    if not references.is_dir():
        return []

    allowed = {"source-evidence.md", "quality-review.md"}
    findings: list[Finding] = []
    for path in sorted(references.glob("*.md")):
        if path.name not in allowed:
            findings.append(
                Finding(
                    "ERROR",
                    f"{path.relative_to(root)} is outside the fixed references scope; keep references to source-evidence.md and optional quality-review.md, and move knowledge/details into modules",
                )
            )
    return findings


def check_source_locators(root: Path, repo_root: Path) -> list[Finding]:
    """Verify that inline path-like source locators resolve to a real file.

    A locator is checked only when it looks like a relative path with a file
    extension (e.g. ``src/foo.py`` or ``tests/test_bar.py:42``). It passes if it
    exists under the repo root, under the repo-docs root, or relative to the
    citing page, which keeps doc-internal links from producing false warnings.
    Fenced code blocks are skipped so commands and sample output are not scanned.
    """
    findings: list[Finding] = []
    repo_root = repo_root.resolve()
    for path in markdown_files(root):
        relative = path.relative_to(root)
        if relative == Path("change-log.md"):
            continue
        text = FENCE_PATTERN.sub("", read_text(path))
        for match in INLINE_CODE_PATTERN.finditer(text):
            token = match.group(1).strip()
            if not SOURCE_LOCATOR_PATTERN.match(token):
                continue
            file_part = token.split(":", 1)[0]
            candidates = [repo_root / file_part, root / file_part, path.parent / file_part]
            if not any(candidate.exists() for candidate in candidates):
                findings.append(
                    Finding("WARN", f"{relative}: source locator `{token}` not found under repo root")
                )
    return findings


def check_scent(root: Path) -> list[Finding]:
    """Check information scent: content pages should route the reader onward, and
    onward link labels should name what the reader gains, not the file or the
    act of clicking. Both are WARN-only and add no text to generated docs; they
    enforce navigability from the author side. Reference/glossary/change-log are
    lookup leaves and are not required to route onward.
    """
    findings: list[Finding] = []
    content_paths: list[Path] = []
    readme = root / "README.md"
    if readme.is_file():
        content_paths.append(readme)
    code_map = root / "code-map.md"
    if code_map.is_file():
        content_paths.append(code_map)
    for sub in ("walkthroughs", "code-map", "modules"):
        directory = root / sub
        if directory.is_dir():
            content_paths.extend(sorted(directory.glob("*.md")))

    for path in content_paths:
        relative = path.relative_to(root)
        text = FENCE_PATTERN.sub("", read_text(path))
        onward_links = 0
        for match in LINK_WITH_TEXT_PATTERN.finditer(text):
            label = match.group(1).strip()
            target = match.group(2).strip()
            if target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            path_part = unquote(target.split("#", 1)[0]).strip()
            if not path_part.endswith(".md"):
                continue
            if (path.parent / path_part).resolve() == path.resolve():
                continue
            onward_links += 1
            base = path_part.rsplit("/", 1)[-1]
            if label.lower() in LOW_SCENT_LABELS or label in (path_part, base, base[:-3]):
                findings.append(
                    Finding("WARN", f"{relative}: low-scent link label '{label}' — name what the reader gains, not the file")
                )
        if onward_links == 0:
            findings.append(
                Finding("WARN", f"{relative}: no onward link to another page (possible dead end)")
            )
    return findings


def has_repo_docs_sync_rule(path: Path, repo_root: Path) -> bool:
    text = read_text(path)
    if REPO_DOCS_RULE_PATTERN.search(text) and SYNC_RULE_HINT_PATTERN.search(text):
        return True
    return False


def find_agent_instruction_markdown(repo_root: Path) -> list[Path]:
    paths: list[Path] = []

    for path in sorted(repo_root.glob("*.md")):
        if AGENT_INSTRUCTION_NAME_PATTERN.match(path.name):
            paths.append(path)
            continue
        text = read_text(path)
        if AGENT_HEADING_PATTERN.search(text):
            paths.append(path)

    cursor_rules = repo_root / ".cursor" / "rules"
    if cursor_rules.is_dir():
        paths.extend(sorted(cursor_rules.glob("*.md")))

    return paths


def check_agent_instruction_sync(repo_root: Path) -> list[Finding]:
    """Warn when project agent instruction Markdown does not preserve repo-docs sync."""
    findings: list[Finding] = []
    active_files = find_agent_instruction_markdown(repo_root)

    if not active_files:
        findings.append(
            Finding(
                "WARN",
                "repo root has no agent instruction Markdown; Build should create AGENTS.md with repo-docs sync rules",
            )
        )
        return findings

    for path in active_files:
        if not has_repo_docs_sync_rule(path, repo_root):
            relative = path.relative_to(repo_root)
            findings.append(
                Finding(
                    "WARN",
                    f"{relative}: missing repo-docs sync rule for future repo questions and behavior-changing edits",
                )
            )
    return findings


def main() -> int:
    args = parse_args()
    root = args.repo_docs.resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}")
        return 2
    if args.seed and args.lite:
        print("ERROR: choose at most one of --seed and --lite")
        return 2

    findings: list[Finding] = []
    findings.extend(check_structure(root, args.seed, args.lite))
    findings.extend(check_links(root, args.repo_root if args.repo_root is not None and args.repo_root.is_dir() else None))
    if not args.seed:
        findings.extend(check_non_seed_routing(root, lite=args.lite))
        findings.extend(check_code_map(root))
        findings.extend(check_explanation_structure(root))
        findings.extend(check_evidence_maps(root))
        findings.extend(check_quality_review(root))
        findings.extend(check_reference_scope(root))
        findings.extend(check_source_truth_hints(root))
        findings.extend(check_reading_experience(root))
        findings.extend(check_scent(root))
        findings.extend(check_change_log_anchor(root))
        if not args.lite:
            findings.extend(check_glossary_coverage(root))
    if args.repo_root is not None:
        if args.repo_root.is_dir():
            findings.extend(check_source_locators(root, args.repo_root))
            if not args.seed:
                findings.extend(check_agent_instruction_sync(args.repo_root.resolve()))
            if not args.seed:
                findings.extend(check_sync_freshness(root, args.repo_root))
        else:
            findings.append(Finding("ERROR", f"--repo-root is not a directory: {args.repo_root}"))

    errors = [finding for finding in findings if finding.severity == "ERROR"]
    warnings = [finding for finding in findings if finding.severity == "WARN"]

    for finding in findings:
        print(f"{finding.severity}: {finding.message}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
