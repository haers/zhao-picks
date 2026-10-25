"""验证索引与正文边界，所有变异样本只在临时目录生成。"""

import importlib.util
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("check_content", Path(__file__).with_name("check-content.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class StructureChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "reviews").mkdir()
        (self.root / "reviews/example.md").write_text("# 示例\n## 结论\n参考\n依据：源码阅读\n")
        self.index = (
            "# 示例清单\n\n## 项目结论\n\n"
            "| 项目 | 用途 | 结论 | 依据 |\n| --- | --- | --- | --- |\n"
            "| [示例](reviews/example.md) | 用途 | 参考 | 阅读 |\n\n"
            "## 如何收录\n\n每条独立成文。\n"
        )

    def failures(self, text):
        return [item[2] for item in checker.check_structure(self.root, text)]

    def test_complete_index_and_topic(self):
        (self.root / "reviews/topic.md").write_text("# 比较专题\n")
        topic = "\n## 选型专题\n\n| 专题 | 用途 | 结论 | 依据 |\n| --- | --- | --- | --- |\n| [比较](reviews/topic.md) | 用途 | 比较 | 阅读 |\n"
        self.assertEqual(self.failures(self.index + topic), [])

    def test_homepage_project_body_is_rejected(self):
        self.assertIn("首页不得嵌入项目详情或非约定章节", self.failures(self.index + "\n## 示例项目\n\n项目详情。\n"))
        self.assertIn("索引章节只允许摘要表格", self.failures(self.index.replace("## 如何收录", "这里又写了详情。\n\n## 如何收录")))

    def test_anchor_missing_and_external_entry_are_rejected(self):
        for href in ["#example", "reviews/missing.md", "https://example.com", "reviews/../README.md"]:
            with self.subTest(href=href):
                self.assertTrue(self.failures(self.index.replace("reviews/example.md", href)))

    def test_duplicate_and_orphan_are_rejected(self):
        row = "| [示例](reviews/example.md) | 用途 | 参考 | 阅读 |"
        self.assertIn("同一正文被重复索引", self.failures(self.index.replace(row, row + "\n" + row)))
        (self.root / "reviews/orphan.md").write_text("# 未引用正文\n")
        self.assertIn("正文未被首页索引引用", self.failures(self.index))

    def test_symlink_and_wrong_columns_are_rejected(self):
        (self.root / "reviews/alias.md").symlink_to(self.root / "reviews/example.md")
        self.assertIn("条目正文缺失、越界或不是普通文件", self.failures(self.index.replace("reviews/example.md", "reviews/alias.md")))
        self.assertIn("索引表格必须为四列", self.failures(self.index.replace("| 用途 | 参考 | 阅读 |", "| 用途 | 阅读 |")))


if __name__ == "__main__":
    unittest.main()
