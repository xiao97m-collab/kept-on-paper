"""Deterministic expressive-title and per-glyph lettering compositor."""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


ART_STYLES = {
    "cut_stencil",
    "dry_marker",
    "offset_screenprint",
    "pencil_note",
    "brush_ink",
    "fountain_pen",
    "paint_brush",
}
ART_LAYOUTS = {"line", "stacked", "vertical", "path_aligned", "compact_block"}
GLYPH_ROLES = {"hero", "connector", "support", "tail"}
SKELETONS = {"upright", "running", "cursive", "compressed", "wide", "custom"}
INTERLOCK_MODES = {
    "stroke_continuation",
    "stroke_substitution",
    "material_transfer",
    "counterform_reveal",
    "occlusion_interlock",
    "glyph_to_field",
}


def _seed(*parts: object) -> int:
    serialized = [
        json.dumps(part, ensure_ascii=False, sort_keys=True)
        if isinstance(part, (dict, list))
        else str(part)
        for part in parts
    ]
    value = "|".join(serialized).encode("utf-8")
    return int.from_bytes(hashlib.sha256(value).digest()[:8], "big")


def _units(text: str, language: str) -> list[str]:
    if language == "zh":
        return [char for char in text if not char.isspace()]
    return re.findall(r"\S+", text)


def _rgba_from_mask(
    mask: Image.Image, color: tuple[int, int, int], opacity: int
) -> Image.Image:
    layer = Image.new("RGBA", mask.size, (*color, 0))
    alpha = mask.point(lambda value: value * opacity // 255)
    layer.putalpha(alpha)
    return layer


def _shift_mask(mask: Image.Image, dx: int, dy: int) -> Image.Image:
    shifted = Image.new("L", mask.size, 0)
    shifted.paste(mask, (dx, dy))
    return shifted


def _glyph_mask(unit: str, font: ImageFont.FreeTypeFont) -> Image.Image:
    probe = Image.new("L", (1, 1), 0)
    bbox = ImageDraw.Draw(probe).textbbox((0, 0), unit, font=font, stroke_width=1)
    pad = max(6, round(font.size * 0.18))
    width = max(1, bbox[2] - bbox[0] + pad * 2)
    height = max(1, bbox[3] - bbox[1] + pad * 2)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).text(
        (pad - bbox[0], pad - bbox[1]),
        unit,
        font=font,
        fill=255,
        stroke_width=max(1, round(font.size / 50)),
        stroke_fill=255,
    )
    return mask


def _load_custom_mask(path: Path, target_height: int) -> Image.Image:
    if not path.is_file():
        raise ValueError(f"custom glyph mask not found: {path}")
    with Image.open(path) as opened:
        if "A" not in opened.getbands():
            raise ValueError("custom glyph mask must have a transparent background")
        source = opened.convert("RGBA")
    alpha = source.getchannel("A")
    if alpha.getextrema() == (255, 255):
        raise ValueError("custom glyph mask must have a transparent background")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError(f"custom glyph mask is empty: {path}")
    alpha = alpha.crop(bbox)
    scale = target_height / max(1, alpha.height)
    width = max(1, round(alpha.width * scale))
    return alpha.resize((width, target_height), Image.Resampling.LANCZOS)


def _load_title_plate(path: Path, target_height: int, mode: str) -> Image.Image:
    if not path.is_file():
        raise ValueError(f"title plate not found: {path}")
    with Image.open(path) as opened:
        if mode == "alpha":
            if "A" not in opened.getbands():
                raise ValueError("alpha title plate must have a transparent background")
            mask = opened.convert("RGBA").getchannel("A")
            if mask.getextrema() == (255, 255):
                raise ValueError("alpha title plate must have a transparent background")
        elif mode == "dark_on_light":
            gray = opened.convert("L")
            low, high = gray.getextrema()
            if low > 160 or high < 220:
                raise ValueError("dark_on_light title plate needs dark ink on a light ground")
            mask = ImageOps.invert(gray).point(lambda value: 0 if value < 12 else value)
        elif mode == "light_on_dark":
            gray = opened.convert("L")
            low, high = gray.getextrema()
            if low > 35 or high < 160:
                raise ValueError("light_on_dark title plate needs light ink on a dark ground")
            mask = gray.point(lambda value: 0 if value < 12 else value)
        else:
            raise ValueError("title_plate_mode must be alpha, dark_on_light, or light_on_dark")
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError(f"title plate is empty: {path}")
    mask = mask.crop(bbox)
    scale = target_height / max(1, mask.height)
    width = max(1, round(mask.width * scale))
    return mask.resize((width, target_height), Image.Resampling.LANCZOS)


