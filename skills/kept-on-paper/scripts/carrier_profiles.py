#!/usr/bin/env python3
"""Shared deterministic geometry for Kept on Paper carriers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CarrierProfile:
    width: int
    height: int
    shape: str = "rectangle"
    center_hole_radius_ratio: float = 0.0
    text_exclusion_radius_ratio: float = 0.0


PROFILES = {
    "FULL_FRAME_3_5": CarrierProfile(1200, 2000),
    "PICTURE_DISC_1_1": CarrierProfile(
        1800,
        1800,
        shape="circle",
        center_hole_radius_ratio=0.018,
        text_exclusion_radius_ratio=0.10,
    ),
}


def get_profile(name: str) -> CarrierProfile:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"unknown carrier profile: {name}") from exc
