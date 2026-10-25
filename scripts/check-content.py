#!/usr/bin/env python3
"""检查公开文字的常见隐私模式、结论卡片边界与仓内链接，不回显命中内容。"""

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PATTERNS = (
    ("用户目录", re.compile(r"/(?:Users|home)/[^/\s]+|[A-Za-z]:\\Users\\[^\\\s]+")),
    ("私钥标记", re.compile(r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----")),
    ("常见令牌", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b")),
    ("URL凭据", re.compile(r"\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^\s/@]+@", re.I)),
)
INTERNAL_TERMS = (
    "废纸篓", "恢复包", "manifest.json", "候选盘点", "本轮复审",
    "文件比对", "源码去留", "原件及", "探针", "未提交", "未推送",
)


def check_structure(root: Path, text: str) -> list[tuple[str, int, str]]:
    """校验首页只作索引，且每条索引与独立正文一一对应。"""
    failures = []
    index_sections = {"项目结论", "选型专题"}
    allowed_sections = index_sections | {"如何收录", "许可与致谢"}
    section = None
    headings = set()
    references = []
    root = root.resolve()
    for number, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(2)
            if heading.group(1) != "##" or section not in allowed_sections:
                failures.append(("README.md", number, "首页不得嵌入项目详情或非约定章节"))
            if section in headings:
                failures.append(("README.md", number, "首页章节重复"))
            headings.add(section)
            continue
        if section not in index_sections or not line.strip():
            continue
        if not line.startswith("|") or not line.endswith("|"):
            failures.append(("README.md", number, "索引章节只允许摘要表格"))
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) != 4:
            failures.append(("README.md", number, "索引表格必须为四列"))
            continue
        if cells[0] in {"项目", "专题"} or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        link = re.fullmatch(r"\[[^\]]+\]\(([^)]+)\)", cells[0])
        if not link or not re.fullmatch(r"reviews/[^/#?]+\.md", link.group(1)):
            failures.append(("README.md", number, "条目必须链接独立reviews文档，不能用首页锚点"))
            continue
        target = root / unquote(link.group(1))
        resolved = target.resolve()
        if target.is_symlink() or resolved.parent != root / "reviews" or not target.is_file():
            failures.append(("README.md", number, "条目正文缺失、越界或不是普通文件"))
            continue
        if resolved in references:
            failures.append(("README.md", number, "同一正文被重复索引"))
        references.append(resolved)
    if "项目结论" not in headings or not references:
        failures.append(("README.md", 0, "缺少项目索引"))
    for path in sorted((root / "reviews").glob("*.md")):
        if path.resolve() not in references:
            failures.append((str(path.relative_to(root)), 0, "正文未被首页索引引用"))
    return failures


def main() -> int:
    """规则只约束公开文本；截图像素、元数据和事实仍需人工检查。"""
    files = [ROOT / "README.md", ROOT / "AGENTS.md", *sorted((ROOT / "reviews").glob("*.md"))]
    failures = []
    for path in files:
        label = str(path.relative_to(ROOT))
        if path.is_symlink() or not path.is_file():
            failures.append((label, 0, "缺少普通文本文件"))
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            for rule, pattern in PRIVATE_PATTERNS:
                if pattern.search(line):
                    failures.append((label, number, rule))
            if line.rstrip() != line:
                failures.append((label, number, "行尾空白"))
            if re.search(r"\]\(\s*\)|\]\(undefined\)", line):
                failures.append((label, number, "空或无效链接"))
            for href in re.findall(r"\]\(([^)]+)\)", line):
                href = href.strip().strip("<>")
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                candidate = (path.parent / unquote(parsed.path)).resolve()
                if not candidate.is_relative_to(ROOT) or not candidate.exists():
                    failures.append((label, number, "仓内链接无效或越界"))
        if path.parent.name == "reviews":
            for term in INTERNAL_TERMS:
                if term in text:
                    failures.append((label, 0, "内部过程用语"))
            if "## 结论" not in text or "依据：" not in text:
                failures.append((label, 0, "缺少结论或简短依据"))
    if (ROOT / "README.md").is_file():
        failures.extend(check_structure(ROOT, (ROOT / "README.md").read_text(encoding="utf-8")))
    for label, line, rule in failures:
        print(f"FAIL {label}:{line} {rule}")
    if failures:
        return 1
    print(f"PASS：{len(files)}份公开文本；有限隐私模式、结论边界、链接及索引与独立正文对应检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
