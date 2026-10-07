"""Offline package contract, based on Agent Plugins 1.0.0 and OpenAI metadata.

Uses stdlib assertions for this manifest's schema fields; no network or new
validator dependency. This is static validation, not a ChatGPT installation test.
"""

import hashlib
import json
import re
import struct
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_plugin


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.interface = self.manifest["extensions"]["com.openai"]["interface"]

    def test_portable_schema_and_openai_namespace(self):
        # https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
        self.assertEqual(set(self.manifest), {
            "$schema", "name", "version", "description", "author", "license",
            "repository", "homepage", "extensions",
        })
        self.assertEqual(self.manifest["$schema"],
                         "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        for key in ("name", "version", "description", "license", "repository", "homepage"):
            self.assertIsInstance(self.manifest[key], str)
            self.assertTrue(self.manifest[key].strip(), key)
        self.assertRegex(self.manifest["name"], r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
        self.assertLessEqual(len(self.manifest["name"]), 64)
        self.assertRegex(self.manifest["version"], r"\A\d+\.\d+\.\d+\Z")
        self.assertLessEqual(len(self.manifest["description"]), 4000)
        self.assertEqual(set(self.manifest["author"]), {"name"})
        self.assertIsInstance(self.manifest["author"]["name"], str)
        self.assertTrue(0 < len(self.manifest["author"]["name"]) <= 120)
        self.assertEqual(set(self.manifest["extensions"]), {"com.openai"})
        self.assertEqual(set(self.manifest["extensions"]["com.openai"]), {"interface"})
        self.assertEqual(self.manifest["license"], "MIT")

    def test_codex_compatibility_and_marketplace_paths(self):
        expected = {key: value for key, value in self.manifest.items()
                    if key not in {"$schema", "extensions"}}
        expected.update(skills="./skills/", interface=self.interface)
        self.assertEqual(self.codex, expected)
        for relative, source in (
            (".agents/plugins/marketplace.json", {"source": "local", "path": "./"}),
            (".claude-plugin/marketplace.json", "./"),
        ):
            catalog = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual(len(catalog["plugins"]), 1)
            self.assertEqual(catalog["plugins"][0]["name"], self.manifest["name"])
            self.assertEqual(catalog["plugins"][0]["source"], source)

    def test_listing_limits_and_icons(self):
        self.assertEqual(set(self.interface), {
            "displayName", "shortDescription", "longDescription", "developerName",
            "category", "capabilities", "websiteURL", "defaultPrompt", "composerIcon", "logo",
        })
        for key, limit in (("displayName", 30), ("shortDescription", 30),
                           ("longDescription", 4000), ("developerName", 80)):
            value = self.interface[key]
            self.assertIsInstance(value, str)
            self.assertTrue(0 < len(value) <= limit, key)
        self.assertEqual(self.interface["category"], "Productivity")
        self.assertEqual(self.interface["capabilities"], [])
        repo = "https://github.com/OPP-studio-macchino/sepia-trilingual"
        self.assertEqual(self.interface["websiteURL"], repo)
        self.assertEqual(self.manifest["homepage"], repo)
        self.assertEqual(self.manifest["repository"], repo)
        prompts = self.interface["defaultPrompt"]
        self.assertIsInstance(prompts, list)
        self.assertTrue(1 <= len(prompts) <= 3)
        self.assertEqual(len(set(prompts)), len(prompts))
        for prompt in prompts:
            self.assertIsInstance(prompt, str)
            self.assertTrue(0 < len(prompt) <= 128)
            self.assertNotIn("@", prompt)
        for key, size in (("composerIcon", 128), ("logo", 512)):
            self.assertEqual(self.interface[key], f"./assets/sepia-user-icon-{size}.png")
            self.assertTrue((ROOT / self.interface[key]).is_file())

    def test_supplied_png_assets_are_preserved(self):
        hashes = {
            128: "38ce59d62b00f3fd25f643705fb899667612288f11b1d08cf06c5de82cc68e83",
            256: "9cae104bbb2717a6b02e1da35ba278dd0e3b59b2eae917eef20cf20b80b9880c",
            512: "e700be7721068ce14eab2e7cf78119c20f951a1c57cd78a90e947b4e69e86668",
        }
        for size, digest in hashes.items():
            with self.subTest(size=size):
                data = (ROOT / f"assets/sepia-user-icon-{size}.png").read_bytes()
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(data[12:16], b"IHDR")
                self.assertEqual(struct.unpack(">II", data[16:24]), (size, size))
                self.assertLessEqual(len(data), 5 * 1024 * 1024)
                self.assertEqual(hashlib.sha256(data).hexdigest(), digest)

    def test_skills_only_no_mcp_or_app_wiring(self):
        for name in ("mcp.json", ".mcp.json", ".app.json"):
            self.assertFalse((ROOT / name).exists(), name)
        for relative in ("plugin.json", ".codex-plugin/plugin.json",
                         ".claude-plugin/plugin.json", ".agents/plugins/marketplace.json",
                         ".claude-plugin/marketplace.json"):
            data = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.assertNotRegex(json.dumps(data), r'"(?:mcpServers|apps|hooks)"\s*:')

    def test_all_four_operations_share_the_canonical_skill(self):
        operations = {"write", "review", "refactor", "recreate"}
        self.assertEqual({path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")},
                         {"sepia"} | {f"sepia-{op}" for op in operations})
        for operation in operations:
            path = ROOT / f"skills/sepia-{operation}/SKILL.md"
            content = path.read_text(encoding="utf-8")
            self.assertIn(f"name: sepia-{operation}\n", content)
            self.assertIn("`../sepia/SKILL.md`", content)
            self.assertIn(f"bind exactly the `{operation}` operation", content)
            self.assertEqual((path.parent / "../sepia/SKILL.md").resolve(),
                             ROOT / "skills/sepia/SKILL.md")

    def test_zip_is_reproducible_complete_and_skills_only(self):
        with tempfile.TemporaryDirectory() as folder:
            first = build_plugin.build(Path(folder) / "one")
            second = build_plugin.build(Path(folder) / "two")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                names = set(archive.namelist())
                expected = {
                    "plugin.json", ".codex-plugin/plugin.json", "LICENSE", "ATTRIBUTION.md",
                    "CHATGPT.md", "examples/voice-profile.example.yaml",
                    "assets/sepia-user-icon-128.png", "assets/sepia-user-icon-256.png",
                    "assets/sepia-user-icon-512.png",
                } | {
                    path.relative_to(ROOT).as_posix() for path in (ROOT / "skills").rglob("*")
                    if path.is_file() and path.suffix in {".md", ".yaml"}
                    and not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
                }
                self.assertEqual(names, expected)
                self.assertIn("plugin.json", names)
                self.assertIn("LICENSE", names)
                self.assertIn("ATTRIBUTION.md", names)
                for entry in archive.infolist():
                    self.assertNotIn("..", Path(entry.filename).parts)
                    self.assertFalse(Path(entry.filename).is_absolute())
                    self.assertNotRegex(entry.filename, r"(?:mcp|sepia-icon-|\.env|__pycache__|\.DS_Store|\._)")
                    self.assertEqual(entry.external_attr >> 16, 0o100644)
                    self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(archive.read(entry), (ROOT / entry.filename).read_bytes())
                    if entry.filename.startswith("skills/") and entry.filename.endswith(".md"):
                        text = archive.read(entry).decode("utf-8")
                        for reference in re.findall(r"\breferences/[\w./-]+\.md", text):
                            self.assertIn(f"skills/sepia/{reference}", names)


if __name__ == "__main__":
    unittest.main()
