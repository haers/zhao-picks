# NotionNext、Wisp与MDX：先选写作方式

选择博客模板之前，先确定文章存在哪里、谁来编辑，以及愿意承担哪些服务依赖。

| 方案 | 适合谁 | 主要价值 | 主要成本 |
| --- | --- | --- | --- |
| [NotionNext](https://github.com/notionnext-org/NotionNext) | 已习惯Notion写作的人 | 多主题、分类、SEO与发布链路围绕Notion组织 | 读取、缓存、同步与私密内容边界 |
| [Wisp模板](https://github.com/Wisp-CMS/nextjs-blog-cms-wisp) | 希望使用托管内容后台的人 | CMS与Next.js展示模板配套 | 账号方案、费用、API、导出与评论服务 |
| [Velite/MDX模板](https://github.com/codebucks27/Nextjs-tailwindcss-blog-template) | 熟悉Git，或要在文章里嵌React组件的人 | 文件内容、schema和组件表达 | 构建管线、代码审查及额外服务配置 |

## 主要不足

NotionNext的主题和密码页仍需要核对更新、缓存失效与内容可见范围。Wisp模板依赖外部内容源，双列卡片不代表脱离账号也能完整运行。

MDX会编译为组件代码，适合可信作者，不宜直接接受不可信投稿。所读模板的阅读计数还依赖Supabase，联系表单也不代表已经实现邮件投递。

## 结论

继续用Notion写作，可优先考察NotionNext；接受托管CMS，可比较Wisp；明确需要文章内组件，再选Velite/MDX。普通Markdown足够时，不必仅为主题外观增加新的内容系统。

依据：源码阅读及部分官方历史截图，未连接CMS账号或验证部署；结论更新2026-10-24。版本信息来自2026-10-23查询，采用前重查。三项上游此前核对为MIT，图片、字体和第三方服务另核授权。
