---
name: kept-on-paper
description: 将用户提供的真实照片完全转绘为具有纪念意义的 3:5 平面艺术作品。仅当用户明确调用 $kept-on-paper、纸上留存或 Kept on Paper 时使用；首次调用简要介绍用法，单图默认进入 PLAN 并给出三个有解释的来源驱动方向，用户也可选择 RANDOM 让 AI 直接决定并生成。支持持续修改；拒绝滤镜化、摄影像素和商业 mockup。
---

# 纸上留存 · Kept on Paper v2.18 Guided Entry Runtime

> 瞬间为核，事实不改；先选方向，一次成图；五分钟内完成。

把真实照片转绘成纪念性 3:5 平面艺术。不要滤镜化、抠图、复制完整摄影空间、套壳或装饰照片。

## 1. 接口

至少输入一张真实照片；缺图时请求补充，不从文字虚构原照片。

- `mode`: `GENERATE` / `ANALYZE`，默认 `GENERATE`。
- `workflow_mode`: `PLAN` / `RANDOM`，默认 `PLAN`；只有用户明确说“随机”“你决定”“直接帮我选”或等价表达时才进入 `RANDOM`。
- 载体固定 `FULL_FRAME_3_5`，最终 1200×2000 PNG。
- `space_mode`: `AUTO` / `OPEN_SPACE` / `QUIET_FILLED_FIELD` / `DENSE_EDITORIAL_FIELD`。
- `graffiti_language`: `AUTO` / `OFF` / `HARDCORE_STREET_GRAFFITI` / `COLOR_PENCIL_INTERACTION`。
- `primary_medium`: `ILLUSTRATION` / `OIL_PAINTING` / `CRAYON` / `WATERCOLOR` / `GOUACHE` / `DIGITAL_PAINTING` / `CHINESE_PAINTING`；`support_medium` 最多一种或 `NONE`。
- `surface`: `AUTO` / `IVORY_ART_PAPER` / `PURE_WHITE_DIGITAL` / `COOL_WHITE_COTTON` / `LIGHT_TONED_PAPER` / `WHITE_GESSO_CANVAS`。
- `color_direction`: `AUTO` / `SOURCE_LED` / `LOW_SATURATION` / `FILM_ORANGE` / `PRUSSIAN_BLUE` 或用户指定。
- `text_mode`: `AUTO` / `USER_TEXT` / `OFF`；`text_role`: `AUTO` / `DEFINITION_LINE` / `TITLE_PLUS_LINE` / `ART_LETTERING` / `OFF`。

输出最终 PNG 与简短中文说明。`ANALYZE` 只交付三个方向或选定方向的精简 Transformation Specification，不生图。

## 2. 首次引导与工作模式

运行时无法可靠读取“刚安装”这一系统事件，因此用“当前对话第一次调用本 Skill”同时覆盖第一次安装后的使用与第一次引用。首次调用时先用 2–3 句完成一次 onboarding；同一对话后续不重复。

推荐话术保持简单：

> Kept on Paper 会把你提供的真实照片完整转绘为 3:5 纪念艺术，保留人物、关系、场景和关键颜色，不做滤镜或拼图。发一张照片即可：默认使用 Plan，我会给出三个有解释的方向；也可以说 Random，由我直接选择并生成。完成后还可以继续告诉我新的想法，我会沿用这张照片持续修改。

- 首次调用但没有图片：介绍后请求用户发送一张真实照片，并说明可选 `PLAN` 或 `RANDOM`。
- 首次调用已经带图：介绍后立即执行所选模式，不要求重新上传或增加确认。
- 用户未提模式：使用 `PLAN`，不能暗中改成 `RANDOM`。
- `RANDOM` 不是无约束随机风格；它表示 AI 根据 Source Lock、可见增益和风险门选择自己认为最好的一个来源驱动方向，并直接生成。

### PLAN（默认）

建立 Source Lock 后，输出恰好三个真正不同的 Direction Card 并等待用户选择。用户可选择 `1/2/3`、同时选择多个方向，或要求合并、删改；选择前禁止生成。

每张 Direction Card 只写：

