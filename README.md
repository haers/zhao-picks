# Zhao Picks · 我的开源精选

分享开源项目的用途、适合人群、优缺点和最终建议，帮助读者判断值不值得进一步了解。

收录分为“初步推荐”“学习/设计参考”和“暂不推荐”。试用与源码阅读会分别标注，收录不代表功能全部验收，也不要求读者Star或Fork。

## 项目结论

| 项目 | 适合谁 / 主要用途 | 结论 | 依据 |
| --- | --- | --- | --- |
| [Stretchly](#stretchly) | 需要电脑休息提醒的人 | 已试用，初步推荐 | 初步试用 |
| [shadcn-admin](#shadcn-admin) | 选择React后台界面基础的开发者 | 推荐学习与选型；不是完整业务后台 | 实际试用 |
| [Toolkits](reviews/toolkits.md) | 临时合并普通PDF | PDF有限可用；九宫格暂不推荐 | 定向试用 |
| [Clarity](reviews/clarity.md) | Nuxt Content博客及长教程作者 | 内容展示设计值得参考 | 有限试用 |
| [Slash Admin](reviews/slash-admin.md) | 学习权限反馈、看板与后台布局的开发者 | 交互样板值得参考，业务后端需自建 | 实际试用 |
| [React Antd Admin](reviews/react-antd-admin.md) | 已选择Ant Design的后台开发者 | 适合比较多页签、主题与表单组织 | 源码阅读，演示仅体验登录 |
| [Play Tailwind](reviews/play-tailwind.md) | 需要轻量HTML落地页的开发者 | 静态模板候选，不含业务后端 | 源码阅读 |
| [Anichart](reviews/anichart.md) | 数据动画开发者 | 排名平滑、地图镜头和编排可参考 | 源码阅读 |
| [getFavicon](reviews/favicon-api.md) | 自行实现站点图标获取的开发者 | 实现参考，不建议原样匿名公网部署 | 源码阅读 |
| [RuoYi Blog](reviews/ruoyi-blog.md) | 希望结合博客、记账与个人记录的开发者 | 功能选型候选，不作成熟记账软件推荐 | 源码阅读 |
| [NBlog](reviews/nblog.md) | 学习Java博客后端和通知流程的开发者 | 教学参考，不优先作为新项目底座 | 源码阅读 |
| [My-Blog两版](reviews/my-blog-comparison.md) | 学习Java单体博客的开发者 | 按业务链路或Layui交互选学习方向 | 源码阅读及官方截图 |
| [NotionNext / Wisp / MDX](reviews/blog-content-sources.md) | 正在选择博客内容管理方式的人 | 先选内容来源，再选模板 | 源码阅读及部分官方截图 |
| [ThriveX](reviews/thrivex.md) | 关注相册、旅行足迹和个人表达的人 | 设计候选，注意后端与地图依赖 | 源码阅读 |
| [OneBlog](reviews/oneblog.md) | 研究自定义页面和存储组织的开发者 | 设计参考，暂不推荐直接作新底座 | 源码阅读 |
| [WeBlog](reviews/weblog.md) | 学习Vue3表单与Java文章保存的开发者 | 教学参考，异步与日期边界需完善 | 源码阅读 |
| [拾壹博客](reviews/shiyi-blog.md) | 有多端博客或社区互动需求的开发者 | 多端分工可参考，聊天能力需另验 | 源码阅读及官方截图 |
| [Shoka风格博客应用](reviews/shoka-blog.md) | 研究文章阅读与评论运营的开发者 | 设计参考，不是可安装的Hexo主题 | 源码阅读 |
| [MikuTools](reviews/mikutools.md) | 设计中文小工具平台的开发者 | 搜索与常用入口可参考，不作整站功能推荐 | 源码阅读及官方预览 |
| [ClassFinal](reviews/classfinal.md) | 学习Java产物保护的开发者 | Agent与类加载原理参考，不作不可逆保护或机密保管方案 | 源码阅读 |
| [AI Vocabulary Builder](reviews/ai-vocabulary-builder.md) | 英文阅读者与个人学习工具开发者 | 语境生词本候选及学习流程参考，尚未试用 | 源码阅读 |
| [BibiGPT / v1源码](reviews/bibigpt-v1.md) | 想了解视频重点的人、研究内容摘要的开发者 | 官网选型线索与v1设计参考，尚未试用 | 源码阅读 |

## Stretchly

[Stretchly](https://github.com/hovancik/stretchly)用于提醒电脑使用者定时休息，支持macOS、Windows和Linux。

**结论：已试用，初步推荐。** 适合容易久坐、希望在工作时收到休息提醒的人。支持短休息、长休息及偏好设置；目前是初步体验，尚无长期使用结论，也未逐项验证所有选项。

[官方网站](https://hovancik.net/stretchly) · [官方下载](https://github.com/hovancik/stretchly/releases) · [个人Fork](https://github.com/haers/zhao-stretchly)

原项目BSD-2-Clause许可。个人Fork未修改上游功能，更新与下载优先参考原项目。最近体验：2026-10-21。

## shadcn-admin

[shadcn-admin](https://github.com/satnaing/shadcn-admin)是React后台界面样板，适合查看表格、筛选、表单和导航如何组合。

**结论：推荐学习与选型，不作为完整业务后台推荐。** 仪表盘、任务搜索、用户弹窗和手机侧栏已作定向试用。手机表格仍需横向查看，部分提示有截短；新增用户示例不保存真实数据，登录、权限、持久化和业务接口需要另行实现。

[官方Demo](https://shadcn-admin.netlify.app/) · [个人Fork](https://github.com/haers/zhao-shadcn-admin)

上游MIT许可，保留Sat Naing署名。最近体验：2026-10-23；不代表所有页面或长期稳定性已验收。

## 如何收录

- 面向读者回答：做什么、适合谁、值得看什么、主要不足、最终建议。
- 用简短的“实际试用 / 有限试用 / 源码阅读”和日期说明依据，不把源码有实现写成体验已通过。
- 只发布有公共参考价值的结论；不写私人项目情况、源码去留、账号配置、文件比对、调试过程或清理记录。
- 不以项目数量或Star排名替代判断。相近方案可以合并比较，不为每个看过的项目凑文章。
- 链接原项目并尊重署名、代码与素材许可；个人Fork只作补充入口。
- 宗教资料须在索引标注“宗教资料”，正文开头提示涉及的宗教内容；介绍聚焦资料用途与来源。
- 结论注明日期，有新体验后再更新。欢迎通过Issue提供项目线索，正式推荐须有实际使用依据。

结论卡片建议格式：项目与来源、适合谁、主要价值、主要不足、最终建议、依据与日期。

维护检查：运行 `python3 scripts/check-content.py`，检查常见隐私模式、结论卡片边界和仓内文件链接。图片、事实与第三方授权仍需人工核对。

## 许可与致谢

本仓原创文字采用[MIT许可证](LICENSE)。第三方代码、截图、名称、商标和其他素材归各自权利人，遵循原有授权；本仓许可不改变第三方权利。

感谢项目作者与维护者。
