from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "sepia" / "SKILL.md"
REFERENCES = ROOT / "skills" / "sepia" / "references"
VERSION = "0.6.0"


class MultilingualContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        path = ROOT / relative
        self.assertTrue(path.is_file(), f"missing required file: {relative}")
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.strip(), f"required file is empty: {relative}")
        return text

    def test_language_reference_files_exist(self) -> None:
        required = [
            "skills/sepia/references/language-routing.md",
            "skills/sepia/references/human-voice.md",
            "skills/sepia/references/voice-profile-config.md",
            "skills/sepia/references/languages/shared.md",
            "skills/sepia/references/languages/ja-JP.md",
            "skills/sepia/references/languages/en.md",
            "skills/sepia/references/languages/es.md",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.read(relative)

    def test_skill_routes_every_supported_language(self) -> None:
        skill = self.read("skills/sepia/SKILL.md")
        for reference in (
            "references/language-routing.md",
            "references/human-voice.md",
            "references/voice-profile-config.md",
            "references/languages/shared.md",
            "references/languages/ja-JP.md",
            "references/languages/en.md",
            "references/languages/es.md",
        ):
            with self.subTest(reference=reference):
                self.assertIn(f"`{reference}`", skill)

        priority = (
            "explicit requested output language → explicit locale or audience variety "
            "→ source text's established language and locale → surrounding user language "
            "→ conservative fallback"
        )
        self.assertIn(priority, skill)

    def test_voice_contract_rejects_fake_human_noise(self) -> None:
        skill = self.read("skills/sepia/SKILL.md")
        voice = self.read("skills/sepia/references/human-voice.md")
        combined = skill + "\n" + voice
        required_phrases = [
            "Never simulate humanity by adding mistakes",
            "Do not inject typos",
            "fake hesitations",
            "A new structure does not authorize a new personality",
            "Do not invent a numerical",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)

    def test_explicit_voice_profile_is_opt_in_and_constrained(self) -> None:
        skill = self.read("skills/sepia/SKILL.md")
        contract = self.read("skills/sepia/references/voice-profile-config.md")
        example = self.read("examples/voice-profile.example.yaml")
        self.assertIn("never auto-discover a profile", skill)
        self.assertIn("Use a profile only when the user provides it inline", contract)
        self.assertIn("cannot select a different operation", contract)
        self.assertIn('schema_version: "1.0"', example)
        self.assertIn('translation: "explicit-only"', example)
        self.assertIn('humor: "observed-only"', example)
        self.assertIn("invented personal experience", example)

    def test_detector_evasion_is_not_a_goal(self) -> None:
        skill = self.read("skills/sepia/SKILL.md")
        shared = self.read("skills/sepia/references/languages/shared.md")
        self.assertIn("Never optimize for AI-detector scores", skill)
        self.assertIn("not authorship tests", shared)
        self.assertNotIn("guaranteed undetectable", (skill + shared).lower())

    def test_locale_specific_invariants_are_present(self) -> None:
        ja = self.read("skills/sepia/references/languages/ja-JP.md")
        en = self.read("skills/sepia/references/languages/en.md")
        es = self.read("skills/sepia/references/languages/es.md")

        for phrase in ("主語・目的語", "です・ます", "させていただく", "整えすぎ"):
            self.assertIn(phrase, ja)
        for phrase in ("colour", "organise", "Do not add contractions", "Formality is not an AI tell"):
            self.assertIn(phrase, en)
        for phrase in ("tú", "usted", "vos", "vosotros", "signos de apertura"):
            self.assertIn(phrase, es)

    def test_version_declarations_match(self) -> None:
        manifests = [
            ROOT / ".claude-plugin" / "plugin.json",
            ROOT / ".codex-plugin" / "plugin.json",
        ]
        declared = []
        for manifest in manifests:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            declared.append(data["version"])

        skill = SKILL.read_text(encoding="utf-8")
        match = re.search(r"(?m)^  version: \"([^\"]+)\"$", skill)
        self.assertIsNotNone(match, "canonical skill must declare metadata.version")
        declared.append(match.group(1))
        self.assertEqual([VERSION, VERSION, VERSION], declared)

    def test_plugin_names_remain_drop_in_compatible(self) -> None:
        for relative in (
            "plugin.json",
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            ".agents/plugins/marketplace.json",
        ):
            data = json.loads(self.read(relative))
            self.assertEqual("sepia", data["name"], relative)

    def test_agent_surfaces_expose_trilingual_voice_contract(self) -> None:
        openai = self.read("skills/sepia/agents/openai.yaml")
        workflow = self.read(".agents/workflows/sepia.md")
        self.assertIn('display_name: "Sepia Trilingual"', openai)
        self.assertIn("Japanese, English, and Spanish", openai)
        self.assertIn("language, locale, and Human Voice Profile", workflow)
        self.assertIn("Never translate", workflow)
        self.assertIn("detector evasion", workflow)

    def test_ci_runs_upstream_and_multilingual_tests(self) -> None:
        workflow = self.read(".github/workflows/multilingual-contract.yml")
        self.assertIn("unittest discover", workflow)
        self.assertIn("test_*.py", workflow)
        self.assertIn("scripts/check_versions.py", workflow)
        self.assertIn("git show --check", workflow)

    def test_acceptance_fixture_schema_and_coverage(self) -> None:
        raw = self.read("evals/multilingual-voice/cases.json")
        cases = json.loads(raw)
        self.assertGreaterEqual(len(cases), 10)

        ids: set[str] = set()
        languages: set[str] = set()
        operations: set[str] = set()
        required_keys = {
            "id",
            "language",
            "operation",
            "input",
            "must_preserve",
            "expected_findings",
            "forbidden_changes",
        }

        for case in cases:
            self.assertEqual(required_keys, set(case), case.get("id"))
            self.assertNotIn(case["id"], ids)
            ids.add(case["id"])
            languages.add(case["language"])
            operations.add(case["operation"])
            self.assertTrue(case["input"].strip())
            self.assertIsInstance(case["must_preserve"], list)
            self.assertIsInstance(case["expected_findings"], list)
            self.assertIsInstance(case["forbidden_changes"], list)

        self.assertTrue(any(value.startswith("ja") for value in languages))
        self.assertTrue(any(value.startswith("en") for value in languages))
        self.assertTrue(any(value.startswith("es") for value in languages))
        self.assertTrue(any(value.startswith("mixed") for value in languages))
        self.assertEqual({"write", "review", "refactor", "recreate"}, operations)

    def test_documentation_and_attribution_exist(self) -> None:
        ja = self.read("README.ja.md")
        es = self.read("README.es.md")
        attribution = self.read("ATTRIBUTION.md")
        self.assertIn("書き手を", ja)
        self.assertIn("voice-profile.example.yaml", ja)
        self.assertIn("No conviertas al autor", es)
        self.assertIn("voice-profile.example.yaml", es)
        self.assertIn("Nanako Tsai", attribution)
        self.assertIn("0326635aa2cee589e6f525af1ec6089d51944f3c", attribution)
        self.assertIn("MIT", attribution)


if __name__ == "__main__":
    unittest.main()