- `保留`：不可改变的视觉关系与事实。
- `主要改动`：构图、信息层级、空间或材料怎样改变。
- `路线`：列出转绘深度、空间模式、构图骨架、主媒介和文字倾向，并用普通中文解释它们对这张图意味着什么。
- `预期效果 / 主要风险`：各一句。

重要术语第一次出现时必须就地解释，不能假设用户理解代码名：

- `T0`：忠实转绘，基本不改结构。
- `T1`：保留主构图和关系，只调整裁切、层级、光色或材料。
- `T2`：中度重组，可合并或移动次要形体，但保护主路径、尺度和场景基底。
- `T3`：大胆重构主要空间或拓扑，但人物、动作、关系、路径和因果色等来源事实仍不能改。
- `OPEN_SPACE`：大面积真实纸面留白；只有环境可安全删除时使用。
- `QUIET_FILLED_FIELD`：环境仍然存在，但大部分区域降低信息密度、保持安静。
- `DENSE_EDITORIAL_FIELD`：高密度编辑海报场，只用于唯一英雄清楚的编辑/涂鸦路线。
- `PAINTERLY_DISTILLATION`：用绘画材料压缩摄影细节。
- `INTERACTIVE_LINE`：在安全留白中用来源线条回应动作或关系。
- `EDITORIAL_GRAFFITI`：把来源结构重组为高密度编辑或涂鸦海报。

每次只解释当前卡片实际使用的术语；不要粘贴完整术语表或写成长篇教学。

### RANDOM

建立同样严格的 Source Lock，但不输出三张 Direction Card、不等待方向确认。内部评估安全路线后选择一个最有可见增益的方向，写入 Generation Lock，直接编译单段提示词并生成一张成品。交付说明中用一句话告诉用户 AI 选择了什么方向及原因。

## 3. Fast Runtime Router

- `NEW_SOURCE`：首次读取照片并建立 Source Lock；`PLAN` 输出三个 Direction Card 后停止，`RANDOM` 直接选择并生成。
- `SELECTED_DIRECTION`：用户选定或调整一个方向；锁定后进入生成。
- `REUSE_SOURCE`：同一照片且事实未变；复用 Source Lock 与已选方向，只重算用户改变的字段。
- `ANALYZE_ONLY`：只分析，不读取生成与排字执行细节。

只按需读取 reference，不为“完整”预加载：

| 条件 | 读取 |
|---|---|
| `NEW_SOURCE`、事实纠正或最终审核 | [source-fidelity-and-improvement.md](references/source-fidelity-and-improvement.md) |
| AUTO 冲突或回退 | [auto-routing.md](references/auto-routing.md) |
| 空间或基底改变 | [surface-and-space.md](references/surface-and-space.md) |
| 媒介改变 | [medium-library.md](references/medium-library.md) |
| 色彩改变 | [palette-system.md](references/palette-system.md) |
| 文案生成/改写 | [title-editor.md](references/title-editor.md) |
| 文字角色、位置、字形 | [typography-and-language.md](references/typography-and-language.md) |
| 条件式艺术字后处理 | [lettering-engine.md](references/lettering-engine.md) |
| 载体、裁切或安全区异常 | [carrier-contracts.md](references/carrier-contracts.md) |

用户明确选择涂鸦或 AUTO 产生候选时才读对应 graffiti / graphic-echo reference。稳定脚本只调用 `--help` 获取参数；已锁定字段不重读 reference。

## 4. 不可改变的合同

- 全部内容转绘；不保留、粘贴或混合摄影像素。
- 只有一个记忆核心、一个主记忆场、最多一个过渡痕迹、一个来源图形回声、一个证据充分的隐喻和一个创作文字模块；文字模块可为单独标题、单独短句，或语义不重复的“标题 + 一小句话”。
- 每张作品只使用一种主要视觉语言：`PAINTERLY_DISTILLATION`、`INTERACTIVE_LINE` 或 `EDITORIAL_GRAFFITI`。
- 身份、年龄感、数量、动作、手势、接触、朝向、距离、尺度、路径、关键色和精确标志属于事实。
- 水面、草坡、天空、道路、建筑框架、光场、可读文字、logo、招牌或符号若承担地点、尺度、路径、因果色彩或身份，禁止删除。
- 使用能产生可见增益的最小转绘深度；与原图差异大不是质量指标。原构图已成立时优先 `T0/T1`。
- 禁止新增人物、动物、建筑、道具、天气、事件或无证据关系；禁止改写事实的镜像。
- 只输出平面作品；禁止桌面、墙面、唱机、手持、投影、包装和商业 mockup。

