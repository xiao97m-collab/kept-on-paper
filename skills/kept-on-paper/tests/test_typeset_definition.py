from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


SCRIPT = Path(__file__).parents[1] / "scripts" / "typeset_definition.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("typeset_definition", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class TypesetDefinitionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.png"
        Image.new("RGB", (600, 1000), (246, 241, 226)).save(self.source)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def args(self, **overrides: object) -> Namespace:
        values = {
            "input": self.source,
            "output": self.root / "out.png",
            "carrier_profile": None,
            "text": "风把远方留在经过的路上",
            "language": "zh",
            "font_profile": "songti",
            "x": 0.10,
            "y": 0.20,
            "align": "left",
            "size_ratio": 0.02,
            "max_width_ratio": 0.34,
            "safe_margin_ratio": 0.07,
            "color": "#334A4A",
            "accent_color": "#D85F3F",
            "opacity": 0.76,
            "style_profile": "classic",
            "lettering_layout": "line",
            "direction_angle": 0.0,
            "glyph_plan": None,
        }
        values.update(overrides)
        return Namespace(**values)

    def test_chinese_left_keeps_size_and_outside_pixels(self) -> None:
        args = self.args()
        metrics = MODULE.typeset(args)
        with Image.open(self.source) as opened:
            before = opened.convert("RGB")
        with Image.open(args.output) as opened:
            after = opened.convert("RGB")
        self.assertEqual(after.size, (600, 1000))
        diff = ImageChops.difference(before, after)
        changed = diff.getbbox()
        self.assertIsNotNone(changed)
        bbox = tuple(metrics["changed_bbox"])
        self.assertEqual(changed, bbox)

    def test_english_right_alignment(self) -> None:
        args = self.args(
            text="THE WIND KEEPS WHAT WE RELEASE",
            language="en",
            font_profile="newyork",
            x=0.90,
            align="right",
        )
        metrics = MODULE.typeset(args)
        self.assertEqual(metrics["align"], "right")
        self.assertTrue(args.output.is_file())

    def test_rejects_bare_chinese_cut_stencil_lettering(self) -> None:
        args = self.args(
            text="各自经过",
            font_profile="stheiti",
            style_profile="cut_stencil",
            lettering_layout="stacked",
            size_ratio=0.06,
            max_width_ratio=0.70,
        )
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(args)

    def test_rejects_bare_brush_ink_lettering(self) -> None:
        args = self.args(
            text="风起",
            font_profile="songti",
            style_profile="brush_ink",
            lettering_layout="vertical",
            size_ratio=0.06,
            max_width_ratio=0.70,
        )
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(args)

    def test_rejects_bare_english_offset_screenprint_lettering(self) -> None:
        args = self.args(
            text="CROSSING HOURS",
            language="en",
            font_profile="impact",
            style_profile="offset_screenprint",
            lettering_layout="path_aligned",
            direction_angle=8.0,
            size_ratio=0.05,
            max_width_ratio=0.70,
        )
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(args)

    def test_art_lettering_is_deterministic(self) -> None:
        plan = self.write_title_plate_plan()
        first = self.args(
            output=self.root / "first.png",
            text="把今天慢慢喝完",
            font_profile="stheiti",
            style_profile="paint_brush",
            lettering_layout="stacked",
            size_ratio=0.05,
            max_width_ratio=0.75,
            glyph_plan=plan,
        )
        second = self.args(
            output=self.root / "second.png",
            text="把今天慢慢喝完",
            font_profile="stheiti",
            style_profile="paint_brush",
            lettering_layout="stacked",
            size_ratio=0.05,
            max_width_ratio=0.75,
            glyph_plan=plan,
        )
        MODULE.typeset(first)
        MODULE.typeset(second)
        with Image.open(first.output) as opened:
            first_image = opened.convert("RGBA")
        with Image.open(second.output) as opened:
            second_image = opened.convert("RGBA")
        self.assertIsNone(ImageChops.difference(first_image, second_image).getbbox())

    def write_glyph_plan(
        self, *, interlock: dict[str, object] | None = None
    ) -> Path:
        plan = {
            "schema_version": 1,
            "group": {
                "material": "dry_marker",
                "skeleton": "custom",
                "source_anchor": "人物向右跨越栏杆的动作",
                "composition_function": "continue_motion",
                "entry_behavior": "短促起笔",
                "turn_behavior": "宽头马克笔硬转折",
                "exit_behavior": "末笔顺着跨越方向延伸",
            },
            "glyphs": [
                {
                    "unit": "向",
                    "role": "support",
                    "scale": 0.86,
                    "rotation": -3,
                    "x_shift": 0,
                    "y_shift": 0.08,
                },
                {
                    "unit": "前",
                    "role": "hero",
                    "scale": 1.18,
                    "rotation": 4,
                    "x_shift": -0.08,
                    "y_shift": 0,
                    "extension": {
                        "edge": "bottom",
                        "direction_angle": 8,
                        "length_ratio": 0.55,
                        "width_ratio": 0.07,
                    },
                },
            ],
            "interlock": interlock,
        }
        path = self.root / "glyph-plan.json"
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return path

    def test_schema_v1_glyph_plan_is_rejected_for_final_output(self) -> None:
        plan = self.write_glyph_plan()
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="向前",
                    font_profile="stheiti",
                    style_profile="dry_marker",
                    lettering_layout="path_aligned",
                    size_ratio=0.06,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_schema_v1_custom_glyph_mask_is_not_final_output(self) -> None:
        mask = self.root / "custom-forward.png"
        custom = Image.new("RGBA", (100, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(custom)
        draw.line((20, 20, 50, 100), fill=(255, 255, 255, 255), width=13)
        draw.line((50, 100, 92, 72), fill=(255, 255, 255, 255), width=13)
        custom.save(mask)
        plan = self.write_glyph_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["glyphs"][1]["custom_mask"] = mask.name
        data["glyphs"][1].pop("extension")
        plan.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="向前",
                    font_profile="stheiti",
                    style_profile="dry_marker",
                    lettering_layout="path_aligned",
                    size_ratio=0.06,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_custom_glyph_mask_rejects_opaque_background(self) -> None:
        mask = self.root / "opaque.png"
        Image.new("RGB", (100, 120), (255, 255, 255)).save(mask)
        plan = self.write_glyph_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["glyphs"][1]["custom_mask"] = mask.name
        plan.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="向前",
                    font_profile="stheiti",
                    style_profile="dry_marker",
                    lettering_layout="path_aligned",
                    size_ratio=0.06,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_memory_interlock_uses_transparent_source_asset(self) -> None:
        asset = self.root / "memory-trace.png"
        trace = Image.new("RGBA", (120, 80), (0, 0, 0, 0))
        ImageDraw.Draw(trace).line((4, 70, 116, 8), fill=(255, 255, 255, 220), width=8)
        trace.save(asset)
        plan = self.write_title_plate_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["interlock"] = {
            "mode": "stroke_continuation",
            "glyph_index": 3,
            "source_element": "杯口与视线的上升方向",
            "source_relationship": "延续标题的收笔方向",
            "semantic_reason": "让收笔进入照片已有的上升关系",
            "stopping_boundary": "只离开末笔一次，不形成第二物件",
            "asset": asset.name,
            "color_role": "accent",
            "scale": 0.72,
            "x": 0.78,
            "y": 0.72,
        }
        plan.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        metrics = MODULE.typeset(
            self.args(
                text="把今天慢慢喝完",
                font_profile="stheiti",
                style_profile="paint_brush",
                lettering_layout="stacked",
                size_ratio=0.05,
                max_width_ratio=0.75,
                glyph_plan=plan,
            )
        )
        self.assertEqual(metrics["interlock_mode"], "stroke_continuation")

    def test_memory_interlock_rejects_opaque_rgba_asset(self) -> None:
        asset = self.root / "opaque-memory.png"
        Image.new("RGBA", (120, 80), (255, 255, 255, 255)).save(asset)
        plan = self.write_glyph_plan(
            interlock={
                "mode": "stroke_continuation",
                "glyph_index": 1,
                "source_element": "运动路径",
                "source_relationship": "延续方向",
                "semantic_reason": "让动作进入字形",
                "stopping_boundary": "只延续一次",
                "asset": asset.name,
                "color_role": "accent",
                "scale": 0.72,
                "x": 0.78,
                "y": 0.72,
            }
        )
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="向前",
                    font_profile="stheiti",
                    style_profile="dry_marker",
                    lettering_layout="path_aligned",
                    size_ratio=0.06,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_stroke_substitution_requires_small_erase_region(self) -> None:
        asset = self.root / "memory-stroke.png"
        trace = Image.new("RGBA", (120, 80), (0, 0, 0, 0))
        ImageDraw.Draw(trace).line((4, 70, 116, 8), fill=(255, 255, 255, 220), width=8)
        trace.save(asset)
        plan = self.write_glyph_plan(
            interlock={
                "mode": "stroke_substitution",
                "glyph_index": 1,
                "source_element": "运动路径",
                "source_relationship": "替换非关键末笔",
                "semantic_reason": "让动作进入字形",
                "stopping_boundary": "只替换一小段末笔",
                "asset": asset.name,
                "color_role": "accent",
                "scale": 0.72,
                "x": 0.78,
                "y": 0.72,
                "erase_region": [0.0, 0.0, 0.9, 0.9],
            }
        )
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="向前",
                    font_profile="stheiti",
                    style_profile="dry_marker",
                    lettering_layout="path_aligned",
                    size_ratio=0.06,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_glyph_plan_rejects_multiple_hero_glyphs(self) -> None:
        plan = self.write_glyph_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["glyphs"][0]["role"] = "hero"
        plan.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="向前",
                    font_profile="stheiti",
                    style_profile="dry_marker",
                    lettering_layout="path_aligned",
                    size_ratio=0.06,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_classic_style_rejects_glyph_plan(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args(glyph_plan=self.root / "unused.json"))

    def test_rejects_overlong_chinese_art_lettering(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="这是一句确实过长的艺术标题",
                    font_profile="stheiti",
                    style_profile="cut_stencil",
                    lettering_layout="stacked",
                    size_ratio=0.05,
                    max_width_ratio=0.70,
                )
            )

    def write_title_plate_plan(self, *, exact_text: str = "把今天慢慢喝完") -> Path:
        plate = self.root / "title-plate.png"
        image = Image.new("L", (360, 180), 255)
        draw = ImageDraw.Draw(image)
        draw.line((20, 40, 150, 32, 290, 58), fill=0, width=18)
        draw.line((52, 105, 190, 92, 330, 142), fill=0, width=24)
        draw.ellipse((265, 118, 338, 158), outline=0, width=12)
        image.save(plate)
        units = list("把今天慢慢喝完")
        roles = ["support", "support", "connector", "hero", "support", "support", "tail"]
        plan = {
            "schema_version": 2,
            "group": {
                "material": "paint_brush",
                "skeleton": "custom",
                "source_anchor": "杯口与墙面卡片的上升方向",
                "composition_function": "balance_weight",
                "entry_behavior": "短促干刷起笔",
                "turn_behavior": "圆转后保留刷毛断边",
                "exit_behavior": "末笔向杯口收束",
                "exact_text": exact_text,
                "title_plate": plate.name,
                "title_plate_mode": "dark_on_light",
                "plate_height_ratio": 2.4,
                "title_zone": "人物左上方的低信息墙面",
                "line_count": 2,
                "group_silhouette": "上短下长的两行舒展字组",
                "reading_order": "从左上进入，向右下结束",
                "visual_weight_target": "弱于人物面部，强于墙面卡片",
                "protected_regions": ["脸部", "双手", "杯口"],
                "primary_color_source": "饮料、木桌和橙色卡片",
                "color_reason": "来源明确并与灰白墙面形成适度对比",
            },
            "glyphs": [
                {
                    "unit": unit,
                    "role": role,
                    "scale": 1.0,
                    "rotation": 0,
                    "x_shift": 0,
                    "y_shift": 0,
                }
                for unit, role in zip(units, roles)
            ],
            "interlock": None,
        }
        path = self.root / "title-plan.json"
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return path

    def test_group_title_plate_is_materialized_without_font_glyphs(self) -> None:
        plan = self.write_title_plate_plan()
        metrics = MODULE.typeset(
            self.args(
                text="把今天慢慢喝完",
                font_profile="stheiti",
                style_profile="paint_brush",
                lettering_layout="stacked",
                size_ratio=0.05,
                max_width_ratio=0.75,
                glyph_plan=plan,
                color="#C8622E",
            )
        )
        self.assertTrue(metrics["title_plate"])
        self.assertEqual(metrics["title_plate_mode"], "dark_on_light")
        self.assertEqual(metrics["unit_count"], 7)
        with Image.open(self.source) as opened:
            before = opened.convert("RGB")
        with Image.open(Path(metrics["output"])) as opened:
            after = opened.convert("RGB")
        self.assertEqual(ImageChops.difference(before, after).getbbox(), tuple(metrics["changed_bbox"]))

    def test_group_title_plate_accepts_optional_visual_language_fields(self) -> None:
        plan = self.write_title_plate_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["group"].update(
            {
                "visual_language": "relaxed_note_group",
                "image_relation": "counterweight",
                "glyph_dna": {
                    "proportion_system": "中等字宽与开放负形",
                    "rhythm_system": "同向右倾与一个连续收笔",
                },
                "color_roles": {
                    "group_main": "饮料棕橙",
                    "semantic_accent": None,
                    "micro_note": None,
                },
                "ornament_grammar": [],
            }
        )
        plan.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        metrics = MODULE.typeset(
            self.args(
                text="把今天慢慢喝完",
                font_profile="stheiti",
                style_profile="paint_brush",
                lettering_layout="stacked",
                size_ratio=0.05,
                max_width_ratio=0.75,
                glyph_plan=plan,
                color="#C8622E",
            )
        )

        self.assertTrue(metrics["title_plate"])
        self.assertEqual(metrics["unit_count"], 7)

    def test_group_title_plate_recolors_without_changing_silhouette(self) -> None:
        plan = self.write_title_plate_plan()
        first = self.args(
            output=self.root / "orange.png",
            text="把今天慢慢喝完",
            font_profile="stheiti",
            style_profile="paint_brush",
            lettering_layout="stacked",
            size_ratio=0.05,
            max_width_ratio=0.75,
            glyph_plan=plan,
            color="#C8622E",
        )
        second = self.args(**{**vars(first), "output": self.root / "blue.png", "color": "#173C5B"})
        first_metrics = MODULE.typeset(first)
        second_metrics = MODULE.typeset(second)
        self.assertEqual(first_metrics["text_bbox"], second_metrics["text_bbox"])
        with Image.open(first.output) as opened:
            orange = opened.convert("RGB")
        with Image.open(second.output) as opened:
            blue = opened.convert("RGB")
        self.assertIsNotNone(ImageChops.difference(orange, blue).getbbox())

    def test_group_title_plate_requires_exact_text_match(self) -> None:
        plan = self.write_title_plate_plan(exact_text="把今天快速喝完")
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="把今天慢慢喝完",
                    font_profile="stheiti",
                    style_profile="paint_brush",
                    lettering_layout="stacked",
                    size_ratio=0.05,
                    max_width_ratio=0.75,
                    glyph_plan=plan,
                )
            )

    def test_rejects_unreliable_chinese_art_font(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    text="纸上留存",
                    font_profile="markerfelt",
                    style_profile="dry_marker",
                )
            )

    def test_classic_style_rejects_display_size(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args(size_ratio=0.05))

    def test_classic_style_rejects_art_layout(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args(lettering_layout="stacked"))

    def test_rejects_multiline(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args(text="第一行\n第二行"))

    def test_rejects_overlong_line(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args(text="这是一段明显超过允许宽度并且不应被自动缩小的定义句"))

    def test_rejects_out_of_bounds(self) -> None:
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args(x=0.01))

    def test_rejects_non_three_by_five(self) -> None:
        Image.new("RGB", (600, 900), (246, 241, 226)).save(self.source)
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(self.args())

    def test_picture_disc_rejects_center_text(self) -> None:
        Image.new("RGBA", (1800, 1800), (246, 241, 226, 255)).save(self.source)
        with self.assertRaises(MODULE.TypesetError):
            MODULE.typeset(
                self.args(
                    carrier_profile="PICTURE_DISC_1_1",
                    x=0.50,
                    y=0.50,
                    text="中心文字",
                )
            )

    def test_picture_disc_preserves_transparent_shape(self) -> None:
        image = Image.new("RGBA", (1800, 1800), (246, 241, 226, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, 1799, 1799), fill=(246, 241, 226, 255))
        draw.ellipse((868, 868, 932, 932), fill=(0, 0, 0, 0))
        image.save(self.source)
        args = self.args(
            carrier_profile="PICTURE_DISC_1_1",
            x=0.20,
            y=0.25,
            text="风仍然经过",
        )
        MODULE.typeset(args)
        with Image.open(args.output) as opened:
            result = opened.convert("RGBA")
            self.assertEqual(result.getpixel((0, 0))[3], 0)
            self.assertEqual(result.getpixel((900, 900))[3], 0)


if __name__ == "__main__":
    unittest.main()
