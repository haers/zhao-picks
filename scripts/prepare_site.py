#!/usr/bin/env python3
"""从公开索引与正文生成Jekyll输入；不把维护目录整仓发布。"""

import json
from html import escape
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def index_entries(text: str) -> list[dict]:
    """复用首页顺序和分组，避免另维护一份项目清单。"""
    section = ""
    entries = []
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if section not in {"项目结论", "选型专题"}:
            continue
        match = re.match(r"\| \[([^]]+)\]\((reviews/[^)]+\.md)\) \|", line)
        if match:
            title, filename = match.groups()
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 4 or not cells[3]:
                raise ValueError("索引必须包含项目、用途、结论、依据四列")
            entries.append({"title": title, "file": filename, "slug": Path(filename).stem, "parent": "项目目录" if section == "项目结论" else "选型专题", "evidence": cells[3]})
    if len({entry["file"] for entry in entries}) != len(entries):
        raise ValueError("索引出现重复正文")
    return entries


def evidence_label(evidence: str) -> str:
    """逐字保留索引依据；源码阅读使用紫色，其余依据使用默认蓝色标签，不扩大验证范围。"""
    color = " label-purple" if "源码阅读" in evidence else ""
    return f'<span class="label{color}">{escape(evidence)}</span>'


def label_table(table: str) -> str:
    """仅装饰索引的依据列，结论与链接仍由README拥有。"""
    lines = []
    for line in table.splitlines():
        if re.match(r"\| \[", line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            cells[3] = evidence_label(cells[3])
            line = "| " + " | ".join(cells) + " |"
        lines.append(line)
    return "\n".join(lines)


def front_matter(**values) -> str:
    """JSON字符串作为YAML标量，保护带冒号等字符的标题。"""
    lines = ["---", "layout: default"]
    lines.extend(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in values.items())
    return "\n".join([*lines, "---", ""])


def rewrite_links(text: str, source: Path, root: Path, baseurl: str, entries: list[dict], assets: set[Path]) -> str:
    """仅重写仓内链接；保留外部URL和页面锚点，拒绝发布边界之外的文件。"""
    indexed = {(root / entry["file"]).resolve(): entry for entry in entries}

    def replace(match):
        href = match.group(1)
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group(0)
        target = (source.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(root) or not target.is_file() or (source.parent / unquote(parsed.path)).is_symlink():
            raise ValueError("正文中有越界、符号链接或缺失的本地链接")
        if target in indexed:
            path = f"/reviews/{indexed[target]['slug']}/"
        elif target == root / "README.md":
            path = "/"
        elif target == root / "LICENSE":
            path = "/about/"
        elif target.is_relative_to(root / "assets"):
            assets.add(target)
            path = "/" + target.relative_to(root).as_posix()
        else:
            raise ValueError("正文链接到非读者网站文件")
        suffix = ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
        return "](" + baseurl + path + suffix + ")"

    return re.sub(r"\]\(([^)\n]+)\)", replace, text)


def prepare(root: Path = ROOT) -> dict:
    root = root.resolve()
    readme = (root / "README.md").read_text()
    entries = index_entries(readme)
    actual = {str(path.relative_to(root)) for path in (root / "reviews").glob("*.md")}
    if actual != {entry["file"] for entry in entries}:
        raise ValueError("首页索引与独立正文不一致")
    config = (root / "_config.yml").read_text()
    baseurl = re.search(r"^baseurl:\s*(.*?)\s*$", config, re.M).group(1).strip('"\'')
    if baseurl and not re.fullmatch(r"/[\w-]+(?:/[\w-]+)*", baseurl):
        raise ValueError("baseurl必须为空或明确的站点子路径")
    stage = root / "work/site-src"
    if (root / "work").is_symlink() or stage.is_symlink():
        raise ValueError("生成目录不能是符号链接")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    (stage / "_config.yml").write_text(config)
    for directory in ["_includes", "_sass", "assets"]:
        folder = root / "site" / directory
        if folder.is_symlink():
            raise ValueError("展示目录不能是符号链接")
        for path in folder.rglob("*"):
            if path.is_symlink():
                raise ValueError("展示文件不能包含符号链接")
        shutil.copytree(folder, stage / directory)
    assets = set()

    def write(name, body, **metadata):
        path = stage / name
        path.parent.mkdir(parents=True, exist_ok=True)
        # 文章可能包含Liquid示例；源内容只作为Markdown，不作为模板执行。
        if "{% endraw %}" in body:
            raise ValueError("正文包含需要显式处理的Liquid raw结束标记")
        path.write_text(front_matter(**metadata) + "{% raw %}\n" + body + "\n{% endraw %}\n")

    home = readme.split("## 项目结论")[0]
    home = re.sub(r"^\[阅读网站\].*\n", "", home, flags=re.M)
    home = re.sub(r"^首页只保留索引.*\n", "", home, flags=re.M)
    home = rewrite_links(home, root / "README.md", root, baseurl, entries, assets)
    home += f'\n[浏览项目]({baseurl}/projects/){{: .btn .btn-purple }}\n[选型专题]({baseurl}/topics/){{: .btn }}\n'
    write("index.md", home, title="精选首页", nav_order=1, permalink="/")
    for title, filename, permalink, order in [("项目目录", "projects.md", "/projects/", 2), ("选型专题", "topics.md", "/topics/", 3)]:
        section = "项目结论" if title == "项目目录" else "选型专题"
        table = readme.split("## " + section + "\n", 1)[1].split("\n## ", 1)[0]
        body = f"# {title}\n\n" + rewrite_links(label_table(table), root / "README.md", root, baseurl, entries, assets)
        write(filename, body, title=title, nav_order=order, has_children=True, has_toc=False, permalink=permalink)
    search_entries = []
    for order, entry in enumerate(entries, 1):
        source = root / entry["file"]
        body = rewrite_links(source.read_text(), source, root, baseurl, entries, assets)
        # 详情只保留主题原生面包屑；依据放在标题之后，不重复返回导航。
        heading, separator, rest = body.partition("\n")
        body = heading + "\n\n" + evidence_label(entry["evidence"]) + "\n" + separator + rest
        write(entry["file"], body, title=entry["title"], parent=entry["parent"], nav_order=order, permalink=f"/reviews/{entry['slug']}/", description=entry["title"] + "：用途、价值、限制与结论。")
        plain = re.sub(r"!?\[([^]]*)\]\([^)]+\)", r"\1", source.read_text())
        plain = re.sub(r"<[^>]+>|[#*`|]", " ", plain)
        search_entries.append({"title": entry["title"], "url": f"{baseurl}/reviews/{entry['slug']}/", "text": re.sub(r"\s+", " ", plain).strip()})
    (stage / "search.json").write_text(json.dumps(search_entries, ensure_ascii=False))
    about = "# 关于与许可\n\n" + readme.split("## 如何收录\n", 1)[1]
    about = re.sub(r"维护检查：.*\n", "", about)
    about = rewrite_links(about, root / "README.md", root, baseurl, entries, assets)
    about = about.replace(f"[MIT许可证]({baseurl}/about/)", "MIT许可证")
    about += "\n\n## 原创文字许可\n\n```text\n" + (root / "LICENSE").read_text() + "\n```\n"
    write("about.md", about, title="关于与许可", nav_order=4, permalink="/about/")
    write("404.md", f"# 页面未找到\n\n可以[返回精选首页]({baseurl}/)，或使用站内搜索找到项目。", title="页面未找到", nav_exclude=True, search_exclude=True, permalink="/404.html")
    for asset in assets:
        destination = stage / asset.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset, destination)
    report = {"projects": sum(e["parent"] == "项目目录" for e in entries), "topics": sum(e["parent"] == "选型专题" for e in entries), "details": len(entries), "baseurl": baseurl}
    (root / "work/site-input.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


if __name__ == "__main__":
    print(json.dumps(prepare(), ensure_ascii=False))
