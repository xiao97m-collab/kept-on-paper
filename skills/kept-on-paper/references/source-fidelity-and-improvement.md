# Source Fidelity And Visible Improvement Gate

每次 `NEW_SOURCE`、用户纠正事实、选择空间路线和最终交付前都读取。本门优先于重构幅度、留白比例、媒介与标题：先保存这张照片不可替换的关系，再决定怎样转绘。

## 1. Source Evidence Card

在原有 Source Lock 内补齐以下字段：

```yaml
content_asset: {why_worth_preserving:, first_visual_anchor:, memory_carrier:}
scene_substrate: {type:, function:, indispensable:, may_become_bare_base:}
exact_marks:
  - {content:, kind: TEXT | LOGO | SIGN | SYMBOL, role:, reproduction_route:}
causal_palette:
  dominant_relation:
  light_source_and_time:
  material_response:
  identity_colors: []
  forbidden_drift: []
scale_and_view:
  subject_environment_ratio:
  viewpoint:
  framing_or_path:
  protected_geometry: []
transformation_budget: T0 | T1 | T2 | T3
visible_improvement_target:
```

- `scene_substrate` 记录让事件成立的连续环境，如水面、草坡、天空、窗洞、店面、光顶、道路或建筑框架。它不因低细节而自动成为可删除背景。
- `exact_marks` 记录可读文字、品牌标志、招牌与符号。颜色带不能替代 logo，近似字不能替代准确字。
- `causal_palette` 记录颜色如何由时间、光源、材料与面积关系产生；只列色名不足以保护原图味道。
- `scale_and_view` 记录小人物—大环境、框中框、长路径、透视顶棚等不可替换的空间关系。

若删除任一字段会使画面可被无关照片替换，该字段必须进入 `factual_invariants` 或 `forbidden_rewrites`。

## 2. Exact Mark Route

来源内的准确文字或品牌标志不是创作标题，不进入 `SHORT_TITLE → DEFINITION_LINE → OFF`：

1. 在无字基础画生成前锁定内容、拼写、结构、位置功能和安全区。
2. 优先使用用户提供或可验证的矢量/确定性文字结构重新绘制；禁止裁贴摄影像素。
3. 不让图像模型独立承担精确拼写或 logo 几何。若无法可靠重建，标为 `UNRESOLVED_EXACT_MARK` 并拒绝交付或请求资产；不得近似、改写或省略。
4. 最终放大核对每个字符、数字、部件和符号，再检查其与人物、物件和场景的层级。

## 3. Smallest Sufficient Transformation

全转绘不等于强制改变原构图。先选能产生可见增益的最小深度：

- `T0`：原图已成立，只需忠实转绘和材料统一。
- `T1`：保留主体—环境拓扑，调整裁切、尺度、局部层级、光色或干扰物。
- `T2`：合并部分环境、移动次要形体或改变面积比例，但保留场景基底、主要路径和尺度关系。
- `T3`：只有原构图明显阻碍内容、且前三级无法改善时，才允许重建主要拓扑或进入高密度编辑路线。

不按数量强制 Structural Delta。一个有用改变胜过三个破坏性改变；原图已有强框架、路径、天空、海面、草坡或光顶时，允许保留主要几何。只换媒介但没有可见增益仍失败，但“与原图差异不大”本身不是失败。

## 4. Breathing Field Is Not A White-Paper Quota

- 低信息呼吸区不等于裸露白纸。水面、天空、草坡、墙面、雾和连续光区都可以承担呼吸、尺度、方向或情绪。
- 只有 `scene_substrate.may_become_bare_base=true`，并且删除它不损伤地点、动作、尺度、方向、光色和品牌身份时，才允许 `OPEN_SPACE` 用裸露基底替代。
- 若环境本身是记忆载体，使用 `QUIET_FILLED_FIELD` 或保留一个来源原生低信息场；不能为了达到面积数字清空它。
- 留白重试不得只增加白纸。必须重新检查是否选错空间模式。

## 5. Internal Baseline Comparison

最终成品即使不向用户展示对比，也必须在内部同时查看：

1. 原图；
2. 简单裁切、层级或色彩修复能够达到的基线；
3. 转绘成品。

逐项回答：

- 内容是否仍明显属于这张原图？
- 第一视觉锚点是否更清楚？
- 场景基底、精确标志、因果色彩和尺度关系是否仍成立？
- 转绘是否增加了结构、材料、光色或记忆关系，而非只增加空白和风格？
- 换入一张无关照片是否必须重新设计？

任一答案为否，不得用“更简洁”“更艺术”或“差异更大”解释通过。

## 6. Visible Improvement Gate

`IMPROVEMENT` 只有在成品明显优于原图或简单基线时通过。下列任一项为致命失败：

- 事实、logo、可读文字、人物关系或动作消失。
- 水、草地、天空、窗框、店面、光顶等场景基底被无功能白纸或泛化背景替代。
- 原图主色关系、光源与材料味道被纸色或统一调色覆盖。
- 小人物—大环境、框中框、长路径或透视关系被改成普通主体摆放。
- 输出虽然不同，但没有更清楚、更好看或更值得记住。

失败时优先降低 `transformation_budget`、恢复来源关系并重选空间模式；不要继续增加装饰、标题或空白。
