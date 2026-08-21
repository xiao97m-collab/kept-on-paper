# Expressive Title Lettering Engine

表现性标题是与记忆核心、记忆场共同设计的构图层，不是成图后的字体贴纸。普通路线在单段最终提示词中直接生成完整标题；本引擎只处理用户要求可复用/非破坏文字层、来源精确标志恢复，或直接生成字形失败且五分钟预算仍允许的条件式后处理。普通 `DEFINITION_LINE` 不进入本引擎。

固定顺序：

```text
读取已通过 Title Editor 的准确短标题
→ 判断是否值得启用标题
→ 从照片事实与构图选择一种字组视觉语言
→ 先规划整组外轮廓、断行与阅读顺序
→ 锁定统一 Glyph DNA
→ 分配单字角色与几何
→ 设计一个主笔画
→ 可选一个 Glyph–Memory Interlock
→ 分别选择书写材料与来源颜色
→ 生成并复核整组标题蒙版
→ 先通过 GLYPH_CORRECTNESS，再检查设计原创性
→ 确定性着色、定位与合成
→ 缩略图、可读性、来源与层级检查
```

## 1. Activation Gate

`ART_LETTERING` 不只属于涂鸦，但也不能因留白自动启用。必须同时满足：

- 短标题已经通过 `title-editor.md` 的事实回指、自然朗读、同一语义世界和过度解释检查；不得为了字形设计、长笔画或来源互锁重新文学化文案。
- 有不会覆盖脸、手、接触、动作和识别线索的标题区。
- 能提炼出中文 2–10 字或英文 1–6 词的准确短标题。
- 标题能承担 `HEROIZE_CORE`、`CONTINUE_MOTION`、`CONNECT_RELATION` 或 `BALANCE_WEIGHT` 中的一项。
- 至少有一个来自核心、动作、物件、路径、光线、影子或记忆场的交互依据。
- 加入标题后画面比无标题时更完整，而不是只显得更满。

任一条件不满足，关闭 `ART_LETTERING` 并改用 `DEFINITION_LINE`。只有 Title Editor 已证明短标题与定义句均失败时才 `OFF`；大面积留白本身不是启用或关闭文字的充分理由。

## 2. Expressive Title Plan

先把文字当成一个整体图形，不逐字随机美化：

```yaml
exact_text:
title_meaning:
visual_language:
title_zone:
line_count:
group_silhouette:
reading_order:
entry_and_exit:
image_relation:
visual_weight_target:
protected_regions: []
composition_function:
source_anchor:
glyph_dna:
material:
color_candidates: []
chosen_color:
primary_color_source:
color_reason:
accent_color:
color_roles:
hero_stroke:
interlock:
ornament_grammar: []
stopping_boundary:
```

- `group_silhouette` 先说明字组是横向舒展、上下错落、竖向生长、沿路径推进还是紧凑成团。
- `reading_order` 必须在非标准断行、错位和尺度变化后仍明确。
- `image_relation` 只选一个主要关系：`COUNTERWEIGHT`、`PATH_FOLLOW`、`EDGE_HOLD`、`FIELD_OVERLAP` 或 `QUIET_ANCHOR`。标题位置由核心、视线、动作、路径、记忆场边缘和低频区域共同决定，不默认居中。
- `visual_weight_target` 说明标题相对核心的重量；常规作品标题不得越过核心，硬核海报可与核心共同成为主层级。
- `protected_regions` 记录标题和长笔画都不可进入的区域。
- `stopping_boundary` 说明标题在哪结束，避免标题发展成第二幅画。

## 3. Visual Language Families

字组视觉语言是现有 `Glyph Group Plan` 的上游路由，只决定整组的轮廓、密度、节奏和图像关系；它不替代 `material`、`skeleton`、逐字角色、标题蒙版或确定性合成。每组只选一种，`AUTO` 必须从照片证据和构图需要选择，不能按题材标签随机轮换。

### RELAXED_NOTE_GROUP

适用于日常片刻、亲密关系、食物、小事件、自然呼吸感，以及 `OPEN_SPACE` 中轻量的作者回应。

