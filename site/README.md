# 网站维护

GitHub Pages使用Jekyll与[Just the Docs 0.12.0](https://github.com/just-the-docs/just-the-docs/releases/tag/v0.12.0)（MIT）。相比博客主题Minima，它的搜索、侧栏及文章导航更适合精选目录。

## 内容与生成

README.md中的两张索引表、reviews/*.md仍为唯一内容源。网站首页、项目目录、选型专题、索引中的详情由scripts/prepare_site.py生成到忽略的work/site-src；不手工编辑生成目录。配置在根_config.yml，主题补充样式及标识在site目录。

只有索引中已收录的正文、公开图片、主题配置及展示文件进入生成目录；AGENTS、脚本、测试、工作文件不发布。Markdown相对链接构建时转换成带baseurl的网页地址；GitHub里仍保持原.md链接。

保留主题导航与阅读布局，沿用Just the Docs原生紫色（light主题的$link-color，当前为#7253ed），不另外覆盖为绿色。正文、标题、侧栏和表头回到主题中性色，紫色只用于链接、选中与焦点等强调。站点图标使用紫底白色展开书本，与页头标识、apple-touch和分享图保持一致；图标资源URL带版本参数，避免浏览器继续复用旧绿色标识。

关闭主题默认英文分词搜索，使用对公开文章的中文/英文子串匹配；搜索索引随构建生成，不上传查询、不持久保存历史、不调用外部服务。没有引入前端应用框架。

网站首页只保留介绍和主题原生“浏览项目 / 选型专题”按钮，完整表格分别放在对应目录；GitHub README继续保留完整索引。详情只使用主题原生面包屑，点击页头标识返回首页。目录依据列及详情标题下使用原生label，逐字复用README依据；紫色表示包含源码阅读依据，蓝色表示试用依据，不把配色当作推荐等级。

新增项目只需新增reviews文档并更新README索引，构建即生成导航与页面。移动资产时保留原文相对路径，检查器会拒绝越界或失效链接。源文件通过Liquid raw保护，不把文章内Liquid示例当模板执行。

## 构建与验收

Ruby使用3.4系列，Bundler依赖由Gemfile.lock锁定。不要使用macOS自带旧Ruby。

```sh
BUNDLE_PATH=work/bundle bundle install
python3 scripts/check-content.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/prepare_site.py
BUNDLE_PATH=work/bundle bundle exec jekyll build --source work/site-src --destination work/site
python3 scripts/check_site.py
```

本机预览：在仓根运行`python3 -m http.server 8431 --bind 127.0.0.1 --directory work/preview`，先将work/site复制到work/preview/zhao-picks，让子路径与线上一致。浏览器验收运行`npm ci && npm run test:site`；复用系统Chrome隔离实例，不下载浏览器。图片、截图与临时报告位于忽略的work，不附用户资料。

检查包括当前索引中的项目与专题均可从目录进入、详情返回导航、404、搜索、桌面1280/手机390布局、链接与资源均在/zhao-picks/路径下。数量按当前索引自动统计，不在构建器里写死。

当前主题构建会产生上游Sass旧接口弃用提示，未出现构建错误；不通过修改第三方源码或隐藏错误代替验证。主题升级时复核兼容性再更新Gemfile.lock。

## 发布

GitHub Pages使用Actions部署，工作流只上传work/site。推送main触发检查/构建/部署；PR只构建，不发布。Pages设置选择GitHub Actions。默认站点为https://haers.github.io/zhao-picks/，无需改仓库名或绑定域名。

维护说明与验收流水不进入读者网站；实际执行证据保留work或本地Archive。发布前复核实际暂存文件与远端提交，仓内公开文档规则仍适用。
