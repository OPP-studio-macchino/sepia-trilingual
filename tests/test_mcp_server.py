"""MCP integration tests; optional SDK is installed by the MCP CI step."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HAS_MCP = importlib.util.find_spec("mcp") is not None
if HAS_MCP:
    from mcp import Client, StdioServerParameters
    from sepia_mcp.server import ROOT, create_server, editing_rules


@unittest.skipUnless(HAS_MCP, "Optional mcp SDK not installed")
class SepiaMCPRulesTests(unittest.TestCase):
    def test_language_routes(self) -> None:
        for language, expected in (
            ("ja-JP", "references/languages/ja-JP.md"),
            ("en", "references/languages/en.md"),
            ("es", "references/languages/es.md"),
        ):
            with self.subTest(language=language):
                rules = editing_rules("review", language, "other")
                self.assertIn(f"BEGIN skills/sepia/{expected}", rules)
                for alternative in ("ja-JP", "en", "es"):
                    if alternative != language:
                        self.assertNotIn(
                            f"BEGIN skills/sepia/references/languages/{alternative}.md", rules
                        )

    def test_domain_routing(self) -> None:
        release = editing_rules("write", "ja-JP", "release-notes")
        self.assertIn("references/domains/release-notes.md", release)
        self.assertNotIn("BEGIN skills/sepia/references/domains/postmortems.md", release)
        self.assertIn("references/professional-pass.md", release)

    def test_invalid_routes_rejected(self) -> None:
        for op, language, domain in (
            ("translate", "ja-JP", "other"),
            ("review", "../../secret", "other"),
            ("review", "ja-JP", "../../secret"),
        ):
            with self.subTest(operation=op, language=language, domain=domain):
                with self.assertRaises(ValueError):
                    editing_rules(op, language, domain)

    def test_has_no_external_model_configuration(self) -> None:
        self.assertFalse((ROOT / "sepia_mcp/.env").exists())
        self.assertIn("server does not", editing_rules("refactor", "es", "other").lower())


@unittest.skipUnless(HAS_MCP, "Optional mcp SDK not installed")
class SepiaMCPProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_is_read_only_and_does_not_accept_draft(self) -> None:
        async with Client(create_server()) as client:
            self.assertEqual(client.protocol_version, "2026-07-28")
            tools = (await client.list_tools()).tools
            self.assertEqual([tool.name for tool in tools], ["sepia_get_rules"])
            tool = tools[0]
            self.assertTrue(tool.annotations.read_only_hint)
            self.assertEqual(set(tool.input_schema["properties"]), {
                "operation", "language", "document_type",
            })
            self.assertEqual(tool.input_schema["required"], ["operation"])
            result = await client.call_tool("sepia_get_rules", {
                "operation": "review", "language": "ja-JP", "document_type": "other",
            })
            self.assertFalse(result.is_error)
            self.assertIn("Operation: review; Language: ja-JP", result.content[0].text)
            self.assertIn("Human Voice", result.content[0].text)
            self.assertNotIn("BEGIN skills/sepia/references/languages/es.md", result.content[0].text)

    async def test_model_is_not_invoked_and_resources_are_readable(self) -> None:
        async with Client(create_server()) as client:
            canonical = await client.read_resource("sepia://canonical")
            self.assertIn("Security boundary", canonical.contents[0].text)
            profiles = await client.read_resource("sepia://voice-profile")
            self.assertIn("profile", profiles.contents[0].text.lower())
            fingerprints = await client.read_resource("sepia://model-fingerprints")
            self.assertGreater(len(fingerprints.contents[0].text), 100)
            icon = client.server_info.icons[0]
            self.assertTrue(icon.src.startswith("data:image/png;base64,"))
            self.assertEqual(icon.sizes, ["256x256"])
            manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(client.server_info.version, manifest["version"])

    async def test_stdio_subprocess(self) -> None:
        # The test runner is launched from the repository root by CI.
        async with Client(StdioServerParameters(
            command=sys.executable, args=["-m", "sepia_mcp"],
        )) as client:
            result = await client.call_tool("sepia_get_rules", {
                "operation": "refactor", "language": "en", "document_type": "tech-articles",
            })
            self.assertFalse(result.is_error)
            self.assertIn("references/domains/tech-articles.md", result.content[0].text)