def _extend_mask(
    mask: Image.Image, extension: dict[str, Any], font_size: int
) -> Image.Image:
    edge = extension.get("edge")
    if edge not in {"top", "right", "bottom", "left"}:
        raise ValueError("glyph extension edge must be top, right, bottom, or left")
    angle = float(extension.get("direction_angle", 0.0))
    length_ratio = float(extension.get("length_ratio", 0.0))
    width_ratio = float(extension.get("width_ratio", 0.08))
    if not -90.0 <= angle <= 90.0:
        raise ValueError("glyph extension direction_angle must be between -90 and 90")
    if not 0.15 <= length_ratio <= 1.25:
        raise ValueError("glyph extension length_ratio must be between 0.15 and 1.25")
    if not 0.025 <= width_ratio <= 0.20:
        raise ValueError("glyph extension width_ratio must be between 0.025 and 0.20")

    bbox = mask.getbbox()
    if bbox is None:
        return mask
    length = max(2, round(font_size * length_ratio))
    stroke_width = max(1, round(font_size * width_ratio))
    theta = math.radians(angle)
    if edge == "bottom":
        start = (bbox[2] - stroke_width, bbox[3] - stroke_width)
        vector = (math.cos(theta) * length, math.sin(theta) * length)
    elif edge == "top":
        start = (bbox[0] + stroke_width, bbox[1] + stroke_width)
        vector = (math.cos(theta) * length, -abs(math.sin(theta) * length))
    elif edge == "right":
        start = (bbox[2] - stroke_width, (bbox[1] + bbox[3]) // 2)
        vector = (abs(math.cos(theta) * length), math.sin(theta) * length)
    else:
        start = (bbox[0] + stroke_width, (bbox[1] + bbox[3]) // 2)
        vector = (-abs(math.cos(theta) * length), math.sin(theta) * length)
    end = (round(start[0] + vector[0]), round(start[1] + vector[1]))

    pad = length + stroke_width * 2
    expanded = Image.new("L", (mask.width + pad * 2, mask.height + pad * 2), 0)
    expanded.paste(mask, (pad, pad))
    draw = ImageDraw.Draw(expanded)
    shifted_start = (start[0] + pad, start[1] + pad)
    shifted_end = (end[0] + pad, end[1] + pad)
    draw.line((shifted_start, shifted_end), fill=255, width=stroke_width)
    draw.ellipse(
        (
            shifted_end[0] - stroke_width // 3,
            shifted_end[1] - stroke_width // 3,
            shifted_end[0] + stroke_width // 3,
            shifted_end[1] + stroke_width // 3,
        ),
        fill=255,
    )
    bbox = expanded.getbbox()
    return expanded.crop(bbox) if bbox else expanded


def validate_glyph_plan(
    plan: dict[str, Any], units: list[str], style: str
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    schema_version = plan.get("schema_version")
    if schema_version not in {1, 2}:
        raise ValueError("glyph plan schema_version must be 1 or 2")
    group = plan.get("group")
    if not isinstance(group, dict):
        raise ValueError("glyph plan requires a group object")
    if group.get("material") != style:
        raise ValueError("glyph plan group.material must match style-profile")
    if group.get("skeleton") not in SKELETONS:
        raise ValueError("glyph plan group.skeleton is invalid")
    for field in (
        "source_anchor",
        "composition_function",
        "entry_behavior",
        "turn_behavior",
        "exit_behavior",
    ):
        if not str(group.get(field, "")).strip():
            raise ValueError(f"glyph plan group.{field} is required")
    title_plate = group.get("title_plate")
    if schema_version == 2:
        if not str(title_plate or "").strip():
            raise ValueError("glyph plan schema_version 2 requires group.title_plate")
        if not Path(title_plate).is_file():
            raise ValueError(f"title plate not found: {title_plate}")
        if group.get("title_plate_mode", "alpha") not in {
            "alpha",
            "dark_on_light",
            "light_on_dark",
        }:
            raise ValueError("glyph plan group.title_plate_mode is invalid")
        exact_text = str(group.get("exact_text", ""))
        if "".join(exact_text.split()) != "".join(units):
            raise ValueError("glyph plan group.exact_text must match input text")
        plate_height_ratio = float(group.get("plate_height_ratio", 1.0))
        if not 0.75 <= plate_height_ratio <= 4.0:
            raise ValueError("glyph plan group.plate_height_ratio must be 0.75 to 4.0")
        for field in (
            "title_zone",
            "group_silhouette",
            "reading_order",
            "visual_weight_target",
            "primary_color_source",
            "color_reason",
        ):
            if not str(group.get(field, "")).strip():
                raise ValueError(f"glyph plan group.{field} is required for title plates")
        line_count = int(group.get("line_count", 0))
        if not 1 <= line_count <= 3:
            raise ValueError("glyph plan group.line_count must be 1 to 3")
        if not isinstance(group.get("protected_regions"), list):
            raise ValueError("glyph plan group.protected_regions must be a list")
    elif title_plate is not None:
        raise ValueError("group.title_plate requires glyph plan schema_version 2")

    glyphs = plan.get("glyphs")
    if not isinstance(glyphs, list) or len(glyphs) != len(units):
        raise ValueError("glyph plan must contain exactly one glyph entry per unit")
    roles: list[str] = []
    extension_count = 0
    normalized: list[dict[str, Any]] = []
    for index, (unit, raw) in enumerate(zip(units, glyphs)):
        if not isinstance(raw, dict) or raw.get("unit") != unit:
            raise ValueError(f"glyph plan unit mismatch at index {index}")
        role = raw.get("role")
        if role not in GLYPH_ROLES:
            raise ValueError(f"glyph role is invalid at index {index}")
        roles.append(role)
        scale = float(raw.get("scale", 1.0))
        rotation = float(raw.get("rotation", 0.0))
        x_shift = float(raw.get("x_shift", 0.0))
        y_shift = float(raw.get("y_shift", 0.0))
        if not 0.70 <= scale <= 1.40:
            raise ValueError("glyph scale must be between 0.70 and 1.40")
        if not -15.0 <= rotation <= 15.0:
            raise ValueError("glyph rotation must be between -15 and 15")
        if not -0.35 <= x_shift <= 0.35 or not -0.35 <= y_shift <= 0.35:
            raise ValueError("glyph shifts must be between -0.35 and 0.35")
        custom_mask = raw.get("custom_mask")
        extension = raw.get("extension")
        if extension is not None:
            if not isinstance(extension, dict):
                raise ValueError("glyph extension must be an object")
            extension_count += 1
        normalized.append(
            {
                "unit": unit,
                "role": role,
                "scale": scale,
                "rotation": rotation,
                "x_shift": x_shift,
                "y_shift": y_shift,
                "custom_mask": custom_mask,
                "extension": extension,
            }
        )
    if roles.count("hero") > 1 or roles.count("connector") > 1:
        raise ValueError("glyph plan allows at most one hero and one connector")
    if extension_count > 1:
        raise ValueError("glyph plan allows at most one semantic stroke extension")

    interlock = plan.get("interlock")
    if interlock is not None:
        if not isinstance(interlock, dict):
            raise ValueError("glyph plan interlock must be an object")
        if interlock.get("mode") not in INTERLOCK_MODES:
            raise ValueError("glyph plan interlock mode is invalid")
        glyph_index = int(interlock.get("glyph_index", -1))
        if not 0 <= glyph_index < len(units):
            raise ValueError("glyph plan interlock glyph_index is invalid")
        for field in (
            "source_element",
            "source_relationship",
            "semantic_reason",
            "stopping_boundary",
            "asset",
            "color_role",
        ):
            if not str(interlock.get(field, "")).strip():
                raise ValueError(f"glyph plan interlock.{field} is required")
        if not Path(interlock["asset"]).is_file():
            raise ValueError(f"interlock asset not found: {interlock['asset']}")
        if interlock["color_role"] not in {"primary", "accent"}:
            raise ValueError("glyph plan interlock.color_role must be primary or accent")
        if interlock["mode"] == "stroke_substitution":
            region = interlock.get("erase_region")
            if not isinstance(region, list) or len(region) != 4:
                raise ValueError("stroke_substitution requires erase_region [x0,y0,x1,y1]")
            x0, y0, x1, y1 = (float(value) for value in region)
            if not (0.0 <= x0 < x1 <= 1.0 and 0.0 <= y0 < y1 <= 1.0):
                raise ValueError("stroke_substitution erase_region must be normalized")
            if (x1 - x0) * (y1 - y0) > 0.18:
                raise ValueError("stroke_substitution may erase at most 18% of the glyph box")
    return normalized, interlock


def _cut_stencil(mask: Image.Image, font_size: int, rng: random.Random) -> Image.Image:
    cuts = Image.new("L", mask.size, 0)
    draw = ImageDraw.Draw(cuts)
    gap = max(2, round(font_size / 28))
    y = round(mask.height * rng.uniform(0.43, 0.57))
    draw.rectangle((0, y, mask.width, y + gap), fill=255)
    if mask.height > font_size * 0.8:
        x = round(mask.width * rng.uniform(0.28, 0.72))
        draw.line(
            (x - gap * 2, mask.height, x + gap * 2, 0),
            fill=255,
            width=max(1, gap // 2),
        )
    return ImageChops.subtract(mask, cuts)


def _dry_marker(mask: Image.Image, font_size: int, rng: random.Random) -> Image.Image:
    textured = mask.copy()
    draw = ImageDraw.Draw(textured)
    count = max(4, round(font_size / 10))
    for _ in range(count):
        y = rng.randrange(max(1, textured.height))
        x = rng.randrange(max(1, textured.width))
        length = rng.randint(max(2, font_size // 12), max(3, font_size // 3))
        draw.line(
            (x, y, min(textured.width, x + length), y + rng.choice((-1, 0, 1))),
            fill=rng.randint(0, 70),
            width=max(1, font_size // 45),
        )
    return textured


def _materialize_mask(
    mask: Image.Image,
    size: int,
    color: tuple[int, int, int],
    accent: tuple[int, int, int],
    opacity: int,
    style: str,
    direction_angle: float,
    rng: random.Random,
) -> Image.Image:
    result = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    angle = math.radians(direction_angle)
    shift = max(1, round(size / 11))
    dx = round(math.cos(angle) * shift)
    dy = round(math.sin(angle) * shift)

    if style == "cut_stencil":
        ink = _cut_stencil(mask, size, rng)
        rim = _shift_mask(ink, max(1, dx // 3), max(1, dy // 3))
        result = Image.alpha_composite(
            result, _rgba_from_mask(rim, accent, round(opacity * 0.30))
        )
        return Image.alpha_composite(result, _rgba_from_mask(ink, color, opacity))
    if style == "dry_marker":
        ink = _dry_marker(mask, size, rng)
        pressure = _shift_mask(ink, 1, 1)
        result = Image.alpha_composite(
            result, _rgba_from_mask(pressure, accent, round(opacity * 0.22))
        )
        return Image.alpha_composite(result, _rgba_from_mask(ink, color, opacity))
    if style == "offset_screenprint":
        shifted = _shift_mask(mask, dx, dy)
        result = Image.alpha_composite(
            result, _rgba_from_mask(shifted, accent, round(opacity * 0.70))
        )
        return Image.alpha_composite(result, _rgba_from_mask(mask, color, opacity))
    if style == "pencil_note":
        ink = _dry_marker(mask, max(12, size // 2), rng)
        result = Image.alpha_composite(
            result,
            _rgba_from_mask(_shift_mask(ink, 1, 0), accent, round(opacity * 0.28)),
        )
        return Image.alpha_composite(result, _rgba_from_mask(ink, color, opacity))
    if style == "brush_ink":
        spread_mask = mask.filter(ImageFilter.MaxFilter(3))
        ink = _dry_marker(mask, max(12, size // 2), rng)
        result = Image.alpha_composite(
            result, _rgba_from_mask(spread_mask, accent, round(opacity * 0.16))
        )
        return Image.alpha_composite(result, _rgba_from_mask(ink, color, opacity))
    if style == "fountain_pen":
        ink = mask.filter(ImageFilter.MinFilter(3))
        result = Image.alpha_composite(
            result,
            _rgba_from_mask(_shift_mask(ink, 1, 1), accent, round(opacity * 0.18)),
        )
        return Image.alpha_composite(result, _rgba_from_mask(ink, color, opacity))
    if style == "paint_brush":
        ink = _dry_marker(mask.filter(ImageFilter.MaxFilter(3)), size, rng)
        result = Image.alpha_composite(
            result,
            _rgba_from_mask(_shift_mask(ink, 1, 1), accent, round(opacity * 0.20)),
        )
        return Image.alpha_composite(result, _rgba_from_mask(ink, color, opacity))
    raise ValueError(f"unknown art lettering style: {style}")


def _render_unit(
    unit: str,
    font_path: Path,
    base_size: int,
    color: tuple[int, int, int],
    accent: tuple[int, int, int],
    opacity: int,
    style: str,
    direction_angle: float,
    rng: random.Random,
    glyph_spec: dict[str, Any] | None = None,
) -> Image.Image:
    spread = 0.025 if style == "pencil_note" else 0.09
    if glyph_spec is None:
        size = max(1, round(base_size * rng.uniform(1 - spread, 1 + spread)))
    else:
        size = max(1, round(base_size * glyph_spec["scale"]))
    font = ImageFont.truetype(str(font_path), size)
    if glyph_spec is not None and glyph_spec.get("custom_mask"):
        mask = _load_custom_mask(Path(glyph_spec["custom_mask"]), size)
    else:
        mask = _glyph_mask(unit, font)
    if glyph_spec is not None and glyph_spec.get("extension"):
        mask = _extend_mask(mask, glyph_spec["extension"], size)
    result = _materialize_mask(
        mask, size, color, accent, opacity, style, direction_angle, rng
    )

    if glyph_spec is None:
        tilt = rng.uniform(-2.0, 2.0) if style == "pencil_note" else rng.uniform(-5.0, 5.0)
        if style == "dry_marker":
            tilt *= 1.35
    else:
        tilt = glyph_spec["rotation"]
    rotated = result.rotate(tilt, expand=True, resample=Image.Resampling.BICUBIC)
    bbox = rotated.getchannel("A").getbbox()
    if bbox is None:
        return rotated
    margin = max(2, round(size * 0.04))
    left = max(0, bbox[0] - margin)
    top = max(0, bbox[1] - margin)
    right = min(rotated.width, bbox[2] + margin)
    bottom = min(rotated.height, bbox[3] + margin)
    return rotated.crop((left, top, right, bottom))


def _apply_interlock(
    image: Image.Image,
    interlock: dict[str, Any],
    font_size: int,
    color: tuple[int, int, int],
    accent: tuple[int, int, int],
) -> Image.Image:
    with Image.open(interlock["asset"]) as opened:
        if "A" not in opened.getbands():
            raise ValueError("interlock asset must have a transparent background")
        asset = opened.convert("RGBA")
    if asset.getchannel("A").getextrema() == (255, 255):
        raise ValueError("interlock asset must have a transparent background")
    bbox = asset.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("interlock asset must contain visible pixels")
    asset = asset.crop(bbox)
    scale = float(interlock.get("scale", 0.75))
    if not 0.20 <= scale <= 1.50:
        raise ValueError("interlock scale must be between 0.20 and 1.50")
    target_height = max(1, round(font_size * scale))
    target_width = max(1, round(asset.width * target_height / asset.height))
    asset = asset.resize((target_width, target_height), Image.Resampling.LANCZOS)
    tint = color if interlock["color_role"] == "primary" else accent
    tinted = Image.new("RGBA", asset.size, (*tint, 0))
    tinted.putalpha(asset.getchannel("A"))
    asset = tinted
    x_ratio = float(interlock.get("x", 0.5))
    y_ratio = float(interlock.get("y", 0.5))
    if not -0.50 <= x_ratio <= 1.50 or not -0.50 <= y_ratio <= 1.50:
        raise ValueError("interlock x and y must be between -0.50 and 1.50")

    x = round(image.width * x_ratio - asset.width / 2)
    y = round(image.height * y_ratio - asset.height / 2)
    mode = interlock["mode"]
    if mode == "material_transfer":
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        layer.alpha_composite(asset, (x, y))
        alpha = ImageChops.multiply(layer.getchannel("A"), image.getchannel("A"))
        layer.putalpha(alpha)
        return Image.alpha_composite(image, layer)
    if mode == "counterform_reveal":
        glyph_alpha = image.getchannel("A").point(lambda value: 255 if value > 24 else 0)
        empty = ImageChops.invert(glyph_alpha)
        exterior = empty.copy()
        ImageDraw.floodfill(exterior, (0, 0), 0, thresh=0)
        counterform = exterior
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        layer.alpha_composite(asset, (x, y))
        layer.putalpha(ImageChops.multiply(layer.getchannel("A"), counterform))
        return Image.alpha_composite(layer, image)
    if mode == "stroke_substitution":
        result = image.copy()
        x0, y0, x1, y1 = (float(value) for value in interlock["erase_region"])
        alpha = result.getchannel("A")
        ImageDraw.Draw(alpha).rectangle(
            (
                round(image.width * x0),
                round(image.height * y0),
                round(image.width * x1),
                round(image.height * y1),
            ),
            fill=0,
        )
        result.putalpha(alpha)
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        layer.alpha_composite(asset, (x, y))
        return Image.alpha_composite(result, layer)

    pad = max(asset.width, asset.height, round(font_size * 0.25))
    result = Image.new(
        "RGBA", (image.width + pad * 2, image.height + pad * 2), (0, 0, 0, 0)
    )
    glyph_pos = (pad, pad)
    asset_pos = (pad + x, pad + y)
    if mode in {
        "stroke_continuation",
        "occlusion_interlock",
        "glyph_to_field",
    }:
        result.alpha_composite(image, glyph_pos)
        result.alpha_composite(asset, asset_pos)
    else:
        raise ValueError(f"unsupported interlock mode: {mode}")
    bbox = result.getchannel("A").getbbox()
    return result.crop(bbox) if bbox else result


def _line_positions(images: list[Image.Image], gap: int) -> list[tuple[int, int]]:
    max_height = max(image.height for image in images)
    positions: list[tuple[int, int]] = []
    x = 0
    for index, image in enumerate(images):
        y = max_height - image.height + (gap // 2 if index % 2 else 0)
        positions.append((x, y))
        x += image.width + gap
    return positions


def _layout_positions(
    images: list[Image.Image], layout: str, gap: int, direction_angle: float
) -> list[tuple[int, int]]:
    if layout == "line":
        return _line_positions(images, gap)
    if layout == "vertical":
        width = max(image.width for image in images)
        y = 0
        positions = []
        for index, image in enumerate(images):
            positions.append(((width - image.width) // 2 + (gap // 2 if index % 2 else 0), y))
            y += image.height + max(1, gap // 3)
        return positions
    if layout == "path_aligned":
        positions = _line_positions(images, gap)
        slope = math.tan(math.radians(direction_angle))
        shifted = [(x, y + round(x * slope)) for x, y in positions]
        min_y = min(y for _, y in shifted)
        return [(x, y - min_y) for x, y in shifted]

    split = max(1, math.ceil(len(images) / 2))
    rows = (images[:split], images[split:])
    positions: list[tuple[int, int]] = []
    y = 0
    for row_index, row in enumerate(rows):
        if not row:
            continue
        row_positions = _line_positions(list(row), gap)
        indent = gap * row_index if layout == "stacked" else gap // 2 * row_index
        for (x, local_y), image in zip(row_positions, row):
            positions.append((x + indent, y + local_y))
        y += max(image.height for image in row) + (gap if layout == "stacked" else gap // 2)
    return positions


def render_lettering(
    canvas_size: tuple[int, int],
    position: tuple[int, int],
    text: str,
    language: str,
    font_path: Path,
    font_size: int,
    align: str,
    color: tuple[int, int, int],
    accent: tuple[int, int, int],
    opacity: int,
    style: str,
    layout: str,
    direction_angle: float,
    glyph_plan: dict[str, Any] | None = None,
) -> tuple[Image.Image, dict[str, object]]:
    units = _units(text, language)
    if not units:
        raise ValueError("art lettering produced no layout units")
    glyph_specs: list[dict[str, Any] | None]
    interlock: dict[str, Any] | None = None
    if glyph_plan is None:
        glyph_specs = [None] * len(units)
    else:
        validated, interlock = validate_glyph_plan(glyph_plan, units, style)
        glyph_specs = list(validated)
    rng = random.Random(_seed(text, language, style, layout, direction_angle, glyph_plan))
    group = glyph_plan.get("group", {}) if glyph_plan is not None else {}
    if group.get("title_plate"):
        target_height = max(
            1, round(font_size * float(group.get("plate_height_ratio", 1.0)))
        )
        mask = _load_title_plate(
            Path(group["title_plate"]),
            target_height,
            str(group.get("title_plate_mode", "alpha")),
        )
        block = _materialize_mask(
            mask,
            target_height,
            color,
            accent,
            opacity,
            style,
            direction_angle,
            rng,
        )
        if interlock is not None:
            block = _apply_interlock(block, interlock, font_size, color, accent)
        anchor_x, anchor_y = position
        dest_x = anchor_x if align == "left" else anchor_x - block.width
        layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        layer.alpha_composite(block, (dest_x, anchor_y))
        return layer, {
            "lettering_layout": layout,
            "unit_count": len(units),
            "block_size": [block.width, block.height],
            "direction_angle": direction_angle,
            "glyph_plan": True,
            "glyph_roles": [spec["role"] for spec in glyph_specs],
            "interlock_mode": interlock["mode"] if interlock else None,
            "title_plate": True,
            "title_plate_mode": str(group.get("title_plate_mode", "alpha")),
        }
    images = [
        _render_unit(
            unit,
            font_path,
            font_size,
            color,
            accent,
            opacity,
            style,
            direction_angle,
            rng,
            glyph_spec,
        )
        for unit, glyph_spec in zip(units, glyph_specs)
    ]
    if glyph_plan is None and layout in {"stacked", "compact_block"} and len(images) >= 3:
        split = max(1, math.ceil(len(images) / 2))
        emphasis = 1.16 if layout == "stacked" else 1.10
        for index in range(split, len(images)):
            image = images[index]
            images[index] = image.resize(
                (round(image.width * emphasis), round(image.height * emphasis)),
                Image.Resampling.LANCZOS,
            )
    if interlock is not None:
        target = int(interlock["glyph_index"])
        images[target] = _apply_interlock(
            images[target], interlock, font_size, color, accent
        )
    gap = max(2, round(font_size * (0.18 if language == "en" else 0.08)))
    positions = _layout_positions(images, layout, gap, direction_angle)
    if glyph_plan is not None:
        positions = [
            (
                x + round(font_size * spec["x_shift"]),
                y + round(font_size * spec["y_shift"]),
            )
            for (x, y), spec in zip(positions, glyph_specs)
            if spec is not None
        ]
        min_x = min(x for x, _ in positions)
        min_y = min(y for _, y in positions)
        positions = [(x - min_x, y - min_y) for x, y in positions]
    width = max(x + image.width for (x, _), image in zip(positions, images))
    height = max(y + image.height for (_, y), image in zip(positions, images))
    block = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for image, (x, y) in zip(images, positions):
        block.alpha_composite(image, (x, y))

    anchor_x, anchor_y = position
    dest_x = anchor_x if align == "left" else anchor_x - block.width
    layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    layer.alpha_composite(block, (dest_x, anchor_y))
    return layer, {
        "lettering_layout": layout,
        "unit_count": len(units),
        "block_size": [block.width, block.height],
        "direction_angle": direction_angle,
        "glyph_plan": glyph_plan is not None,
        "glyph_roles": [spec["role"] for spec in glyph_specs if spec is not None],
        "interlock_mode": interlock["mode"] if interlock else None,
        "title_plate": False,
    }