## 5. Source Lock

`NEW_SOURCE` 只建立最小运行卡，不写长篇日志：

```yaml
memory_thesis:
core: {recognition_cues: [], factual_invariants: []}
content_asset: {first_visual_anchor:, memory_carrier:, why_worth_preserving:}
scene_substrate: {type:, function:, indispensable:, may_become_bare_base:}
exact_marks: []
causal_palette: {dominant_relation:, light_source_and_time:, identity_colors: [], forbidden_drift: []}
scale_and_view: {subject_environment_ratio:, viewpoint:, framing_or_path:, protected_geometry: []}
memory_field: {source:, memory_carried:, primary_form:, recognition_cues: []}
transformation_budget: T0 | T1 | T2 | T3
visible_improvement_target:
forbidden_rewrites: []
```

不能确认的事实写 `UNKNOWN`。核心必须包含承载命题所需的关系、接触、场景基底、路径、色彩、尺度与框架，而不只是显眼物体。只有源文件、事实纠正或核心命题改变时才重建 Source Lock。

## 6. PLAN 选择门

每个 `NEW_SOURCE + PLAN` 必须先输出恰好三个编号方向并等待用户选择；选择前禁止编译最终提示词、调用图像生成、制作字牌或输出假定成品。`RANDOM` 按第 2 节显式绕过此门，但不能降低 Source Lock、事实保护或质量检查。

三个方向共享 Source Lock，但在改动目标上真正不同，不能只替换媒介名、色名或标题。三个方向都必须安全、好看且有来源证据，不塞入劣质方向充数。用户可选 `1/2/3`、同时选择多个方向，或提出合并、删改；只有选择明确后才进入 `SELECTED_DIRECTION`。

## 7. 五分钟硬预算

读取原图到交付成品的主动思考、reference 读取、提示词编译、图像调用、检查与载体整理累计不得超过 300 秒；用户等待选择的时间不计。

- `NEW_SOURCE + PLAN → 三方向`：60 秒；Source Lock 最多 20 秒，三个方向最多 40 秒。
- `NEW_SOURCE + RANDOM → 最终交付`：300 秒；Source Lock 与方向选择 35 秒，最终提示词 35 秒，首次图像生成 120 秒，最终检查 45 秒，载体整理与交付 65 秒。
- `用户选择 → 最终交付`：240 秒；方向锁定与标题判断 35 秒，最终提示词 35 秒，首次图像生成 120 秒，最终检查 25 秒，载体整理与交付 25 秒。

每层到时立即采用当前最小充分判断，不继续扩写卡片、重读未变 reference 或追求轻微优化。外部图像调用超过分层预算时不再追加调用；到 300 秒仍未完成就停止并如实报告。只有致命失败且总预算至少还剩 90 秒时允许一次定向重试，否则交付 `REJECTED` 或说明超时。

## 8. AUTO Route 与 Generation Lock

安全基线为 `PAINTERLY_DISTILLATION`。只有 `OPEN_SPACE` 成立、关系明确且线条不覆盖事实时才候选 `INTERACTIVE_LINE`；只有用户明确要求，或照片同时有强都市/海报节奏、可压平结构、唯一英雄和视觉出口时才候选 `EDITORIAL_GRAFFITI`。冲突、证据不足或判断相持时回退安全基线，不得用混合风格折中。

空间淘汰门：只有 `scene_substrate.may_become_bare_base=true` 且删除环境不损伤地点、尺度、路径、因果色彩或核心关系时，才选 `OPEN_SPACE`；环境不可缺时选 `QUIET_FILLED_FIELD`；`DENSE_EDITORIAL_FIELD` 只随 `EDITORIAL_GRAFFITI` 成立。