- 细至中等粗细、松而不断的行距、允许轻微基线漂移和字宽差异；整体仍须形成一个可描述的外轮廓。
- 优先使用一处连笔、拖尾、括合或轻微上下错落来建立呼吸，不把每个字都做成不同手写体。
- 可与 `FOUNTAIN_PEN`、`PENCIL_NOTE`、轻量 `PAINT_BRUSH` 或克制 `BRUSH_INK` 组合。
- 禁止自动加入花朵、星星、箭头、对话框和英文小字来制造“手账感”。

### MODERN_WORDMARK_GROUP

适用于建筑、单一物件、清晰色块、安静现代空间和需要紧凑配重的构图。

- 统一字高、笔重、圆角或硬角逻辑，形成横向或近方形的紧凑字标。
- 可使用实心/空心、粗/细两级建立语义层级，但同一层必须共享结构，不逐字换字体。
- 至少一个关键字需要经过比例、负形、笔画连接或轮廓重构，避免直接成为现成圆体或黑体。
- 可与 `CUSTOM`、`COMPRESSED`、`WIDE` 骨架及 `CUT_STENCIL`、`DRY_MARKER`、`PAINT_BRUSH`、`OFFSET_SCREENPRINT` 组合。

### KINETIC_EDITORIAL_GROUP

适用于都市节奏、明显运动、道路或波浪方向、硬核涂鸦和高密度编辑画面。

- 整组共享一个倾斜方向、速度轴和尖锐或厚重的端点逻辑；断行必须沿同一动势推进。
- 允许字组与一次斜向承托形、错位套印或长引导笔画互锁，但这些必须从标题运动或原图路径生长。
- 可与 `DRY_MARKER`、`CUT_STENCIL`、`OFFSET_SCREENPRINT` 或强对比 `BRUSH_INK` 组合。
- 不用于安静、亲密或开放留白作品，除非原图本身存在足够明确的速度、冲突或方向证据。

### Family selection gate

选择前依次检查：照片的主动作与情绪 → 空间模式的密度 → 标题区形状 → 核心与记忆场的主方向 → 所需配重。若三种语言都不能自然接入现有构图，关闭 `ART_LETTERING`，不得为展示字形而改坏图片。

## 4. Unified Glyph DNA

同一字组只锁定一套视觉血缘：

- `material`：`CUT_STENCIL`、`DRY_MARKER`、`OFFSET_SCREENPRINT`、`BRUSH_INK`、`FOUNTAIN_PEN`、`PAINT_BRUSH` 或 `PENCIL_NOTE`。
- `skeleton`：`UPRIGHT`、`RUNNING`、`CURSIVE`、`COMPRESSED`、`WIDE` 或 `CUSTOM`。
- `entry_behavior`：共同的起笔角度、压力或喷边方式。
- `turn_behavior`：共同的硬折、圆转、顿挫、回锋或断裂逻辑。
- `exit_behavior`：共同的收笔、飞白、拖尾或套印结束方式。
- `stroke_contrast`：共同的粗细与压力关系。
- `edge_behavior`：共同的干湿、颗粒、切口、刷毛或渗漏。
- `proportion_system`：共同的字宽、字高、重心和封闭空间开放程度。
- `rhythm_system`：共同的字距、行距、倾斜方向和书写速度。

各字可有不同尺度、位置、倾斜和运笔动作，但不能各用一种字体、材料或色系。默认字体只允许作为不可见结构参考，不能直接成为最终表现性字形。

### Material behavior

- `CUT_STENCIL`：厚重骨架、真实桥接切口和有限缺损。
- `DRY_MARKER`：宽头马克笔或干水粉笔触、压力断痕和速度感。
- `OFFSET_SCREENPRINT`：完整主字与一次来源方向套印。
- `BRUSH_INK`：提按、飞白、墨量与收锋；整组统一为正楷、行楷或草书倾向。
- `FOUNTAIN_PEN`：细线、回锋、连续运笔和克制粗细变化。
- `PAINT_BRUSH`：可见刷毛、堆色与干刷边，不模拟书法墨韵。
- `PENCIL_NOTE`：轻微颗粒、重复描线和局部擦除，只用于开放留白边注。

## 5. Glyph Roles And Hero Stroke

逐字分配角色：

- `HERO`：最多一个，允许最明显的语义变形。
- `CONNECTOR`：最多一个，连接原图方向、主体或其他字。
- `SUPPORT`：保持稳定清楚，维持阅读。
- `TAIL`：负责收束字组或把视线送回图像。

