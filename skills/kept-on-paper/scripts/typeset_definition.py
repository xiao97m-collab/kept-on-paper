#!/usr/bin/env python3
"""Deterministically typeset a definition line or art-lettering composition."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

from carrier_profiles import PROFILES, CarrierProfile, get_profile
from lettering_engine import ART_LAYOUTS, ART_STYLES, render_lettering


FONTS = {
    "songti": Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
    "pingfang": Path("/System/Library/Fonts/PingFang.ttc"),
    "stheiti": Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    "newyork": Path("/System/Library/Fonts/NewYork.ttf"),
    "baskerville": Path("/System/Library/Fonts/Supplemental/Baskerville.ttc"),
    "avenir": Path("/System/Library/Fonts/Avenir Next.ttc"),
    "impact": Path("/System/Library/Fonts/Supplemental/Impact.ttf"),
    "markerfelt": Path("/System/Library/Fonts/MarkerFelt.ttc"),
    "signpainter": Path("/System/Library/Fonts/Supplemental/SignPainter.ttc"),
    "chalkduster": Path("/System/Library/Fonts/Supplemental/Chalkduster.ttf"),
}

CHINESE_FONTS = {"songti", "pingfang", "stheiti"}
STYLE_PROFILES = {"classic", *ART_STYLES}


class TypesetError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--carrier-profile", choices=tuple(PROFILES))
    parser.add_argument("--text", required=True)
    parser.add_argument("--language", required=True, choices=("zh", "en"))
    parser.add_argument("--font-profile", required=True, choices=tuple(FONTS))
    parser.add_argument("--x", required=True, type=float)
    parser.add_argument("--y", required=True, type=float)
    parser.add_argument("--align", required=True, choices=("left", "right"))
    parser.add_argument("--size-ratio", type=float, default=0.02)
    parser.add_argument("--max-width-ratio", type=float, default=0.34)
    parser.add_argument("--safe-margin-ratio", type=float, default=0.07)
    parser.add_argument("--color", default="#334A4A")
    parser.add_argument("--accent-color", default="#D85F3F")
    parser.add_argument("--opacity", type=float, default=0.76)
    parser.add_argument(
        "--style-profile", choices=tuple(sorted(STYLE_PROFILES)), default="classic"
    )
    parser.add_argument(
        "--lettering-layout", choices=tuple(sorted(ART_LAYOUTS)), default="line"
    )
    parser.add_argument("--direction-angle", type=float, default=0.0)
    parser.add_argument(
        "--glyph-plan",
        type=Path,
        help="Validated JSON plan for per-glyph roles, geometry, and one memory interlock",
    )
    return parser.parse_args()


def validate_text(text: str, language: str, style: str) -> None:
    if not text.strip():
        raise TypesetError("text must not be empty")
    if "\n" in text or "\r" in text:
        raise TypesetError("input text must be exactly one logical line")
    if language == "zh":
        count = len(re.findall(r"[\u3400-\u9fff]", text))
        if count < 1:
            raise TypesetError("Chinese text must contain Chinese characters")
        if style in ART_STYLES - {"pencil_note"} and not 2 <= count <= 10:
            raise TypesetError("Chinese art lettering must contain 2 to 10 characters")
    else:
        words = re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)?", text)
        if not words:
            raise TypesetError("English text must contain English words")
        if style in ART_STYLES - {"pencil_note"} and not 1 <= len(words) <= 6:
            raise TypesetError("English art lettering must contain 1 to 6 words")


def validate_canvas(width: int, height: int, profile: CarrierProfile, name: str) -> None:
    expected = (profile.width, profile.height)
    if width <= 0 or height <= 0 or (width, height) != expected:
        raise TypesetError(
            f"input must match {name} at {expected[0]}x{expected[1]}; got {width}x{height}"
        )


def resolve_profile(
    width: int, height: int, profile_name: str | None
) -> tuple[CarrierProfile, str]:
    if profile_name is not None:
        profile = get_profile(profile_name)
        validate_canvas(width, height, profile, profile_name)
        return profile, profile_name
    if width <= 0 or height <= 0 or width * 5 != height * 3:
        raise TypesetError(f"legacy input must be exact 3:5; got {width}x{height}")
    return CarrierProfile(width, height), "LEGACY_3_5"


def validate_shaped_text_bounds(
    bbox: tuple[int, int, int, int], profile: CarrierProfile, safe_margin: int
) -> None:
    if profile.shape != "circle":
        return
    cx, cy = profile.width / 2, profile.height / 2
    usable_radius = min(profile.width, profile.height) / 2 - safe_margin
    corners = (
        (bbox[0], bbox[1]),
        (bbox[0], bbox[3]),
        (bbox[2], bbox[1]),
        (bbox[2], bbox[3]),
    )
    if any((x - cx) ** 2 + (y - cy) ** 2 > usable_radius**2 for x, y in corners):
        raise TypesetError("text crosses the usable circular carrier boundary")
    exclusion = min(profile.width, profile.height) * profile.text_exclusion_radius_ratio
    nearest_x = min(max(cx, bbox[0]), bbox[2])
    nearest_y = min(max(cy, bbox[1]), bbox[3])
    if (nearest_x - cx) ** 2 + (nearest_y - cy) ** 2 < exclusion**2:
        raise TypesetError("text intersects the picture-disc center exclusion zone")


def validate_ranges(args: argparse.Namespace) -> None:
    for name in ("x", "y"):
        value = getattr(args, name)
        if not 0.0 <= value <= 1.0:
            raise TypesetError(f"{name} must be between 0 and 1")
    style = getattr(args, "style_profile", "classic")
    layout = getattr(args, "lettering_layout", "line")
    max_size = 0.03 if style == "classic" else 0.08
    max_width = 0.34 if style == "classic" else 0.75
    if not 0.015 <= args.size_ratio <= max_size:
        raise TypesetError(f"size-ratio must be between 0.015 and {max_size:.2f}")
    if not 0.05 <= args.max_width_ratio <= max_width:
        raise TypesetError(f"max-width-ratio must be between 0.05 and {max_width:.2f}")
    if not 0.07 <= args.safe_margin_ratio <= 0.20:
        raise TypesetError("safe-margin-ratio must be between 0.07 and 0.20")
    if not 0.0 < args.opacity <= 1.0:
        raise TypesetError("opacity must be greater than 0 and at most 1")
    if style == "classic" and layout != "line":
        raise TypesetError("classic definitions only support lettering-layout line")
    if style == "classic" and getattr(args, "glyph_plan", None) is not None:
        raise TypesetError("classic definitions do not support glyph-plan")
    if not -45.0 <= getattr(args, "direction_angle", 0.0) <= 45.0:
        raise TypesetError("direction-angle must be between -45 and 45 degrees")


def typeset(args: argparse.Namespace) -> dict[str, object]:
    style = getattr(args, "style_profile", "classic")
    validate_text(args.text, args.language, style)
    validate_ranges(args)

    font_path = FONTS[args.font_profile]
    if args.language == "zh" and args.font_profile not in CHINESE_FONTS:
        raise TypesetError(
            f"font-profile {args.font_profile} does not provide reliable Chinese glyphs"
        )
    if not font_path.is_file():
        raise TypesetError(f"font not found: {font_path}")
    if not args.input.is_file():
        raise TypesetError(f"input not found: {args.input}")

    with Image.open(args.input) as opened:
        input_has_alpha = "A" in opened.getbands()
        base = opened.convert("RGBA")
    width, height = base.size
    profile, profile_name = resolve_profile(
        width, height, getattr(args, "carrier_profile", None)
    )
    preserve_alpha = input_has_alpha or profile.shape != "rectangle"

    short_edge = min(width, height)
    font_size = max(1, round(short_edge * args.size_ratio))
    x = round(width * args.x)
    y = round(height * args.y)
    rgb = ImageColor.getrgb(args.color)
    accent_rgb = ImageColor.getrgb(getattr(args, "accent_color", "#D85F3F"))
    alpha = round(255 * args.opacity)
    glyph_plan_path = getattr(args, "glyph_plan", None)
    glyph_plan: dict[str, object] | None = None
    if glyph_plan_path is not None:
        if not glyph_plan_path.is_file():
            raise TypesetError(f"glyph plan not found: {glyph_plan_path}")
        try:
            glyph_plan = json.loads(glyph_plan_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TypesetError(f"invalid glyph plan JSON: {exc}") from exc
        if not isinstance(glyph_plan, dict):
            raise TypesetError("glyph plan root must be an object")
        for glyph in glyph_plan.get("glyphs", []):
            if isinstance(glyph, dict) and glyph.get("custom_mask"):
                path = Path(glyph["custom_mask"])
                if not path.is_absolute():
                    glyph["custom_mask"] = str(glyph_plan_path.parent / path)
        group = glyph_plan.get("group")
        if isinstance(group, dict) and group.get("title_plate"):
            path = Path(group["title_plate"])
            if not path.is_absolute():
                group["title_plate"] = str(glyph_plan_path.parent / path)
        interlock = glyph_plan.get("interlock")
        if isinstance(interlock, dict) and interlock.get("asset"):
            path = Path(interlock["asset"])
            if not path.is_absolute():
                interlock["asset"] = str(glyph_plan_path.parent / path)

    if style in ART_STYLES - {"pencil_note"}:
        if glyph_plan is None:
            raise TypesetError(
                "final art lettering requires a reviewed schema_version 2 title plate"
            )
        group = glyph_plan.get("group")
        if glyph_plan.get("schema_version") != 2 or not (
            isinstance(group, dict) and group.get("title_plate")
        ):
            raise TypesetError(
                "final art lettering rejects font-derived or schema_version 1 output; "
                "provide a reviewed schema_version 2 title plate"
            )

    lettering_metrics: dict[str, object] = {
        "lettering_layout": "line",
        "unit_count": 1,
        "direction_angle": 0.0,
    }
    if style == "classic":
        font = ImageFont.truetype(str(font_path), font_size)
        anchor = "la" if args.align == "left" else "ra"
        layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).text(
            (x, y), args.text, font=font, fill=(*rgb, alpha), anchor=anchor
        )
    else:
        try:
            layer, lettering_metrics = render_lettering(
                base.size,
                (x, y),
                args.text,
                args.language,
                font_path,
                font_size,
                args.align,
                rgb,
                accent_rgb,
                alpha,
                style,
                getattr(args, "lettering_layout", "line"),
                getattr(args, "direction_angle", 0.0),
                glyph_plan,
            )
        except ValueError as exc:
            raise TypesetError(str(exc)) from exc

    mask_bbox = layer.getchannel("A").getbbox()
    if mask_bbox is None:
        raise TypesetError("font produced an empty text mask")
    left, top, right, bottom = mask_bbox
    text_width = right - left
    if text_width > short_edge * args.max_width_ratio:
        raise TypesetError(
            f"text width {text_width}px exceeds {args.max_width_ratio:.0%} of short edge"
        )

    safe_x = round(width * args.safe_margin_ratio)
    safe_y = round(height * args.safe_margin_ratio)
    if left < safe_x or right > width - safe_x or top < safe_y or bottom > height - safe_y:
        raise TypesetError(
            f"text bbox {mask_bbox} crosses safe bounds "
            f"{(safe_x, safe_y, width-safe_x, height-safe_y)}"
        )
    validate_shaped_text_bounds(mask_bbox, profile, max(safe_x, safe_y))

    result = Image.alpha_composite(base, layer)
    if not preserve_alpha:
        result = result.convert("RGB")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output, format="PNG", optimize=True)

    return {
        "input": str(args.input),
        "output": str(args.output),
        "carrier_profile": profile_name,
        "size": [width, height],
        "font": str(font_path),
        "font_size_px": font_size,
        "anchor": [x, y],
        "align": args.align,
        "style_profile": style,
        "glyph_plan_path": str(glyph_plan_path) if glyph_plan_path else None,
        **lettering_metrics,
        "text_bbox": list(mask_bbox),
        "changed_bbox": list(mask_bbox),
    }


def main() -> int:
    try:
        metrics = typeset(parse_args())
    except (OSError, TypesetError, ValueError) as exc:
        print(f"typeset error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(metrics, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
