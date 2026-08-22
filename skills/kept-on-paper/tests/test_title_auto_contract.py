import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class TitleAutoContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.editor = (SKILL_ROOT / "references/title-editor.md").read_text(
            encoding="utf-8"
        )
        cls.typography = (
            SKILL_ROOT / "references/typography-and-language.md"
        ).read_text(encoding="utf-8")
        cls.lettering = (SKILL_ROOT / "references/lettering-engine.md").read_text(
            encoding="utf-8"
        )

    def test_auto_uses_title_first_fallback_chain(self):
        self.assertIn("SHORT_TITLE → DEFINITION_LINE → OFF", self.skill)
        self.assertIn("SHORT_TITLE → DEFINITION_LINE → OFF", self.editor)

    def test_title_plus_line_is_optional_and_non_redundant(self):
        self.assertIn("TITLE_PLUS_LINE", self.skill)
        self.assertIn("TITLE_PLUS_LINE", self.editor)
        self.assertIn("REDUNDANCY_CHECK", self.editor)
        self.assertIn("标题负责视觉命名或记忆锚定", self.editor)
        self.assertIn("小句负责不重复的情绪回应", self.editor)

    def test_english_title_is_preferred_only_when_language_quality_is_comparable(self):
        self.assertIn("两者在 `GROUNDED`、`RESONANT`、`SPECIFIC`", self.skill)
        self.assertIn("两种语言质量相当时，优先英文短标题", self.editor)
        self.assertIn("英文偏好不是硬配额", self.editor)
        self.assertIn("英文主标题 + 中文小句", self.editor)
        self.assertIn("英文主标题 + 中文支持句", self.typography)
        self.assertIn("不得是逐字直译", self.editor)
        self.assertIn("不得为了制造杂志感自动添加伪栏目", self.editor)

    def test_emotional_resonance_is_allowed_without_story_invention(self):
        self.assertIn("NARRATIVE_HALLUCINATION", self.editor)
        self.assertIn("EMOTIONAL_RESONANCE", self.editor)
        self.assertIn("EMOTIONAL_ECHO", self.editor)
        self.assertIn("不替画中人物宣布内心", self.editor)

    def test_reasonable_visual_inference_uses_multiple_evidence(self):
        self.assertIn("Reasonable Visual Inference", self.editor)
        self.assertIn("由多个明确视觉证据共同支持", self.editor)
        self.assertIn("冬日渔港", self.editor)
        self.assertIn("北海道冬日渔港", self.editor)

    def test_fact_trace_replaces_one_hop_poetry_limit(self):
        self.assertNotIn("诗性最多跨一层", self.skill)
        self.assertNotIn("一层诗性上限", self.editor)
        self.assertIn("OBSERVED", self.editor)
        self.assertIn("REASONABLE_INFERENCE", self.editor)
        self.assertIn("EMOTIONAL_SYNTHESIS", self.editor)

    def test_copy_ranking_balances_grounded_resonant_specific(self):
        self.assertIn("GROUNDED + RESONANT + SPECIFIC", self.editor)
        self.assertIn("不再让事实字面度压倒其他指标", self.editor)

    def test_generic_emotion_terms_require_visual_anchor(self):
        self.assertIn("SCENE_SWAP", self.editor)
        self.assertIn("ANCHOR_REMOVAL", self.editor)
        self.assertIn("FORMULA_REUSE", self.editor)
        self.assertIn("不是禁词", self.editor)
        self.assertIn("不能自己充当视觉证据", self.editor)
        self.assertIn("愿所有美好如期而至", self.editor)
        self.assertIn("海风很冷，但日子总会有温柔的光", self.editor)

    def test_should_title_has_positive_evidence_gate(self):
        self.assertIn("两个及以上普通信号", self.editor)
        self.assertIn("HIGH_SPECIFICITY", self.editor)
        self.assertIn("SHOULD_TITLE", self.skill)

    def test_missing_art_zone_falls_back_to_definition(self):
        self.assertIn("没有安全艺术字区", self.editor)
        self.assertIn("必须回退小号定义句", self.typography)

    def test_off_requires_candidate_failures(self):
        self.assertIn("2–4 个短标题候选及至少一个定义句候选", self.editor)
        self.assertIn("candidate → failed gate → visible evidence", self.editor)

    def test_batch_off_collapse_is_rechecked(self):
        self.assertIn("超过约 75%", self.skill)
        self.assertIn("超过约 75%", self.editor)

    def test_semantic_and_visual_title_roles_are_separate(self):
        self.assertIn("Title Route Card", self.skill)
        self.assertIn("HERO_TITLE", self.skill)
        self.assertIn("SUPPORT_TITLE", self.typography)
        self.assertIn("CAPTION", self.typography)

    def test_batch_small_title_collapse_is_rechecked(self):
        self.assertIn("超过约 75% 都是 `CAPTION`", self.skill)
        self.assertIn("统一小字", self.skill)

    def test_title_plate_v2_is_a_conditional_fallback(self):
        self.assertIn("文字与画面默认进入同一段最终提示词", self.skill)
        self.assertIn("schema_version: 2 title_plate", self.skill)
        self.assertIn("不是普通短标题的默认税", self.skill)
        self.assertIn("schema_version: 1", self.lettering)
        self.assertIn("不能通过最终排字入口", self.lettering)

    def test_short_title_requires_per_glyph_audit(self):
        self.assertIn("Title Glyph Audit", self.skill)
        self.assertIn("Title Glyph Audit", self.lettering)
        self.assertIn("逐字确认可见定制决定", self.skill)
        self.assertIn("standard_font_difference", self.lettering)

    def test_standard_font_substitution_is_a_hard_gate(self):
        self.assertIn("标准字体替代测试", self.skill)
        self.assertIn("标准字体替代测试", self.lettering)
        self.assertIn("color_or_position_only", self.lettering)
        self.assertIn("replaceable: false", self.lettering)

    def test_pencil_note_cannot_bypass_raster_audit(self):
        self.assertIn("包括 `PENCIL_NOTE`", self.skill)
        self.assertIn("包括 `PENCIL_NOTE`", self.typography)
        self.assertIn("仍须逐字审核", self.typography)

    def test_glyph_correctness_precedes_custom_design(self):
        self.assertIn("GLYPH_CORRECTNESS", self.skill)
        self.assertIn("glyph_correctness_gate", self.lettering)
        self.assertIn("standard_font_substitution_test", self.lettering)
        self.assertIn("不能反向证明字形正确", self.lettering)

    def test_source_exact_marks_cannot_be_dropped_with_title(self):
        self.assertIn("SOURCE_EXACT_MARK", self.editor)
        self.assertIn("SOURCE_EXACT_MARK", self.typography)
        self.assertIn("不得因标题为 `OFF` 而省略", self.typography)


if __name__ == "__main__":
    unittest.main()
