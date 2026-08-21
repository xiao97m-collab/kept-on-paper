# Carrier Contracts

Kept on Paper 当前只有一个公开且确定性的输出规格。画布几何从生成前参与核心尺度、记忆场拓扑、排字区和安全区安排，不是生成完成后附加的边框。

确定性输出只支持 `FULL_FRAME_3_5`：1200 × 2000 的完整 3:5 矩形平面作品。不生成其他物件载体、桌面、墙面、唱机、手持、投影、包装场景或商业 mockup。

## 1. Deterministic Profiles

| Profile | Final size | Active shape | Default text role |
|---|---:|---|---|
| `FULL_FRAME_3_5` | 1200 × 2000 | 完整矩形 | `AUTO` |

先让图像模型按 3:5 几何和安全区直接生成包含可选文字的完整作品，再运行 `scripts/prepare_carrier_canvas.py`。该脚本只做确定性尺寸与裁切，不能修复错误构图或文字。裁切会丢失超过 50% 时拒绝，要求按 3:5 重新生成。

## 2. Fixed Profile Card

生成前只填写：

- `Profile`: 固定 `FULL_FRAME_3_5`。
- `Active shape`: 完整 3:5 矩形。
- `Core scale`: 核心占有效形状的视觉重量。
- `Exclusion zones`: 画面与文字安全边界。
- `Memory-field topology`: 矩形内的方向场、配重和视觉出口。
- `Low-information plan`: 在完整矩形内部计算。
- `Text role and zone`: 可用定义句、表现性标题、语义互补的标题加小句，或无字。
- `Finishing step`: 3:5 画布准备和可选排字配置。

## 3. Composition

- 使用完整 3:5 矩形安排核心、记忆场、空间模式和文字。
- 支持 `OPEN_SPACE`、`QUIET_FILLED_FIELD` 与仅供硬核涂鸦的 `DENSE_EDITORIAL_FIELD`；分别执行各自低信息或层级预算。
- 适合绝大多数人物关系、事件、环境尺度和视觉锚点。
- 默认由 Title Editor 按画面决定单标题、单短句、标题加小句或无字，不按载体强制统一文字形式。
- 禁止自动添加边框、唱片、产品投影或任何物件载体暗示。

## 4. Quality Gate

- 最终像素尺寸是否准确为 1200 × 2000？
- 是否使用完整 3:5 矩形，没有额外物件外形、透明外缘或中心孔？
- 3:5 几何是否在生成前参与构图，而非生成后机械裁切？
- 核心在缩小观看时是否仍可读？
- 安全边界是否避开脸、手势、接触点和事实线索？
- 文字角色和区域是否与构图共同规划？
- 是否保持平面可交付设计，无商业 mockup 和伪生产信息？
