from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).parents[1] / "scripts" / "prepare_carrier_canvas.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("prepare_carrier_canvas", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PrepareCarrierCanvasTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.png"
        Image.new("RGB", (600, 1000), (246, 241, 226)).save(self.source)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def args(self, profile: str, **overrides: object) -> Namespace:
        values = {
            "input": self.source,
            "output": self.root / f"{profile}.png",
            "carrier_profile": profile,
            "centering_x": 0.5,
            "centering_y": 0.5,
            "max_crop_fraction": 0.50,
        }
        values.update(overrides)
        return Namespace(**values)

    def test_full_frame_size(self) -> None:
        args = self.args("FULL_FRAME_3_5")
        metrics = MODULE.prepare(args)
        self.assertEqual(metrics["output_size"], [1200, 2000])
        with Image.open(args.output) as opened:
            self.assertEqual(opened.size, (1200, 2000))

    def test_all_profile_dimensions_are_locked(self) -> None:
        expected = {
            "FULL_FRAME_3_5": (1200, 2000),
            "PICTURE_DISC_1_1": (1800, 1800),
        }
        actual = {name: (p.width, p.height) for name, p in MODULE.PROFILES.items()}
        self.assertEqual(actual, expected)

    def test_picture_disc_circle_and_center_hole_are_transparent(self) -> None:
        args = self.args("PICTURE_DISC_1_1")
        MODULE.prepare(args)
        image = Image.open(args.output).convert("RGBA")
        self.assertEqual(image.getpixel((0, 0))[3], 0)
        self.assertEqual(image.getpixel((900, 900))[3], 0)
        self.assertEqual(image.getpixel((900, 300))[3], 255)

    def test_removed_profiles_are_rejected(self) -> None:
        for profile in (
            "BOOKMARK_1_3",
            "POSTER_2_3",
            "ALBUM_COVER_1_1",
            "VINYL_LABEL_1_1",
            "FRIDGE_MAGNET_4_5",
        ):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                MODULE.get_profile(profile)

    def test_rejects_excessive_crop(self) -> None:
        Image.new("RGB", (1000, 200), (246, 241, 226)).save(self.source)
        with self.assertRaises(MODULE.CarrierPreparationError):
            MODULE.prepare(self.args("PICTURE_DISC_1_1"))


if __name__ == "__main__":
    unittest.main()
