# Source-driven Graffiti Languages

涂鸦是来源驱动的视觉语言，不是新载体、滤镜或独立装饰系统。只使用 `FULL_FRAME_3_5`；图像模型不得生成可读文字，中文或英文艺术字由确定性排字完成，并可成为涂鸦构图中的明确层级。

## 1. Shared Source Contract

启用任一分支前建立最小 Graffiti Card：

- `Source fact`：原图中的动作、关系、环境结构、颜色或情绪证据。
- `Inferred relation`：只写证据支持的运动、张力、靠近、回应、时间或地点余韵。
- `Visual carrier`：来源轮廓、姿态、路径、影子、接触、重复节奏或识别色。
- `Composition function`：`HEROIZE_CORE`、`CONTINUE_MOTION`、`CONNECT_RELATION`、`BALANCE_WEIGHT`、`RETURN_COLOR` 或 `CREATE_EXIT`，只选一个主要功能。
- `Stopping boundary`：说明到哪里停止，避免第二故事、贴纸化或通用潮流模板。

任一字段无法填写则设置 `graffiti_language=OFF`。两种涂鸦不能共存，也不能与 `graphic_echo` 共存。

## 2. HARDCORE_STREET_GRAFFITI

把照片重构成高密度海报或时尚编辑画面。锁定 `space_mode=DENSE_EDITORIAL_FIELD`、`carrier=FULL_FRAME_3_5`。

### Structural transformation

以下五项至少完成三项，否则判定为滤镜化失败：

1. 重新裁切、放大或偏置核心，使其成为唯一英雄。
2. 压平或取消原摄影空间的完整景深关系。
3. 把环境压成一个来源明确的模板底印、喷漆轮廓、方向层或印刷大形。
4. 用重叠、遮挡或错位套色重建核心、记忆场与文字预留的层级。
5. 删除大部分摄影微纹理，只保留一至三个来源识别线索。

### Material grammar

只选择一个主材料包，最多加入一个弱辅助行为：

- `SPRAY_AND_STENCIL`：喷漆雾边、来源模板轮廓、一次不完整的干喷轨迹。
- `MARKER_AND_SCREENPRINT`：粗马克笔方向线、有限丝网墨层、一次来源形状内的错位套色。
- `PASTEUP_AND_DRY_BRUSH`：破碎纸边感、来源底印、粗粝干刷；保持平面作品，不生成真实墙面或粘贴 mockup。

底层核心仍选择 `ILLUSTRATION` 或 `DIGITAL_PAINTING` 作为主要转绘逻辑；涂鸦材料统一核心与记忆场，不能形成第三风格岛。

### Hierarchy and color

- 核心承担约 45%–60% 的视觉重量；保持最高对比、最锐利识别线索和最强局部色彩。
- 记忆场与材料层合计约 25%–40%；只保留一个主运动方向。
- 文字预留与其他痕迹保持次要，并留出一块低频视觉出口。
- 先使用来源主色、身份色和有色暗部，再允许加入一个高饱和强调色；不得使用无来源彩虹配色。
- 纯黑、脏白、酸性色或红色只能承担层级功能，不能自动成为“街头感”快捷键。

### Intensity

- `RESTRAINED`：一个主材料包、一次套色或喷漆行为，低频出口最大。
- `STANDARD`：一个主材料包加一个弱辅助行为，默认强度。
- `STRONG`：提高裁切、重叠和笔触张力，不增加新对象、标签或第二色系。

## 3. COLOR_PENCIL_INTERACTION

只在真正具有连续留白的作品中加入细彩铅作者边注。锁定 `space_mode=OPEN_SPACE`、`carrier=FULL_FRAME_3_5`；占用原 15%–30% 明确绘制预算，不追加新预算。

### Interaction contract

- 使用两至四种来源色或其低饱和邻近色；保持可见的铅芯颗粒、压力变化、断线和不均匀覆盖。
- 真实着色面积通常约 3%–10%，视觉重量低于记忆场，更低于核心。
- 必须通过接触、延续、回应、围合、牵引或配重与核心发生一次可见互动。
- 简笔小人必须明显是画面外的作者边注：平面、微小、不进入原场景透视，不暗示照片中新增真实人物或事件。
- 可以跨越较大留白，但必须稀疏、断裂，并保留至少一块连续安静基底。

### Interaction forms

- `MOTION_RESPONSE`：从身体、衣角、道路、水迹或视线延续一条断续运动线；不得改写实际运动方向。
- `RELATION_METAPHOR`：从接触、间距、共同方向或影子生长一个非标准的关系形态；不得使用现成爱心、emoji 或无证据亲密断言。
- `PLAYFUL_MARGIN`：用一个极小简笔人物或物件边注模仿、托住、指向或回应核心；不得形成第二主角或第二事件。

## 4. Typography

- 模型只生成无字艺术图；喷漆、模板和马克笔可形成不可读材料笔势，但不得伪造英文标签、品牌或杂志刊号。
- 硬核分支可选择 `DEFINITION_LINE` 或 `ART_LETTERING`。艺术字按 [lettering-engine.md](lettering-engine.md) 建立 Glyph Group Plan：先锁定整组材料、骨架、来源色和起转收笔，再分配单字角色与几何。
- 中文逐字、英文逐词合成；允许 `STACKED`、`VERTICAL`、`PATH_ALIGNED` 或 `COMPACT_BLOCK`。只有一个主字可承担强变形；最多一个来源记忆元素进入笔画、负形或书写路径。艺术字可以比定义句更大、更有对比，但必须与核心共享来源锚点、颜色和运动方向，并始终弱于核心。
- 彩铅分支可使用小号 `PENCIL_NOTE`，像作者边注一样与动作或关系互动；不得变成巨大标题或第二主角。
- 所有可读文字的输入必须是一条准确文本并由 `typeset_definition.py` 合成；视觉上可重排为字组。单字变形、切口、断线、旋转和错位套色都要计入安全边界。

## 5. Hard Avoids

- 在原照片上叠加喷漆、描边、颗粒或统一色罩而不重新构图。
- 通用 crown、flame、star、smiley、heart、arrow、无来源或不可读 tag、logo、二维码、条形码、坐标、裁切标或套准标。
- 用规则圆形、矩形、网格或重复色块承载涂鸦。
- 用纽约街墙、滑板贴纸或潮牌模板替代原图来源。
- 覆盖脸部、手势、接触点、身份色或必要识别线索。
- 让材料层形成第二人物、第二事件、第二故事或独立装饰海报。
- 因为空白而自动添加彩铅线，或因为题材都市而自动添加硬核涂鸦。

## 6. Gates and Corrections

同时通过：来源链完整；核心第一落点；外围不独立成画；媒介统一；颜色有因；文字可确定性排版；无模型文字与通用符号。

- `FILTER_LIKE_GRAFFITI`：重新裁切并压平空间，把同一来源环境转为印刷层；不要增加更多叠效。
- `GENERIC_STREET_STYLE`：删除通用标签和符号，换回可指出来源的轮廓、姿态、路径或颜色。
- `NOISY_HIERARCHY`：删除最弱材料层，恢复唯一英雄、主方向和低频出口；不要把所有层一起降透明度。
- `PENCIL_STICKER`：删除独立小图标，让线条从核心动作、关系或影子自然生长。
- `ADDED_EVENT`：移除会被误读为真实人物或事件的边注，改为明显平面且更小的作者互动。
- `TEXT_LIKE_NOISE`：删除模型笔迹中的伪字母、数字或标签，改用可验证的确定性艺术字承担文字。
