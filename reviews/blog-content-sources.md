# NotionNext、Wisp与Velite/MDX：先选内容来源，再选博客模板

> 评估日期：2026-10-24；类型：源码选型对比。没有连接Notion或Wisp账号、构建站点、提交评论或验证部署，不作为三套方案的运行推荐。

这三种博客方案最值得比较的是文章从哪里来、作者怎样编辑、发布时依赖什么。若只比较首页和主题数量，很容易选中不适合日常写作的内容流程。

## 一张表选方向

| 内容来源 | 参考项目 | 适合的作者 | 需要承担的工作 |
| --- | --- | --- | --- |
| Notion页面/数据库 | [NotionNext](https://github.com/notionnext-org/NotionNext) | 已习惯在Notion写作，愿意以它作为内容源 | 内容公开边界、读取与缓存、更新同步、主题和部署 |
| 托管CMS | [Wisp博客模板](https://github.com/Wisp-CMS/nextjs-blog-cms-wisp) | 希望使用托管内容后台，接受外部服务依赖 | 账号方案、成本、内容导出、API和评论/邮件边界 |
| 仓库文件与MDX | [Next.js Tailwind博客模板](https://github.com/codebucks27/Nextjs-tailwindcss-blog-template) | 熟悉Git，或需要在可信文章里嵌入React组件 | schema、构建管线、作者代码审查，以及额外服务配置 |

已有普通Markdown即可满足写作需求时，主题外观不一定值得引入新的CMS或MDX执行管线。真正需要的编辑方式、协作和内容组件，才是迁移理由。

## NotionNext：围绕Notion内容源

项目有多主题、分类/标签、SEO、RSS和部署链路。2026-10-23核对时上游仍有维护，既有依赖更新，也有主题解锁/密码页修复。阅读基线为 [93a14f2](https://github.com/notionnext-org/NotionNext/tree/93a14f25570b39da856d40285bafe3d77e838753)。当时发布列表显示v4.11.1，而读取的main包版本为4.11.0，不能混成同一版本证据。

[官方文档/演示入口](https://notionnext.tangly1024.com)可用于进一步选型，本轮未打开当前演示。旧版自带主题截图已查看，只能说明历史设计，不能证明上述版本的功能可用。适合已有Notion内容的人；没有迁移内容源的需求时，不必仅为主题再增加拉取和缓存链路。

采用前至少核对私密页边界、更新同步和缓存失效，再验文章、分类、搜索与手机页面。主题支持密码不等于所有内容获取路径已被验证。

## Wisp：外部内容后台与模板配套

Wisp模板包含App Router、标签、RSS、sitemap、相关文章、评论及OG图片逻辑。[固定阅读版本bdd10b7](https://github.com/Wisp-CMS/nextjs-blog-cms-wisp/tree/bdd10b752d5aa1dcdcb516b9d24229a4c8e2630a)为2025-12-08，包中Next为15.1.9；这是2026-10-23的维护快照，不声称它是持续最新版本或已经解决全部安全问题。

[官方演示](https://blog-demo.wisp.blog)与[文档](https://www.wisp.blog/docs/next-js-blog-starter-kit/overview)是进一步了解的入口。已查看旧版自带的Travel博客截图，双列卡片与标签有参考价值；本轮没有运行当前模板。

它依赖Wisp托管内容源，不能把模板理解为不需账号的完整静态站。评论通过外部服务写入，成功提示还涉及邮件验证；试用前需核对服务方案、内容导出、评论失败和邮件行为。OG签名也应连同配置来源和生成流程检查，不因存在HMAC就承诺安全。

## Velite/MDX：仓库内容与组件表达

该模板用Velite组织文章schema、MDX、目录、阅读时长、封面和高亮。可从[固定版Velite配置](https://github.com/codebucks27/Nextjs-tailwindcss-blog-template/blob/5ee6b9237cf8c2ca58927ce7b3538a963f8ffdf0/velite.config.js)及[首页编排](https://github.com/codebucks27/Nextjs-tailwindcss-blog-template/tree/5ee6b9237cf8c2ca58927ce7b3538a963f8ffdf0/src/components/Home)阅读，并参照[作者教程](https://youtu.be/1QGLHOaRLwM)。固定提交为2026-10-06，记录来自2026-10-23，本轮没有重新确认更新或运行环境。

MDX编译后作为组件代码执行，适合可信作者维护的交互教程，不宜直接接受不可信投稿。普通Markdown内容不需要组件执行能力时，增加这条管线可能没有收益。

这个示例也并非完全离线：阅读计数会创建Supabase客户端并调用计数RPC；缺环境和远端schema时不能保证直接运行。所读版本的联系表单只是console.log，不等于邮件投递、订阅或后台管理已经实现。[官方演示](https://create-blog-with-nextjs.vercel.app/)本轮未访问。

## 许可与验证边界

三项上游在此前核对中均为MIT项目；代码许可不替代主题图片、人物图、字体或其他素材的独立授权。本篇只链接来源，不转载这些资产。

本次依据源码、维护快照与部分项目自带图片比较内容流程，没有测量部署费用、发布速度或长期稳定性。当前没有明确迁移内容来源的需求，因此保留这份比较，不新建个人Fork或整站维护任务。实际采用时固定版本、使用合成内容，并先验证准备依赖的那条流程。
