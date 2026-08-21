# Kept on Paper · 纸上留存

Kept on Paper 是一个面向 Codex 的照片转绘 Skill。它把用户提供的真实照片完整转绘为 3:5 纪念艺术，同时保护照片中的人物、动作、关系、尺度、路径、场景基底与关键颜色。

它不做滤镜转换、摄影像素拼贴或商业 mockup。核心原则是：

> 瞬间为核，事实不改；先选方向，一次成图。

Kept on Paper is a Codex skill for turning real photographs into source-faithful 3:5 commemorative artwork. It redraws the image instead of applying a filter, pasting photo pixels, or inventing a second story.

## 能做什么

- 从原照片建立 Source Lock，保护身份、数量、动作、朝向、关系和场景事实。
- 根据照片选择 `T0`–`T3` 转绘深度，而不是机械套用统一风格。
- 在 `OPEN_SPACE`、`QUIET_FILLED_FIELD` 和 `DENSE_EDITORIAL_FIELD` 之间判断合适的空间模式。
- 支持插画、油画、蜡笔、水彩、水粉、数字绘画和中国画等媒介方向。
- 判断是否需要标题、短句或艺术字，并检查文案事实依据与中文字形正确性。
- 输出固定为 1200×2000 PNG，并支持基于同一照片持续修改。

## 安装

```bash
git clone https://github.com/xiao97m-collab/kept-on-paper.git
mkdir -p ~/.codex/skills
cp -R kept-on-paper/skills/kept-on-paper ~/.codex/skills/kept-on-paper
```

重新打开 Codex，或让 Codex 重新读取本地 Skills。

## 第一次使用

上传一张真实照片，然后调用：

```text
使用 $kept-on-paper 处理这张照片
```

默认进入 **Plan**：Skill 会先给出三个来源驱动的转绘方向，并解释关键术语，等待用户选择后再生成。

如果希望由 AI 直接判断并生成：

```text
使用 $kept-on-paper，以 Random 模式直接帮我决定并生成
```

生成后可以继续提出修改，例如：

```text
再抽象一点
保留这个方向，但增加真实纸面留白
加入标题，字体更有设计感
只调整颜色，不改构图
```

## 工作模式

### Plan（默认）

先读取照片并建立 Source Lock，再输出三个真正不同的 Direction Card。选择方向之前不会生成图片。

### Random

AI 根据来源事实、可见增益与风险门自行选择最合适的方向，并直接生成。Random 不表示无约束随机风格。

## 运行要求

- 支持本地 Skills 与图像生成工具的 Codex 环境。
- Python 3.9+。
- Pillow，用于确定性载体与排字辅助脚本：

  ```bash
  python3 -m pip install -r requirements.txt
  ```

- 确定性排字脚本默认引用 macOS 系统字体，因此该分支目前以 macOS 为优先支持环境。仓库不包含、复制或重新分发 Apple 字体。普通的一次性图像生成不要求把这些字体文件加入仓库。

## 仓库结构

```text
skills/kept-on-paper/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── tests/
```

## 验证

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/kept-on-paper

python3 -m unittest discover \
  -s skills/kept-on-paper/tests \
  -p 'test_*.py' -v
```

当前公开版本：`v2.18.0`。

## 照片权利与隐私

输入照片必须由使用者拥有使用权或者相关授权。请勿提交未经授权的私人照片、受版权保护的素材、敏感个人信息或不应公开的原始图片。

本仓库不包含用户照片、生成结果、API 密钥或系统字体。

## License

[MIT License](LICENSE)
