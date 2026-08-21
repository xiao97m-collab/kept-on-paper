# Typography and Definition Language

文字为作品提供作者判断与视觉配重。先由 [title-editor.md](title-editor.md) 决定文案内容与 `SHORT_TITLE`、`DEFINITION_LINE`、`TITLE_PLUS_LINE` 或 `OFF`；再独立选择 `HERO_TITLE`、`SUPPORT_TITLE`、`CAPTION` 或 `NONE`。普通路线把文字与画面一起写入最终提示词并直接生成；本文件同时保留高风险文字的确定性后处理合同。不能为了适配艺术字效果而把准确文案改得更夸张，也不能把所有成立的标题统一缩成定义小字。

`DEFINITION_LINE` 是克制的小字；`TITLE_PLUS_LINE` 是一个双层文字模块，其中标题负责识别与命名，小句负责不重复的情绪回应；`ART_LETTERING` 是通过 Title Editor 的短标题的表现方式，可独立用于插画、绘画、海报或涂鸦，不是地点说明、商品标签或随机潮流噪声。

## 1. 文案规则

文案必须先通过 `title-editor.md`。其中 `DEFINITION_LINE` 先回答“这一刻被留下的是什么”，再压缩为单行：

- 中文约 8–24 个汉字；英文约 4–12 个词。
- 定义意义，不复述“一个人在某地做某事”。
- 可以含轻微判断或诗性张力，但不能虚构关系、动机、职业、目的地或结局。
- 避免“生活就是……”“愿所有……”“治愈一切”等通用金句。
- 不自动添加装饰性副标题。只有 Title Editor 判定两层语义互补时才使用 `TITLE_PLUS_LINE`；仍不加日期、编号、署名、坐标或伪编辑信息。

`USER_TEXT` 必须逐字使用；用户提供标题与小句时分别锁定，只验证各自安全边界、行数和最大宽度，不私自改写。`OFF` 不排字。

`SOURCE_EXACT_MARK` 是原照片里的准确文字、logo、招牌或符号，不是标题。优先使用用户提供或可验证的矢量/确定性结构重绘；不得交给图像模型自由拼写，不得用品牌色带代替 logo，也不得因标题为 `OFF` 而省略。无法可靠重建时必须拒绝交付或请求资产。

`SHORT_TITLE` 默认保持 Title Editor 选定的准确文本，不因字形、断行、押韵或视觉冲击重新改写。它可以进入 `ART_LETTERING`；若没有安全标题区或构图收益，则回退 `DEFINITION_LINE`。只有 Title Editor 已证明短标题与定义句均失败时才 `OFF`。

`TITLE_PLUS_LINE` 中标题与小句必须各司其职：默认标题回答“这是什么或最值得记住的视觉锚点”，小句回答“这些视觉证据产生了什么感受”。小句不能换一种说法复述标题，也不能承担地点、日期、人物关系或故事补全。标题可进入 `ART_LETTERING`，小句始终保持规整、次级和易读。

`AUTO` 在固定 3:5 全幅上先执行 Title Editor；其 `SHOULD_TITLE` 结论对文字层具有约束力。构图只决定使用 `ART_LETTERING` 还是 `DEFINITION_LINE`，不能因艺术字没有安全区就直接改为 `OFF`。仍不得只因留白面积大而强行加标题。

`ART_LETTERING` 中文使用 2–10 个汉字，英文使用 1–6 个词；字数越长，越需要两行或紧凑字组。输入仍是一条准确文字，但视觉输出可按字组堆叠、竖排或沿路径组织。完整合同见 [lettering-engine.md](lettering-engine.md)。

## 2. 字体映射

- 中文默认 `songti`: `/System/Library/Fonts/Supplemental/Songti.ttc`。
- 现代插画或数字板绘可选 `pingfang`: `/System/Library/Fonts/PingFang.ttc`。
- 英文默认 `newyork`: `/System/Library/Fonts/NewYork.ttf`。
- 文学或油画倾向可选 `baskerville`: `/System/Library/Fonts/Supplemental/Baskerville.ttc`。
- 现代数字媒介可选 `avenir`: `/System/Library/Fonts/Avenir Next.ttc`。
- 中文艺术字以 `stheiti`、`pingfang` 或 `songti` 作为可读结构参考；最终 raster 必须逐字复核。只有进入确定性后处理时才要求整组标题蒙版。
- 英文艺术字可选 `impact`、`markerfelt`、`signpainter` 或 `chalkduster`。

字体文件缺失、无法加载或不可靠支持目标语言时拒绝排字，不静默替换。英文展示字体不得用于中文；中文艺术字由完整中文字形与效果共同完成。

## 3. 几何规则

先按视觉角色确定尺度，不从字数或批量模板直接确定：

