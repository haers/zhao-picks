"""网站生成的单源、子路径和发布边界回归。"""

import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("prepare_site", Path(__file__).with_name("prepare_site.py"))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SitePreparation(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        (self.root / 'reviews').mkdir()
        (self.root / 'assets').mkdir()
        for directory in ['_includes', '_sass', 'assets']:
            (self.root / 'site' / directory).mkdir(parents=True)
        (self.root / '_config.yml').write_text('baseurl: /demo\n')
        (self.root / 'LICENSE').write_text('License text')
        (self.root / 'AGENTS.md').write_text('Not a reader page')
        self.index = '# Demo\n\n## 项目结论\n\n| 项目 | 用途 | 结论 | 依据 |\n| --- | --- | --- | --- |\n| [示例](reviews/example.md) | 用途 | 参考 | 阅读 |\n\n## 选型专题\n\n| 专题 | 用途 | 结论 | 依据 |\n| --- | --- | --- | --- |\n\n## 如何收录\n\n公开结论\n\n## 许可与致谢\n\n[许可](LICENSE)\n'
        (self.root / 'README.md').write_text(self.index)
        (self.root / 'reviews/example.md').write_text('# 示例\n\n## 结论\n\n值得阅读。\n依据：源码阅读。\n')

    def test_single_source_and_excluded_maintenance(self):
        report = builder.prepare(self.root)
        self.assertEqual(report['details'], 1)
        stage = self.root / 'work/site-src'
        self.assertFalse((stage / 'AGENTS.md').exists())
        self.assertFalse((stage / 'scripts').exists())
        self.assertNotIn('/demo/reviews/example/', (stage / 'index.md').read_text())
        self.assertIn('/demo/projects/){: .btn .btn-purple }', (stage / 'index.md').read_text())
        self.assertIn('/demo/reviews/example/', (stage / 'projects.md').read_text())
        self.assertIn('<span class="label">阅读</span>', (stage / 'projects.md').read_text())
        self.assertNotIn('page-context', (stage / 'reviews/example.md').read_text())
        self.assertIn('parent: "项目目录"', (stage / 'reviews/example.md').read_text())
        self.assertIn('值得阅读', (stage / 'search.json').read_text())
        self.assertNotIn('Not a reader', (stage / 'search.json').read_text())

    def test_evidence_is_not_promoted_and_is_escaped(self):
        self.assertIn('源码阅读，尚未试用', builder.evidence_label('源码阅读，尚未试用'))
        self.assertIn('label-purple', builder.evidence_label('源码阅读'))
        self.assertIn('&lt;script&gt;', builder.evidence_label('<script>'))

    def test_rewrite_assets_and_preserve_external_links(self):
        image = self.root / 'assets/example.svg'
        image.write_text('<svg/>')
        assets = set()
        text = '[详情](example.md#结论) ![图](../assets/example.svg) [外链](https://example.com/a.md)'
        result = builder.rewrite_links(text, self.root / 'reviews/example.md', self.root, '/demo', builder.index_entries(self.index), assets)
        self.assertIn('/demo/reviews/example/#结论', result)
        self.assertIn('/demo/assets/example.svg', result)
        self.assertIn('https://example.com/a.md', result)
        self.assertEqual(assets, {image})

    def test_maintenance_links_and_orphans_fail(self):
        with self.assertRaises(ValueError):
            builder.rewrite_links('[内部](../AGENTS.md)', self.root / 'reviews/example.md', self.root, '/demo', builder.index_entries(self.index), set())
        (self.root / 'reviews/orphan.md').write_text('# Orphan')
        with self.assertRaises(ValueError):
            builder.prepare(self.root)

    def test_work_symlink_is_rejected(self):
        (self.root / 'work').symlink_to(self.root / 'assets', target_is_directory=True)
        with self.assertRaises(ValueError):
            builder.prepare(self.root)


if __name__ == '__main__':
    unittest.main()
