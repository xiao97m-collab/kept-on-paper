import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class SourceFidelityContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.fidelity = (
            SKILL_ROOT / "references/source-fidelity-and-improvement.md"
        ).read_text(encoding="utf-8")
        cls.space = (SKILL_ROOT / "references/surface-and-space.md").read_text(
            encoding="utf-8"
        )
        cls.palette = (SKILL_ROOT / "references/palette-system.md").read_text(
            encoding="utf-8"
        )

    def test_source_lock_protects_relations_not_only_objects(self):
        for marker in (
            "scene_substrate",
            "exact_marks",
            "causal_palette",
            "scale_and_view",
            "visible_improvement_target",
        ):
            self.assertIn(marker, self.skill)
            self.assertIn(marker, self.fidelity)

    def test_breathing_field_is_not_white_paper_quota(self):
        self.assertIn("低信息呼吸区不等于裸露白纸", self.fidelity)
        self.assertIn("scene_substrate.may_become_bare_base=true", self.space)
        self.assertIn("水面", self.space)
        self.assertIn("草坡", self.space)

    def test_smallest_sufficient_change_replaces_delta_quota(self):
        self.assertIn("Smallest Sufficient Transformation", self.fidelity)
        self.assertIn("不按数量强制 Structural Delta", self.fidelity)
        self.assertIn("T0/T1", self.skill)

    def test_plan_may_offer_guarded_t3_without_weakening_execution_safety(self):
        self.assertIn("PLAN 探索例外", self.fidelity)
        self.assertIn("受保护的 T3 方向", self.fidelity)
        self.assertIn("不等于自动执行许可", self.fidelity)
        self.assertIn("RANDOM", self.fidelity)

    def test_exact_marks_have_a_deterministic_failure_route(self):
        self.assertIn("UNRESOLVED_EXACT_MARK", self.fidelity)
        self.assertIn("不得近似、改写或省略", self.fidelity)
        self.assertIn("精确标志缺失或近似即失败", self.skill)

    def test_color_gate_protects_relationship_and_area(self):
        self.assertIn("dominant_relation", self.palette)
        self.assertIn("area_relation", self.palette)
        self.assertIn("纸面颜色不能成为新主色", self.palette)

    def test_visible_improvement_is_a_delivery_gate(self):
        self.assertIn("`IMPROVEMENT`", self.skill)
        self.assertIn("原图、简单裁切/色彩修复基线与成品", self.skill)
        self.assertIn("仅更空、更不同或更有风格不能通过", self.skill)

    def test_compact_prompt_does_not_delete_protected_background(self):
        self.assertIn("no deletion of protected scene substrate", self.skill)
        self.assertNotIn("no complete background", self.skill)
        self.assertNotIn("no preserved photographic depth", self.skill)


if __name__ == "__main__":
    unittest.main()