- `HERO_TITLE`：通常占短边约 28%–70% 的组宽，并与强路径、尺度、动作或编辑节奏建立主关系。
- `SUPPORT_TITLE`：通常占短边约 16%–45% 的组宽，承担配重、顺势、连接或边缘收束。
- `CAPTION`：使用 `DEFINITION_LINE`，保持短边约 1.5%–3% 的小号规整文字。
- `SUPPORT_LINE`：只随 `TITLE_PLUS_LINE` 出现，通常为短边约 1.5%–2.5% 的规整文字，与标题保持清楚的尺度差和阅读顺序。
- `NONE`：不排字。

以上为构图目标，不是机械配额。若 `SHORT_TITLE` 被路由为 `CAPTION`，必须记录 `HERO_TITLE` 与 `SUPPORT_TITLE` 分别失败的具体安全区、构图收益或来源交互证据。

- `DEFINITION_LINE` 默认字号为画布短边约 2%，允许约 1.5%–3%；单行最大宽度为画布短边约 34%。
- `ART_LETTERING` 的基础尺度约为短边 1.5%–8%；整组标题蒙版可按计划扩展为约 0.75–4 个基础字高，最终宽度不超过短边约 75%，并保持核心为第一落点。
- 文字边界距画布四边至少 7%。
- 根据灰度视觉重量选择左对齐或右对齐；不固定底部，不居中横跨画面。
- `DEFINITION_LINE` 字色取画面较深的低饱和来源色，默认 70%–80% 不透明度。`ART_LETTERING` 依次评估来源证据、标题区对比、语义/情绪和视觉层级，再选择颜色；胶片橙、咖啡棕、普鲁士蓝或其他个人偏好色不能越过来源与构图门槛。
- 排字区域必须在生成前预留为连续低信息区域；它可以露出基底，也可以位于静默填充场，但不能压在核心或记忆场识别线索上。
- 全幅图案唱片默认不排字；透明外缘不能作为排字空间。

## 4. 艺术字路由

- `DEFINITION_LINE`：继续使用完整字行、小号规整排版，不进入 Lettering Engine。
- `TITLE_PLUS_LINE`：标题按 `ART_LETTERING` 或规整标题处理，小句按 `SUPPORT_LINE` 处理；两者共同预留安全区，但不得合成同一视觉音量。
- `ART_LETTERING`：有安全标题区、短标题、构图收益和来源交互依据时，先把整组外轮廓、阅读顺序、Glyph DNA、材料与颜色写入最终提示词直接生成。只有用户要求可复用文字层、来源精确标志需要确定性恢复，或直接生成失败且预算允许时才进入 Lettering Engine。
- `PENCIL_NOTE`：作为开放留白的轻量边注，保持小号，不参与硬核标题竞争；可随最终提示词直接生成，但仍须逐字审核。

`AUTO` 不因留白而强行启用艺术字。若 Title Editor 判定 `SHOULD_TITLE` 但艺术字门失败，必须回退小号定义句；只有 Title Editor 的短标题与定义句均失败时才无字。启用后根据来源锚点、运动方向与构图功能选择字形和布局，不随机轮换。整组字使用一个主色，最多一个小面积辅助色；禁止逐字换色。

表现性标题必须先通过字形正确门，再检查是否逐字设计；此逐字审核包括 `PENCIL_NOTE`。把正确文本写进计划、生成出非标准字体外观或通过标准字体替代测试，都不能证明最终 raster 字形正确。

## 5. 条件式确定性排字

只在用户要求可复用/非破坏文字层、精确标志恢复，或直接生成文字失败且总预算至少剩余 90 秒时使用 `scripts/typeset_definition.py`，并传入与 `scripts/prepare_carrier_canvas.py` 相同的 `--carrier-profile`。坐标 `x`、`y` 为相对画布的锚点；`align=left` 时 `x` 是文字左边，`align=right` 时 `x` 是文字右边。脚本必须：

- 验证输入尺寸和形状匹配所选载体；不做裁剪或缩放。
- 拒绝空文本与换行。
- 验证字体、字号、单行宽度和 7% 安全边界。
- 用透明文字层合成，保持文字遮罩外像素逐像素不变。
- 保持输入像素尺寸，输出 PNG，并打印测量 JSON。
- 对圆形载体验证外圆边界和中心孔文字禁入区；保留透明通道。
- 艺术字后处理通过 `--style-profile`、`--lettering-layout`、`--direction-angle`、可选 `--accent-color` 和 `--glyph-plan` 确定性合成；此条件分支必须使用包含已审核整组 `title_plate` 的 `schema_version: 2` 计划。脚本拒绝无计划、`schema_version: 1` 和字体轮廓替代品。

失败时只修正致命的字形、位置或层级问题；不得突破五分钟总预算。
