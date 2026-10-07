"""Expose the existing Sepia rule files without processing or collecting prose.

The model in the MCP client performs review/refactor/recreate/write. This
server does not call an LLM or accept the user's draft as a tool argument.
"""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from typing import Literal

from mcp.server import MCPServer
from mcp.types import Icon, ToolAnnotations

ROOT = Path(__file__).resolve().parents[1]
SKILL = "skills/sepia/"

Operation = Literal["write", "review", "refactor", "recreate"]
Language = Literal["ja-JP", "en", "es"]
DocumentType = Literal[
    "fiction", "release-notes", "dev-replies", "postmortems",
    "tickets", "tech-articles", "other",
]

COMMON = (
    "SKILL.md",
    "references/language-routing.md",
    "references/human-voice.md",
    "references/languages/shared.md",
)
LANGUAGES = {
    "ja-JP": "references/languages/ja-JP.md",
    "en": "references/languages/en.md",
    "es": "references/languages/es.md",
}
DOMAIN = {
    "fiction": (
        "references/narrative-pass.md", "references/discourse-pass.md",
        "references/style-pass.md", "references/rubric.md",
    ),
    "release-notes": (
        "references/professional-pass.md",
        "references/domains/release-notes.md", "references/style-pass.md",
    ),
    "dev-replies": (
        "references/professional-pass.md",
        "references/domains/dev-replies.md", "references/style-pass.md",
    ),
    "postmortems": (
        "references/professional-pass.md",
        "references/domains/postmortems.md", "references/style-pass.md",
    ),
    "tickets": (
        "references/professional-pass.md",
        "references/domains/tickets.md", "references/style-pass.md",
    ),
    "tech-articles": (
        "references/professional-pass.md",
        "references/domains/tech-articles.md",
        "references/discourse-pass.md", "references/style-pass.md",
    ),
    "other": ("references/professional-pass.md", "references/style-pass.md"),
}


def _read_reference(relative_path: str) -> str:
    """Read only fixed, repository-owned Sepia sources, never user-supplied paths."""
    return (ROOT / SKILL / relative_path).read_text(encoding="utf-8")


def editing_rules(operation: Operation, language: Language, document_type: DocumentType) -> str:
    """Return canonical, composable guidance; this is not edited prose."""
    if operation not in ("write", "review", "refactor", "recreate"):
        raise ValueError("Unsupported operation")
    if language not in LANGUAGES or document_type not in DOMAIN:
        raise ValueError("Unsupported language or document type")

    names = (*COMMON, LANGUAGES[language], *DOMAIN[document_type])
    header = (
        "SEPIA TRILINGUAL EDITORIAL RULEBOOK (READ-ONLY)\n"
        f"Operation: {operation}; Language: {language}; Document type: {document_type}.\n"
        "Apply these rules inside the connected AI; this server does NOT edit prose.\n"
        "Do not send draft text, private documents, or credentials to this server.\n"
        "Follow the selected operation contract, preserve evidence and author voice,\n"
        "and distinguish facts, inference, and uncertainty.\n"
    )
    sections = [header]
    for name in names:
        sections.append(f"\n--- BEGIN {SKILL}{name} ---\n")
        sections.append(_read_reference(name))
        sections.append(f"\n--- END {SKILL}{name} ---\n")
    return "".join(sections)


def create_server() -> MCPServer:
    icon_path = ROOT / "assets/sepia-icon-256.png"
    icon_src = "data:image/png;base64," + base64.b64encode(icon_path.read_bytes()).decode("ascii")
    mcp = MCPServer(
        name="sepia-trilingual",
        title="Sepia Trilingual",
        version=json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))["version"],
        description="Read-only editorial rules for Japanese, English, and Spanish.",
        instructions=(
            "Call sepia_get_rules for the requested operation and language. "
            "Then perform writing/editing with the AI already in the MCP client. "
            "This server does not accept drafts, rewrite text, or invoke an LLM."
        ),
        icons=[Icon(src=icon_src, mimeType="image/png", sizes=["256x256"])],
    )

    @mcp.tool(
        name="sepia_get_rules",
        title="Get Sepia editorial rules",
        description=(
            "Read-only: retrieve the canonical Sepia Trilingual writing/editing rules. "
            "No source text is accepted. Use the result to write, review, minimally "
            "refactor, or recreate text in the current chat. Does not itself edit."
        ),
        annotations=ToolAnnotations(
            readOnlyHint=True, destructiveHint=False,
            idempotentHint=True, openWorldHint=False,
        ),
    )
    def sepia_get_rules(
        operation: Operation,
        language: Language = "ja-JP",
        document_type: DocumentType = "other",
    ) -> str:
        return editing_rules(operation, language, document_type)

    @mcp.resource("sepia://canonical", mime_type="text/markdown")
    def canonical_skill() -> str:
        return _read_reference("SKILL.md")

    @mcp.resource("sepia://model-fingerprints", mime_type="text/markdown")
    def model_fingerprints() -> str:
        return _read_reference("references/model-fingerprints.md")

    @mcp.resource("sepia://voice-profile", mime_type="text/markdown")
    def voice_profile_schema() -> str:
        return _read_reference("references/voice-profile-config.md")

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Sepia Trilingual read-only MCP server")
    parser.add_argument("--transport", choices=("stdio", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3801)
    args = parser.parse_args()
    if args.transport == "streamable-http":
        if args.host not in ("127.0.0.1", "localhost", "::1"):
            parser.error("Only loopback binding is supported. Use an authenticated TLS proxy for remote access.")
        create_server().run(transport="streamable-http", host=args.host, port=args.port, json_response=True)
    else:
        create_server().run(transport="stdio")


if __name__ == "__main__":
    main()