每个单字记录：

```yaml
unit:
role:
scale:
rotation:
x_shift:
y_shift:
semantic_action:
protected_structure:
custom_mask:
extension:
```

- `scale` 为 `0.70–1.40`，`rotation` 为 `-15°–15°`。
- 强烈单字变形最多两个，但主笔画只有一个。
- `protected_structure` 标明不能破坏的关键笔画、部件或负形。
- 正楷、行楷、草书或完全设计字由整组骨架决定，不能逐字切换。
- “走”的末笔可沿真实行走方向伸长，“光”的撇捺可回应真实光源；只是为了酷而拉长不成立。

## 6. Material And Color Are Separate

先选书写材料，再独立选择颜色。不得把“普鲁士蓝钢笔字”固化成单一模板。

颜色候选按顺序评分：

1. `SOURCE`：是否来自关键物件、光线、衣服、环境或识别色。
2. `ZONE_CONTRAST`：在标题区域是否清楚，但不压过核心。
3. `MEANING`：是否匹配标题与记忆命题的情绪。
4. `HIERARCHY`：是否能平衡构图并维持唯一核心。
5. `PREFERENCE`：前四项接近时，才用胶片橙、普鲁士蓝、低饱和绿等个人偏好校准。

整组字只使用一个主色，最多一个小面积辅助色；颜色按角色分配，不按字符轮换：

- `GROUP_MAIN`：覆盖绝大多数有效笔画，建立统一字组。
- `SEMANTIC_ACCENT`：只强调一个关键词、一个笔画组或一次互锁。
- `MICRO_NOTE`：仅用于用户提供或事实明确的日期、英文或小型说明，视觉重量低于主标题；字形引擎不得自行补写这些内容。

辅助色只能用于一次套印、一个局部互锁或极短强调。禁止逐字换色、彩虹字和“每个字都有自己的性格与颜色”。

### Ornament grammar

括号、下划线、标签、气泡、花朵、星形、箭头和放射线不是默认装饰库。每个保留标记必须填写：

```yaml
source_or_reason:
function:
carrier:
placement_relation:
stopping_boundary:
```

`function` 只允许 `ENCLOSE`、`SUPPORT_BASELINE`、`POINT_TO_SOURCE`、`OPEN_OR_CLOSE_GROUP`、`CREATE_ENTRY` 或 `CREATE_EXIT`。同组最多使用一个装饰家族；删除后若不改变事实回指、阅读顺序或构图配重，就删除。照片里真实存在的花、道路、光线、叶片或波纹可以被压缩为标记，但仍受一个主互锁和一个主笔画上限约束。

## 7. Glyph–Memory Interlock

互锁让一个来源形态参与笔画、负形或书写过程，而不是把小插画塞进字里：

```yaml
source_element:
source_relationship:
interlock_mode:
glyph_index:
affected_stroke_or_space:
semantic_reason:
asset:
color_role:
entry_point:
exit_point:
legibility_invariants:
stopping_boundary:
```

只允许一种主要互锁：

- `STROKE_SUBSTITUTION`：来源路径替换一小段非关键笔画，删除不超过字框约 18%。
- `STROKE_CONTINUATION`：道路、影子、光线、水迹、枝条、蒸汽或动作轨迹从一笔继续。
- `COUNTERFORM_REVEAL`：来源轮廓或材质只在真实封闭负形中显露。
- `MATERIAL_TRANSFER`：雪、波纹、树影或玻璃折射限制在字形内部。
- `OCCLUSION_INTERLOCK`：来源形态只在一处从字前或字后经过。
- `GLYPH_TO_FIELD`：一笔离开字形并成为记忆场的一部分。

来源必须能在原图指出；不能覆盖识字关键结构；25% 缩略图先读字再感到关系；隐藏文字后，互锁不能成为独立插画。

## 8. Conditional Title Plate Contract

进入本条件分支后，表现性标题的最终轮廓来自一张整组标题蒙版，而不是逐字字体效果：