用户选择后填写一次内部 `Generation Lock`：

```yaml
generation_lock:
  direction_id:
  route: {transformation_budget:, space_mode:, visual_language:, composition_skeleton:}
  art: {primary_medium:, support_medium:, surface:, color_roles: {dominant:, support:, accent:}}
  protected: {scene_substrate:, exact_marks: [], causal_color_signature:, scale_relation:}
  composition: {core_zone_and_scale:, memory_field_form:, visible_improvement_target:}
  title_route: {need:, content_role:, title_text:, support_line:, visual_role:}
  eliminated_routes: []
  fatal_risks: []
```

后续只更新用户改变的字段及直接依赖项；不得借机重选核心或改变其他已选方向。

## 9. 选择后执行

```text
复用 Source Lock 与用户选定方向
→ 写入 Generation Lock
→ 锁定 3:5、最小转绘深度、空间、构图、媒介与因果色彩
→ Title Editor 决定 SHORT_TITLE、DEFINITION_LINE、TITLE_PLUS_LINE 或 OFF
→ 独立决定 HERO_TITLE、SUPPORT_TITLE、CAPTION 或 NONE
→ 将画面与可选文字编译进同一段最终提示词
→ 以原图为唯一事实母本调用一次图像生成，直接得到完整成品
→ 对照原图、简单基线与成品检查
→ 仅致命失败且预算至少剩余 90 秒时重试一次
→ 整理 1200×2000 载体并交付
```

方向选定后，或 `RANDOM` 已完成内部选择后，由 AI 自动补全未指定参数，不再增加逐项选择题或生成前确认轮次。

## 10. 构图、空间、材料与颜色

构图骨架只选一个：`RELATIONAL_TRIANGLE`、`DIRECTIONAL_SWEEP`、`SMALL_ANCHOR_VAST_FIELD`、`ASYMMETRIC_FRAME`、`CENTRAL_TENSION`。锁定核心区域/尺度、视线入口、记忆场连接、反侧配重和眼睛出口。原图关系成立时少改；只有层级确实受阻才进入 `T2/T3`。

- `OPEN_SPACE`：约 70% 以上为连续真正裸露基底；水、天空、草坡、墙面、道路或光场承担命题时不得选择。
- `QUIET_FILLED_FIELD`：允许高覆盖，但至少约 70% 为来源原生低信息场；不能只是整图低对比滤镜。
- `DENSE_EDITORIAL_FIELD`：只随编辑涂鸦使用，保留唯一英雄和一个低频出口。

使用一种主媒介与最多一种辅助媒介。媒介服务信息层级，不按题材套风格。先保护因果色彩关系、光源、主色面积、身份色和有色暗部，再决定降饱和或强化；纸色不得成为新主色。

## 11. 文字

文字与画面默认进入同一段最终提示词、同一次图像生成。先按 [title-editor.md](references/title-editor.md) 使用 `SHORT_TITLE → DEFINITION_LINE → OFF` 的基础回退链；短标题成立且补充句能提供不重复的情绪余味时，可升级为 `TITLE_PLUS_LINE`。事实是文案起点，不是字面终点；非字面表达必须具备可完整回溯的 `Fact Trace`，并严格禁止替人物虚构经历、关系、动机、地点、日期或人生故事。再独立选择视觉角色。

内部 `Title Route Card` 只保留会影响成图的字段：

```yaml
title_route: {need: SHOULD_TITLE | OPTIONAL | OFF, content_role: SHORT_TITLE | DEFINITION_LINE | TITLE_PLUS_LINE | OFF, title_text:, support_line:, visual_role: HERO_TITLE | SUPPORT_TITLE | CAPTION | NONE, safe_title_zone:, composition_function:, scale_reason:}
```

`SHORT_TITLE` 先检查 `HERO_TITLE` 与 `SUPPORT_TITLE`，有具体失败证据才回退 `CAPTION`。多图中超过约 75% 为 `OFF`，或超过约 75% 都是 `CAPTION` / 统一小字时逐张复核，但不按配额强加文字。

