# My-Blog Boot3与Layui版：两条Java单体博客学习路线

> 评估日期：2026-10-24；类型：源码对比。查看了项目自带截图并阅读业务实现，未安装、构建、登录或导入数据库；不作为生产可用推荐。

这两个项目都有文章、分类、标签、评论和后台管理，但适合学习的内容不同。Boot3版展示Spring MVC、Thymeleaf与MyBatis的单体链路；Layui衍生版展示另一套后台交互和MyBatis-Plus用法。不能把Layui版理解为同一套代码只换了Java版本。

## 先按学习目标选

| 维度 | My-Blog Boot3分支 | My-Blog Layui衍生版 |
| --- | --- | --- |
| 原项目 | [ZHENFENG13/My-Blog](https://github.com/ZHENFENG13/My-Blog) | [ZHENFENG13/My-Blog-layui](https://github.com/ZHENFENG13/My-Blog-layui) |
| 阅读基线 | [6956f02](https://github.com/ZHENFENG13/My-Blog/tree/6956f02359e88e326814453d8c2b1a804ddfb53f)，spring-boot-3.x | [0e0d8cf](https://github.com/ZHENFENG13/My-Blog-layui/tree/0e0d8cf35d9231fd7af86248e3c765d4b8797f2b)，master |
| 基线栈 | Java17、Boot3.1.0、Thymeleaf、MyBatis | Java8、Boot2.1.0、Layui、MyBatis-Plus3.1.1 |
| 更适合读什么 | 请求到数据库、文章保存、发布状态、服务端主题选择 | 列表筛选、开关、分页，以及MyBatis-Plus CRUD和标签关系 |
| 维护快照 | 该分支最后核对提交为2023-07-19 | 该分支最后核对提交为2021-08-29 |
| 许可 | Apache-2.0 | Apache-2.0；同时保留原作者及衍生作者署名 |

版本与维护日期来自2026-10-23的核对，本文未刷新远端。Boot3并不等于最新Boot版本；仓库推送时间也不等于所选分支有新功能。

## 文章保存的区别值得细读

Boot3版可从[BlogServiceImpl](https://github.com/ZHENFENG13/My-Blog/blob/6956f02359e88e326814453d8c2b1a804ddfb53f/src/main/java/com/site/blog/my/core/service/impl/BlogServiceImpl.java)阅读文章保存及关联数据处理。它的教学意义是把表单、业务服务和数据库调用串起来，不是证明所有边界都已正确实现。

Layui版的[BlogController](https://github.com/ZHENFENG13/My-Blog-layui/blob/0e0d8cf35d9231fd7af86248e3c765d4b8797f2b/src/main/java/com/site/blog/controller/admin/BlogController.java)先保存文章，再调用[标签关系服务](https://github.com/ZHENFENG13/My-Blog-layui/blob/0e0d8cf35d9231fd7af86248e3c765d4b8797f2b/src/main/java/com/site/blog/service/impl/BlogTagRelationServiceImpl.java)。后者有自身事务，但控制器没有用统一事务包住两步；保存还无条件重设createTime。学习时应区分“局部方法有事务”和“文章及全部关系原子保存”。本次没有通过真实数据库故障验证回滚。

## 界面能提供哪些参考

Boot3版[官方首页截图](https://github.com/ZHENFENG13/My-Blog/blob/6956f02359e88e326814453d8c2b1a804ddfb53f/static-files/index02.png)与[编辑器截图](https://github.com/ZHENFENG13/My-Blog/blob/6956f02359e88e326814453d8c2b1a804ddfb53f/static-files/edit.png)展示图文列表、侧栏及Markdown双栏编辑。多主题由服务端选择模板目录，不是可直接导入React项目的主题系统。

Layui版[文章列表截图](https://github.com/ZHENFENG13/My-Blog-layui/blob/0e0d8cf35d9231fd7af86248e3c765d4b8797f2b/static-files/blog-list.png)和[模板源码](https://github.com/ZHENFENG13/My-Blog-layui/blob/0e0d8cf35d9231fd7af86248e3c765d4b8797f2b/src/main/resources/templates/adminLayui/blog-list.html)可用于看分类/标题筛选、分页与状态开关。源码中的开关主要展示响应消息，未见完整失败回滚和请求异常收尾；截图也不证明手机可用。

这些是查看过的官方历史展示，不是本次运行截图。

## 两版共同需要留意

- 登录涉及MD5处理；不能直接作为新产品口令方案。Layui版旧密码校验还经过GET参数，需重新设计信息传递边界。
- 上传方法按原文件后缀、时间与随机数命名，所读方法内未见完整内容白名单；不能只靠扩展名判断文件可信。
- Markdown渲染方法未配置完整HTML转义或净化；具体内容入口仍须结合全链路审查。Layui评论存在escapeHtml4，不宜笼统说所有输入都未处理。
- Boot3版详情浏览量采用先读、加一、再更新的方式，不据此承诺并发统计可靠。

这是限定源码位置的观察，不是完整安全审计或已复现的运行漏洞。

## 结论

学习Java单体博客可优先按目标挑一个阅读，不必同时维护两套旧环境。需要现代产品后台时，这两版都不能仅凭页面完整或版本名称就直接采用。

两份SQL分别含69条、34条INSERT；已与各自保存的上游样例核对一致，Boot3整份SQL仅USE数据库名有差异。应把它们当初始化样例，以合成数据隔离试用，不能当成真实数据库备份。本次不新建个人Fork或部署服务，保留对比与固定入口。