1. 基础艺术图保持无字并预留标题区。
2. 按 `Expressive Title Plan` 一次生成整组标题字形，保留断行、连笔和整体外轮廓。
3. 蒙版可为透明底、白底黑字或黑底白字；不得包含背景图片、阴影、渐变或多色材料。
4. 逐字对照 `exact_text` 和标准字形参考，放大检查缺字、错字、必要部件、关键笔画、粘连与阅读顺序；任何含混都在 `GLYPH_CORRECTNESS` 拒绝。
5. 通过脚本统一施加材料、颜色、不透明度、位置和一次可选互锁。
6. 标题有错只重做标题蒙版；不得重新生成基础艺术图。

允许字体骨架用于草拟结构，但不得在缺少合格标题蒙版时静默回退为字体成品。

## 9. Deterministic Plan Schema

旧的 `schema_version: 1` 逐字计划只保留为草稿分析兼容，不能通过最终排字入口。凡进入本后处理分支的 `SHORT_TITLE` 或 `PENCIL_NOTE`，都必须使用 `schema_version: 2` 和经过逐字复核的整组 `title_plate`；缺少蒙版时必须失败，不能回退为标准字体的缩放、旋转、套印或材料效果。本次新增的 `visual_language`、`image_relation`、`glyph_dna`、`color_roles` 与 `ornament_grammar` 均为可选描述字段：

```json
{
  "schema_version": 2,
  "group": {
    "visual_language": "relaxed_note_group",
    "material": "paint_brush",
    "skeleton": "custom",
    "source_anchor": "杯口、视线与墙上卡片形成的上升方向",
    "composition_function": "balance_weight",
    "entry_behavior": "短促干刷起笔",
    "turn_behavior": "圆转后保留刷毛断边",
    "exit_behavior": "末笔向杯口收束",
    "exact_text": "把今天慢慢喝完",
    "title_plate": "title-plate.png",
    "title_plate_mode": "dark_on_light",
    "plate_height_ratio": 2.4,
    "title_zone": "人物左上方的低信息墙面",
    "line_count": 2,
    "group_silhouette": "上短下长的两行舒展字组",
    "reading_order": "从左上进入，向右下结束",
    "image_relation": "counterweight",
    "visual_weight_target": "弱于人物面部，强于墙面卡片",
    "protected_regions": ["脸部", "双手", "杯口"],
    "primary_color_source": "饮料、木桌和橙色卡片",
    "color_reason": "来源明确，在灰白墙面清楚且保持温暖记忆",
    "glyph_dna": {
      "proportion_system": "中等字宽、开放负形、轻微重心错落",
      "rhythm_system": "同向右倾、上短下长、一个连续收笔"
    },
    "color_roles": {"group_main": "饮料棕橙", "semantic_accent": null, "micro_note": null},
    "ornament_grammar": []
  },
  "glyphs": [
    {"unit": "把", "role": "support", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0},
    {"unit": "今", "role": "support", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0},
    {"unit": "天", "role": "connector", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0},
    {"unit": "慢", "role": "hero", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0},
    {"unit": "慢", "role": "support", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0},
    {"unit": "喝", "role": "support", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0},
    {"unit": "完", "role": "tail", "scale": 1, "rotation": 0, "x_shift": 0, "y_shift": 0}
  ],
  "interlock": null
}
```

`title_plate` 相对路径以 JSON 所在目录为基准。`plate_height_ratio` 为整组蒙版相对基础字号的高度比例，范围 `0.75–4.0`。脚本验证计划与输入文字一致、材料一致、安全边界和最终像素范围。

## 10. Two-Stage Title Glyph Audit

每个进入标题蒙版分支的 `SHORT_TITLE` 在合成前必须依次通过“字形正确”和“定制设计”两门；直接随成品生成的标题也必须在最终 raster 逐字检查，但不要求先制作蒙版。

第一门必须保留：

```yaml
glyph_correctness_gate:
  exact_text:
  exact_unicode_sequence: []
  units:
    - unit:
      protected_components: []
      required_strokes_or_spaces: []
      missing_wrong_or_merged: []
      legible_at_100_percent: true
      legible_at_25_percent: true
      pass: true
  reading_order_pass: true
  overall_pass: true
```

- 以标准字形作为结构对照，只允许在不破坏关键部件、必要笔画和可读负形的范围内设计。
- 任一字符部件错误、缺笔、多笔、误并、与相邻字粘连或在 25% 尺寸产生歧义，`overall_pass=false`。
- `GLYPH_CORRECTNESS` 失败时立即重做标题蒙版，不进入风格、互锁或标准字体替代测试。
- 标准字体替代测试只能判断设计是否仍是字体思维，不能反向证明字形正确。

