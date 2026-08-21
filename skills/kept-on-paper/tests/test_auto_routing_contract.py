import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class AutoRoutingContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.agent_config = (SKILL_ROOT / "agents/openai.yaml").read_text(
            encoding="utf-8"
        )
        cls.router = (SKILL_ROOT / "references/auto-routing.md").read_text(
            encoding="utf-8"
        )
        cls.cases = json.loads(
            (SKILL_ROOT / "tests/fixtures/routing_cases.json").read_text(
                encoding="utf-8"
            )
        )

    def test_main_skill_locks_one_visual_language(self):
        self.assertIn("Generation Lock", self.skill)
        self.assertIn("PAINTERLY_DISTILLATION", self.skill)
        self.assertIn("只有一种主要视觉语言", self.router)
        self.assertIn("不得用混合风格折中", self.skill)

    def test_auto_router_is_conditionally_loaded(self):
        self.assertIn("references/auto-routing.md", self.skill)
        self.assertIn("安全回退", self.router)

    def test_main_runtime_contract_stays_compact(self):
        self.assertLess(len(self.skill), 22000)
        self.assertLess(len(self.skill.splitlines()), 300)

    def test_new_source_plan_requires_three_direction_choice_gate(self):
        self.assertIn("NEW_SOURCE + PLAN", self.skill)
        self.assertIn("输出恰好三个编号方向", self.skill)
        self.assertIn("选择前禁止编译最终提示词", self.skill)
        self.assertIn("只有选择明确后", self.skill)
        self.assertIn("RANDOM", self.skill)
        self.assertIn("绕过此门", self.skill)

    def test_first_invocation_onboards_without_reasking_for_an_attached_image(self):
        self.assertIn("当前对话第一次调用本 Skill", self.skill)
        self.assertIn("同一对话后续不重复", self.skill)
        self.assertIn("首次调用但没有图片", self.skill)
        self.assertIn("首次调用已经带图", self.skill)
        self.assertIn("不要求重新上传", self.skill)

    def test_plan_is_default_and_random_requires_explicit_intent(self):
        self.assertIn("workflow_mode", self.skill)
        self.assertIn("默认 `PLAN`", self.skill)
        self.assertIn("不能暗中改成 `RANDOM`", self.skill)
        self.assertIn("用户明确说", self.skill)
        self.assertIn("不输出三张 Direction Card", self.skill)
        self.assertIn("直接编译单段提示词并生成一张成品", self.skill)

    def test_direction_cards_explain_only_terms_they_use(self):
        for term in (
            "`T1`：",
            "`T2`：",
            "`T3`：",
            "`OPEN_SPACE`：",
            "`QUIET_FILLED_FIELD`：",
            "`DENSE_EDITORIAL_FIELD`：",
        ):
            self.assertIn(term, self.skill)
        self.assertIn("每次只解释当前卡片实际使用的术语", self.skill)
        self.assertIn("不要粘贴完整术语表", self.skill)

    def test_agent_prompt_exposes_plan_random_and_continuous_revision(self):
        self.assertIn("$kept-on-paper", self.agent_config)
        self.assertIn("默认进入 Plan", self.agent_config)
        self.assertIn("Random", self.agent_config)
        self.assertIn("继续提出修改", self.agent_config)

    def test_successful_delivery_invites_source_locked_iteration(self):
        self.assertIn("每次成功交付后必须", self.skill)
        self.assertIn("如果还有新想法，可以继续告诉我", self.skill)
        self.assertIn("后续修改进入 `REUSE_SOURCE`", self.skill)
        self.assertIn("只修改你提出的部分", self.skill)
        self.assertIn("不改变用户未提及的事实", self.skill)

    def test_active_runtime_has_a_five_minute_hard_budget(self):
        self.assertIn("累计不得超过 300 秒", self.skill)
        self.assertIn("NEW_SOURCE + PLAN → 三方向`：60 秒", self.skill)
        self.assertIn("NEW_SOURCE + RANDOM → 最终交付`：300 秒", self.skill)
        self.assertIn("用户选择 → 最终交付`：240 秒", self.skill)
        self.assertIn("用户等待选择的时间不计", self.skill)

    def test_selected_direction_uses_one_final_prompt_and_one_image_call(self):
        self.assertIn("同一段最终提示词", self.skill)
        self.assertIn("原图为唯一事实母本", self.skill)
        self.assertIn("默认一次图像生成", self.skill)
        self.assertIn("不先做无字底图、字牌或拼图", self.skill)

    def test_regression_set_has_twelve_unique_source_classes(self):
        self.assertEqual(len(self.cases), 12)
        self.assertEqual(len({case["id"] for case in self.cases}), 12)
        self.assertEqual(len({case["source_class"] for case in self.cases}), 12)

    def test_every_case_has_a_complete_route_contract(self):
        required = {
            "id",
            "source_class",
            "primary_language",
            "allowed_space",
            "eligible_upgrade",
            "forbidden_auto",
            "preferred_medium",
            "critical_risk",
        }
        languages = {
            "PAINTERLY_DISTILLATION",
            "INTERACTIVE_LINE",
            "EDITORIAL_GRAFFITI",
        }
        for case in self.cases:
            self.assertEqual(set(case), required)
            self.assertIn(case["primary_language"], languages)
            self.assertTrue(case["allowed_space"])
            self.assertTrue(case["preferred_medium"])
            self.assertTrue(case["critical_risk"])

    def test_identity_and_editorial_boundaries_are_locked(self):
        cases = {case["id"]: case for case in self.cases}
        self.assertEqual(
            cases["identity_portrait"]["primary_language"],
            "PAINTERLY_DISTILLATION",
        )
        self.assertIn(
            "EDITORIAL_GRAFFITI", cases["identity_portrait"]["forbidden_auto"]
        )
        self.assertEqual(
            cases["urban_poster_rhythm"]["primary_language"],
            "EDITORIAL_GRAFFITI",
        )
        self.assertEqual(
            cases["open_relation_gesture"]["primary_language"],
            "INTERACTIVE_LINE",
        )


if __name__ == "__main__":
    unittest.main()
