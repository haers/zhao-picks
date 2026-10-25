#!/usr/bin/env python3
"""检查生成网站的子路径、页面链接、资源及发布文件边界。"""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.add(data['id'])
        for attribute in ['href', 'src']:
            if data.get(attribute):
                self.links.append(data[attribute])


def check():
    output = ROOT / 'work/site'
    metadata = json.loads((ROOT / 'work/site-input.json').read_text())
    base = metadata['baseurl']
    pages = {path: Page(path.read_text()) for path in output.rglob('*.html')}
    failures = []
    links = 0
    for path, page in pages.items():
        relative = path.relative_to(output).as_posix()
        url = base + '/' + relative.removesuffix('index.html')
        for href in page.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            resolved = urlsplit(urljoin(url, href))
            if not resolved.path.startswith(base + '/'):
                failures.append((relative, '链接未保留项目子路径'))
                continue
            target = output / unquote(resolved.path[len(base) + 1:])
            if target.is_dir():
                target /= 'index.html'
            if not target.resolve().is_relative_to(output.resolve()) or not target.is_file():
                failures.append((relative, '站内页面或资源不存在'))
            elif resolved.fragment and target in pages and unquote(resolved.fragment) not in pages[target].ids:
                failures.append((relative, '页面锚点不存在'))
            links += 1
    for path in output.rglob('*'):
        if path.is_file() and (path.suffix in {'.md', '.py', '.yml', '.lock'} or any(part in {'scripts', 'work', '.github', 'AGENTS.md'} for part in path.relative_to(output).parts)):
            failures.append((str(path.relative_to(output)), '非读者文件进入网站'))
    details = list((output / 'reviews').glob('*/index.html'))
    if len(details) != metadata['details']:
        failures.append(('reviews', '详情数量与索引不一致'))
    search = json.loads((output / 'search.json').read_text())
    if len(search) != metadata['details']:
        failures.append(('search.json', '搜索条目与详情不一致'))
    if failures:
        for filename, reason in failures[:20]:
            print(f'FAIL {filename}: {reason}')
        raise SystemExit(1)
    print(f'PASS: {len(details)}详情，{len(pages)}网页，{links}处站内链接/资源及发布边界')


if __name__ == '__main__':
    check()