最终 raster 先通过 `GLYPH_CORRECTNESS`，再做 `Title Glyph Audit`：逐字确认可见定制决定、来源结构交互和标准字体差异；标准字体替代测试不能反向证明字形正确。直接生成是默认路线。只有用户要求可复用/非破坏文字层、来源精确标志需确定性恢复，或直接生成失败且预算允许时，才升级到 `lettering-engine.md` 的 `schema_version: 2 title_plate`；本条件包括 `PENCIL_NOTE`，但不是普通短标题的默认税。

`SOURCE_EXACT_MARK` 不是创作标题。精确标志缺失或近似即失败；无法验证时拒绝交付，不得省略、改写或用相似颜色代替。

## 12. Single-Prompt Compiler

方向选定后只编译一段最终提示词，目标 220–450 个英文单词，硬上限 600；不要输出 Skill 原理、完整决策日志或重复禁令。固定六块：

1. `Source Truth`：不可改变的关系、场景基底、尺度、路径、因果色彩与精确标志。
2. `Visual Proposition`：这张照片独有、需要放大的一个视觉句子。
3. `Recomposition`：3:5、T0–T3、空间模式、构图骨架、信息层级和最小 Structural Delta。
4. `Material & Color`：媒介边缘、笔触、纸面行为与来源色角色。
5. `Typography`：若有文字，分别写入准确标题与可选短句、两者语义职责、位置、尺度、字形气质和禁止覆盖区；无字明确 `no text`。
6. `Avoid`：只列本图高风险，并包含 `no photography, no style-only repaint, no invented background, no deletion of protected scene substrate, no altered scale relation, no added subjects, no watermark, no signature`。

原图始终是唯一事实母本。不得把失败候选升级为新的主要编辑对象；致命失败时回到原图，只修改失败字段并重编完整提示词。

## 13. 生成、交付与持续修改

默认一次图像生成，直接得到包含可选文字的完整作品；不先做无字底图、字牌或拼图。按以下九门快速检查最终 raster：

1. `FACTS`：身份、数量、动作、方向、可读文字、logo 与符号真实。
2. `CORE`：25% 缩略图与灰度图首先看到核心并能对应原图。
3. `FIDELITY`：场景基底、尺度、视点、框架/路径和因果色彩仍成立。
4. `RECOMPOSITION`：改变处于所选 T0–T3 且改善层级；滤镜式重画或强改好构图均失败。
5. `FIELD_SPACE`：环境不因留白消失；高密度路线仍有唯一英雄和出口。
6. `CARRIER`：1200×2000、3:5 平面作品，无 mockup。
7. `ART_COLOR`：媒介、纸面、色彩面积、光源和材料响应有来源。
8. `TYPE`：文字准确、可读、角色与层级正确；错误不因设计感通过。
9. `IMPROVEMENT`：内部并看原图、简单裁切/色彩修复基线与成品；必须更清楚、更好看或更值得留下。仅更空、更不同或更有风格不能通过。

只有致命失败且五分钟总预算至少还剩 90 秒才允许一次定向重试；时间不足直接 `REJECTED`，不得以字牌、拼图或连续生成绕过预算。最终只交付通过硬门的 PNG 与简短说明，不展示过程稿或用说明合理化失败。

每次成功交付后必须用一句简短话提醒用户可以继续修改，例如：

> 如果还有新想法，可以继续告诉我，例如更抽象、更留白、更大胆、换文案、换字体，或只改颜色；下一轮会复用这张照片的 Source Lock，只修改你提出的部分。

后续修改进入 `REUSE_SOURCE`：

- 用户给出具体修改时，直接更新相关字段与必要依赖并生成，不要求重新开始或再次选择模式。
- 用户只说“再换一种”“再大胆些”等宽泛要求时，默认给出三个精简的后续方向；若用户同时说 `RANDOM`、“你决定”或等价表达，则由 AI 直接选择并生成。
- 不改变用户未提及的事实、已确认文字或已锁定方向；只有修改目标确实依赖这些字段时才联动更新，并在交付说明中点明。
