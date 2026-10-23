# RuoYi Blog：记账与时间线值得参考，暂不采用整站

> 评估日期：2026-10-24；类型：源码选型评估。未安装、构建、登录或进行浏览器交互验收，不作为开箱即用软件推荐。

RuoYi Blog 在博客之外加入了记账、时间线、便签和文件管理。它适合需要研究这些功能如何落到 Java 单体应用的人；如果已有内容管理或文件服务，仅为常见博客功能再维护一套环境，收益有限。

本次结论：保留功能与固定源码入口，目前不采用整站，也不建立个人 Fork。这个取舍针对当前需求，不代表项目没有维护或这些功能没有价值。

## 来源、版本与许可

| 项目 | 信息 |
| --- | --- |
| 原项目 | [GiteeKey/ruoyi-blog](https://gitee.com/GiteeKey/ruoyi-blog) |
| 本次源码阅读基线 | [48ac7f7](https://gitee.com/GiteeKey/ruoyi-blog/tree/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd)，master，提交日期2026-10-22 |
| 基线技术栈 | 项目4.8.3、Java 8、Spring Boot 2.5.15、Shiro 1.13.0；来自该版本pom，不代表最新依赖组合 |
| 上游建议的稳定分支 | [v4.8.0-mysql固定版本](https://gitee.com/GiteeKey/ruoyi-blog/tree/c5568c7e421f8e9e45d0225ac7251cea7b719bae)，2025-01-20；与上述master不是同一版本 |
| 许可 | [基线根LICENSE](https://gitee.com/GiteeKey/ruoyi-blog/blob/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd/LICENSE)为MIT，保留RuoYi署名；引用组件与素材仍须分别核对其许可 |

上游提交和分支信息于2026-10-23查询，本文整理时没有重新联网确认后续更新。上述固定版本用于复查判断，不承诺它是部署时的最新或最合适版本。另有SQLite适配分支，上游说明部分功能未完成，本次没有试用。

## 能做到什么

| 功能 | 源码体现的能力 | 使用前仍需验证 |
| --- | --- | --- |
| 博客 | 文章、分类、标签、归档、评论及Markdown目录，另有密码页面与静态化处理 | 密码校验是否覆盖详情和静态文件等全部访问路径，评论流程及移动端阅读 |
| 记账 | 收支账户、月度汇总、分类分析和日历数据；统计使用BigDecimal，并有按当前用户查询的调用 | 账户授权、用户隔离、余额一致性，以及导入、备份与恢复是否满足实际需要 |
| 时间线与便签 | 主时间线、明细、便签和看板的增删改查 | 私有与共享范围、权限以及完整编辑流程；createBy字段本身不证明隔离成立 |
| 文件管理 | 分片探测、上传与合并，有实际服务端实现 | 文件权限、合并失败恢复和部署目录边界 |
| 个人主页 | 风景、时钟、天气和站点卡片 | 外部天气服务可用性及手机布局，不能由宣传图推断可靠性 |

以上是源码能力说明，不是逐项实测通过。尤其是记账：统计方法使用BigDecimal、调用当前用户查询，只证明存在这些实现，不足以证明整个账务流程或权限安全。

## 值得阅读的入口

- [AccountBillServiceImpl](https://gitee.com/GiteeKey/ruoyi-blog/blob/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd/src/main/java/com/ruoyi/project/emmanuel/account/service/impl/AccountBillServiceImpl.java)：月度收支、分类汇总及日历数据组织。适合比较统计模型，不把展示统计直接当成完整账务系统。
- [TimeLineMServiceImpl](https://gitee.com/GiteeKey/ruoyi-blog/blob/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd/src/main/java/com/ruoyi/project/emmanuel/memorial/service/impl/TimeLineMServiceImpl.java)：主时间线的业务组织，可结合控制器与Mapper继续阅读权限和查询条件。
- [BoardNoteController](https://gitee.com/GiteeKey/ruoyi-blog/blob/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd/src/main/java/com/ruoyi/project/emmanuel/memorial/controller/BoardNoteController.java)：便签看板操作入口，适合有明确个人记录需求时进一步选型。

[官方主页截图](https://gitee.com/GiteeKey/ruoyi-blog/blob/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd/doc/homepage.png)和[官方文章截图](https://gitee.com/GiteeKey/ruoyi-blog/blob/48ac7f74cb9b3bd44c1d702e388b9c1ebeb532fd/doc/article.png)已查看，但图片本身是历史展示。它们不能证明上述基线已成功运行，也不证明天气接口、手机页面或登录流程可用。

## 为什么目前不采用

博客、评论和文件管理属于常见能力，当前没有必须引入这套应用才能解决的问题。记账月历与时间线更有辨识度，但尚未形成具体需求；为可能用到的功能先维护整站、数据库和定时任务，不是必要投入。

如果以后确实要做个人记账或时间线，再从当时适用的固定分支开始，以合成数据验证准备采用的那条流程。先验证权限和数据保存，再看统计、交互及备份恢复，不因源码里存在菜单或实体就认定整套功能可用。

## 本次验证边界

本次依据固定源码、版本记录及官方截图进行选型判断，在价值初筛后停止。没有安装依赖、连接数据库、启动定时任务、接入真实账号或验证部署。文章不包含私人配置、账号、业务数据或运行凭据，也不提供整包源码镜像；源码与更新请从上游获取。