字形正确后再保留定制设计审核卡：

```yaml
title_glyph_audit:
  units:
    - unit:
      role:
      visible_custom_decision:
      source_or_group_relation:
      standard_font_difference:
  visible_source_interaction:
  color_or_position_only: false
  standard_font_substitution_test:
    closest_reference_font:
    attempted_equivalent_operations: [color, position, scale, rotation, texture]
    replaceable: false
    lost_design_evidence: []
```

- 逐字核对每个字符，而不只检查整组风格。每字必须记录一个可见定制决定；`SUPPORT` 字可以保持稳定字形，但仍须说明其比例、字距、重心、笔势或连接如何服务整组，不能只写“保持可读”。
- 至少一个字或主笔画必须与原图的动作、路径、边界、光线、影子、物件形态或人物距离产生可见结构关系。只从原图取色、把字放进留白区、靠近主体或选择相似情绪字体，均不算来源交互。
- 执行标准字体替代测试：用最接近的标准字体作为对照，允许对照做颜色、位置、整体缩放、整体旋转和统一笔刷纹理。若替换后仍保留近似的字组外轮廓、单字角色和画面关系，则标题仍是标准字体思维，必须拒绝。
- `title_plate` 由图像模型生成、看似手写、带飞白或笔刷颗粒，都不能自动通过；没有逐字差异证据和画面结构联系即失败。
- 审核不得从 JSON 计划或提示词反推成品合格；必须观察最终 raster 中真实可见的笔画和部件。
- `DEFINITION_LINE` / `CAPTION` 不进入本审核，可使用规整标准字体，但交付说明不得把它称为逐字设计标题。

`glyph_correctness_gate.overall_pass` 不是 `true`，或任一字符缺少设计审核记录、`replaceable=true`、`lost_design_evidence` 为空、`color_or_position_only=true` 时，`TYPE` 失败。只重做标题蒙版与排字，不重生基础图。

## 11. Quality Gate And Correction

- 是否先以最终 raster 通过 `GLYPH_CORRECTNESS`，逐字确认关键部件、必要笔画、负形、粘连与阅读顺序，而不是只核对计划文本？
- 文案是否逐字正确，断行和阅读顺序是否清楚？
- 是否已完成 `Title Glyph Audit`，并逐字确认角色、可见定制决定、来源或字组关系与标准字体差异？
- 标准字体替代测试是否明确失败；若只用颜色、位置、缩放、旋转或统一笔刷纹理就能替代，是否已拒绝标题？
- 是否至少有一个可见的来源结构交互，而非只有取色、靠近主体或占据留白？
- 整组外轮廓是否先于单字成立，并与核心、记忆场共同构图？
- 字组视觉语言是否由照片动作、空间密度、标题区形状和主方向共同支持，而非随机套用？
- 标题位置是否承担配重、顺势、边缘收束、路径延续或安静锚定，而非默认居中？
- 是否共享同一材料、骨架、主色与起转收笔逻辑？
- 是否只有一个主笔画、最多一个主互锁和最多两个强变形字？
- 颜色是否有来源、标题区对比和层级理由，而非只凭偏好？
- 是否没有默认字体感、逐字换色、无功能英文/日期、通用爱心/星星/箭头或字腔小插画？
- 每个装饰是否有来源或字组语法功能，且删除无效装饰后字组更清楚？
- 是否避开脸、手、接触点、动作和识别线索？
- 25% 缩略图是否可读，且核心仍是第一落点？
- 删除标题后作品是否成立；加入后是否确实加强记忆命题？
- 确定性合成是否保持标题遮罩外像素不变？

失败时按顺序修正：恢复准确字形、关键部件与阅读 → 完成缺失的逐字设计 → 通过标准字体替代测试 → 建立一个可见来源结构交互 → 修正或关闭字组视觉语言 → 重做整组外轮廓和位置 → 删除最弱变形与无效装饰 → 统一字形 DNA → 换回有来源且有对比的颜色 → 关闭互锁。只重做标题层，不通过描边、阴影、装饰符号或重生基础图掩盖失败。
