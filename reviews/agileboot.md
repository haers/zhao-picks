# AgileBoot：把业务校验写成可读的方法

[后端项目](https://github.com/valarchie/AgileBoot-Back-End) · [后端阅读版本](https://github.com/valarchie/AgileBoot-Back-End/tree/4e9ab30d68f2cb9dce6d9fc772456bcd106d575f) · [配套前端](https://github.com/valarchie/AgileBoot-Front-End)

## 适合谁

写过CRUD，希望进一步组织业务规则、应用服务和数据权限测试的Java开发者。

## 价值与不足

最值得读的是AddUserCommand、UserApplicationService和UserModel之间的职责，以及部门、部门树等数据权限的测试样例。把唯一性、关联存在和允许删除等规则写成明确方法，比只看分层目录更容易理解设计意图。

这不是与数据库完全隔离的领域模型：模型仍继承持久化实体、调用持久化服务，应用服务还操作缓存。名称约定的全局事务也要检查方法是否落在覆盖范围，不能只因叫DDD就照搬整套架构；现有测试文件不等于本次已经运行通过。

后端仍是Java8、Spring Boot2.7一代，前后端最近提交分别在2025年6月，不能称为近期高频维护。前端来自Pure-admin，使用Vue3、Element Plus、TypeScript与Pinia，路由、权限、HTTP和布局有配套约定；README引用的Pure-admin预览不能证明AgileBoot全栈功能。

前后端LICENSE标注MIT，但前端README另有二次开源需联系作者的说明。本文只链接原项目；需要再分发前端时应先厘清这些文字的适用范围。

## 结论

值得作为业务规则组织和数据权限测试的源码参考。推荐读具体方法与测试，不优先作为现代后台的整套底座，也不以配套前端的外观替代后端能力判断。

依据：固定版本源码、依赖及文档阅读，未构建、运行测试或验证全栈交互；2026-10-25。上游许可说明见原仓库。
