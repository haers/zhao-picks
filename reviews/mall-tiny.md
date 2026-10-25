# mall-tiny：读懂Java后台的资源授权

[原项目](https://github.com/macrozheng/mall-tiny) · [3.x阅读版本](https://github.com/macrozheng/mall-tiny/tree/a97360ea48024dda576009553f588a86e9883db1) · [4.x分支](https://github.com/macrozheng/mall-tiny/tree/4.x)

## 适合谁

想学习Spring Security、JWT、Redis与MyBatis-Plus如何组成一个小型Java后台的开发者，尤其适合梳理用户、角色、菜单和接口资源的关系。

## 价值与不足

它把权限模块控制在较小范围内：角色分配资源、登录后加载权限、角色变更后清缓存，容易顺着一次请求阅读。3.x的AuthorizationManager还适合与旧版动态授权写法对照。

名称带mall，但它主要是账号与权限脚手架，没有完整商品、订单、支付流程。README展示的完整商城及配套前端是相关项目，不能当作mall-tiny已经具备的业务。运行需要数据库和Redis；它也不是OIDC认证服务或可直接嵌入任意页面的UI组件库。

默认master仍是旧技术栈，3.x与4.x另有Java17及较新的Spring Boot实现，2026年4月仍有版本升级。选分支时应看实际POM；这不能直接证明当前高频维护、所有依赖安全或整条授权链已经可靠。示例配置和权限策略需要按实际业务重新审视。

## 结论

值得收录为Java资源授权的学习参考。优先沿3.x固定版本阅读关键授权流程，再按运行环境比较4.x；不把它当完整商城或已经生产验证的安全底座。

依据：固定版本源码阅读及分支核对，未安装、运行数据库或验证在线业务；2026-10-25。上游Apache-2.0。
