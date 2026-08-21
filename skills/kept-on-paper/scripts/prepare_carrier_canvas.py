#!/usr/bin/env python3
"""Fit generated art to a deterministic Kept on Paper carrier canvas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from carrier_profiles import PROFILES, CarrierProfile, get_profile


class CarrierPreparationError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--carrier-profile", required=True, choices=tuple(PROFILES))
    parser.add_argument("--centering-x", type=float, default=0.5)
    parser.add_argument("--centering-y", type=float, default=0.5)
    parser.add_argument("--max-crop-fraction", type=float, default=0.50)
    return parser.parse_args()


def crop_fraction(source: tuple[int, int], target: tuple[int, int]) -> float:
    source_ratio = source[0] / source[1]
    target_ratio = target[0] / target[1]
    retained = target_ratio / source_ratio if source_ratio > target_ratio else source_ratio / target_ratio
    return 1.0 - retained


def carrier_mask(profile: CarrierProfile) -> Image.Image | None:
    if profile.shape == "rectangle":
        return None

    mask = Image.new("L", (profile.width, profile.height), 0)
    draw = ImageDraw.Draw(mask)
    if profile.shape == "circle":
        draw.ellipse((0, 0, profile.width - 1, profile.height - 1), fill=255)
        radius = round(min(profile.width, profile.height) * profile.center_hole_radius_ratio)
        cx, cy = profile.width // 2, profile.height // 2
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=0)
    else:
        raise CarrierPreparationError(f"unsupported carrier shape: {profile.shape}")
    return mask


def prepare(args: argparse.Namespace) -> dict[str, object]:
    if not args.input.is_file():
        raise CarrierPreparationError(f"input not found: {args.input}")
    for name in ("centering_x", "centering_y"):
        if not 0.0 <= getattr(args, name) <= 1.0:
            raise CarrierPreparationError(f"{name.replace('_', '-')} must be between 0 and 1")
    if not 0.0 <= args.max_crop_fraction <= 0.50:
        raise CarrierPreparationError("max-crop-fraction must be between 0 and 0.50")

    profile = get_profile(args.carrier_profile)
    with Image.open(args.input) as opened:
        source = opened.convert("RGBA")
    discarded = crop_fraction(source.size, (profile.width, profile.height))
    if discarded > args.max_crop_fraction:
        raise CarrierPreparationError(
            f"carrier crop would discard {discarded:.1%}, above {args.max_crop_fraction:.1%}; regenerate with carrier-aware composition"
        )

    fitted = ImageOps.fit(
        source,
        (profile.width, profile.height),
        method=Image.Resampling.LANCZOS,
        centering=(args.centering_x, args.centering_y),
    )
    mask = carrier_mask(profile)
    if mask is not None:
        fitted.putalpha(mask)
        result = fitted
    else:
        result = fitted.convert("RGB")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output, format="PNG", optimize=True)
    return {
        "input": str(args.input),
        "output": str(args.output),
        "carrier_profile": args.carrier_profile,
        "source_size": list(source.size),
        "output_size": [profile.width, profile.height],
        "shape": profile.shape,
        "crop_fraction": round(discarded, 6),
    }


def main() -> int:
    try:
        metrics = prepare(parse_args())
    except (OSError, CarrierPreparationError, ValueError) as exc:
        print(f"carrier preparation error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(metrics, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
