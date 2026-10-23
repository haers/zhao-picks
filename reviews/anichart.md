# Anichart：动画算法值得读，不必再维护一套工作台

> 评估日期：2026-10-23；类型：源码选型评测。未安装、构建或实测视频导出，不作为开箱即用软件推荐。

Anichart 是用 TypeScript、Canvas 和 D3 构建的数据动画库。它能提供排名赛跑、地图及同画布组合的设计参考，但库与演示项目不等于带有数据编辑、作品管理和视频交付流程的完整产品。

本次判断是：保留这份评测和固定源码入口，退出旧源码副本，不建立个人 Fork 或第二套工作台。已有图表工作台时，真正值得比较的是少数动画算法；为了可能用到它们而保存整套旧工程，收益不够明确。

| 项目 | 信息 |
| --- | --- |
| 原项目 | [Jannchie/anichart.js](https://github.com/Jannchie/anichart.js) |
| 本次阅读基线 | [959b857727361fe59855e9b5cb1e1c031632c768](https://github.com/Jannchie/anichart.js/tree/959b857727361fe59855e9b5cb1e1c031632c768)，本地package版本3.2.4 |
| 已记录上游发布 | [v3.3.1](https://github.com/Jannchie/anichart.js/releases/tag/v3.3.1)，2023-09-21；此项来自当日此前的上游核对，本轮未重新联网查更新 |
| 许可 | [MIT](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/LICENSE)，提炼代码须保留署名和许可 |

## 能做到什么程度

[上游预览图](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/public/image/anichart-preview.png)展示柱状排名、时间折线、环图与同画布组合。本次已经查看这张原仓图片，但它是作者提供的示意效果，不是本次运行截图，也不能证明当前工程能直接启动或导出。

源码里值得阅读的三个具体点：

| 参考点 | 入口与机制 | 什么时候值得提炼 |
| --- | --- | --- |
| 名次交换平滑 | [BarChart](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/core/chart/BarChart.ts)预计算整个排名序列，再用归一化卷积核处理；[convolve](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/core/utils/convolve.ts)使用边界延拓 | 现有排名交换确有跳变，再比较视觉轨迹和预计算成本；它平滑的是名次轨迹，不能直接当作原始排名变化的精确时间 |
| 地图投影与镜头 | [MapChart](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/core/chart/MapChart.ts)与[KalmanFilter](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/core/utils/KalmanFilter.ts) | 确实需要世界地图投影或领先地区镜头跟随，再单独评估地理数据许可和镜头效果 |
| 多图编排 | [Stage](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/core/Stage.ts)、[Ani](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/core/ani/Ani.ts)与[示例](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/src/test/index.ts) | 确认要做地图＋排名等同步叙事时借鉴时间线组织，不因它存在就重做编辑器 |

卷积逐样本遍历核，时间成本约为序列长度乘核长度；BarChart还会为各实体建立历史排名序列。对大量实体、长时序和高帧率数据，要衡量预计算和内存，而不是只把“更平滑”当作无成本改进。本轮没有性能实测。

## 为什么不整包留下

已有图表工具能够满足常用绘图、编辑与导出需求时，仅增加常见柱赛跑或折线，没有足够的采用收益。数值插值与Anichart的排名卷积是不同处理对象，不能说“功能重复就完全没价值”，也不能因此认为必须引入整套库。

旧工程还有实际适配成本：示例引用的疫情CSV缺失，地图依赖远程GeoJSON，工具链与现代React项目有距离。旧README介绍内置FFmpeg导出，但[CHANGELOG](https://github.com/Jannchie/anichart.js/blob/959b857727361fe59855e9b5cb1e1c031632c768/CHANGELOG.md)已经说明v3移除了原渲染模块，不能照旧介绍承诺视频交付；[Remotion模板](https://github.com/Jannchie/anichart-remotion-template)是另一个需要单独验证的项目。

固定源码入口足以支持以后按需重新阅读，不需要为了可能用到的算法长期维护整套旧环境。

## 本轮停止点

本轮停在价值初筛：源码、已有能力和官方预览已经足以决定“不新增工作台、有限算法参考”。没有生成测试CSV、安装依赖、启动浏览器、升级旧工程或试跑视频导出，也没有因旧样例缺失就宣称整个库损坏。

如果以后出现具体动画问题，应拿同一组小数据比较现有实现与候选算法，通过实际视觉及性能检查后再决定采用。当前不建立待开发任务，不为保留源码寻找用途。
