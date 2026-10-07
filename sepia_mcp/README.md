# Sepia Trilingual MCP bridge (read-only)

[English](#english) | [日本語](#日本語)

## English

This optional MCP server serves **the existing Sepia rulebook** to an MCP client.
It makes no AI/API calls, never receives the user's source prose, and does not
rewrite text by itself. ChatGPT, Codex, or another connected AI uses the returned
rules to perform **write**, **review**, **refactor**, or **recreate** in the chat.
It is not an AI-detector bypass tool.

### Setup (local stdio clients)

From the repository root, with Python 3.10+ installed:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r sepia_mcp/requirements.txt
.venv/bin/python -m sepia_mcp
```

The last command runs a stdio MCP server; connect it using your MCP client's
stdio configuration. For clients launched from other working directories, use
an absolute path to `sepia_mcp/server.py` with the same virtualenv interpreter.

### HTTP (local testing only)

```bash
.venv/bin/python -m sepia_mcp --transport streamable-http --port 3801
# endpoint: http://127.0.0.1:3801/mcp
```

The server deliberately binds only to loopback. **ChatGPT Web cannot connect
straight to this localhost URL.** Deploy behind an authenticated HTTPS gateway,
or use a supported secure MCP tunnel, before connecting the remote endpoint.
Do not expose the unauthenticated development endpoint to the public internet.

### MCP interface

- Tool: `sepia_get_rules(operation, language, document_type)` — read-only.
- Resources: `sepia://canonical`, `sepia://model-fingerprints`,
  `sepia://voice-profile`.
- Languages: `ja-JP`, `en`, `es`.
- Document types: fiction, release-notes, dev-replies, postmortems, tickets,
  tech-articles, other.

**No text/draft parameter is accepted.** The tool reads the canonical
`skills/sepia/` documents from the checkout at call time. No duplicated rules,
file writes, network access, provider keys, or external model billing.

ChatGPT Web Pro currently supports developer-mode custom MCPs for read/fetch;
full write/modify MCP is plan-gated. Importing the server does **not**
automatically apply Sepia to every answer: invoke or select the MCP tool in
eligible chats, or configure project instructions to use it for prose editing.

Icon: [SVG](../assets/sepia-icon.svg) and [PNG](../assets/sepia-icon-256.png).
The server advertises the PNG in its MCP icon metadata. Some clients may require
uploading a logo separately in their app settings.

## 日本語

これは既存のSepia Trilingualの編集ルールをMCPで取得するための
**読み取り専用サーバー**です。文章そのものをサーバーへ送らず、
接続先のChatGPTやCodexが文章を監査・編集します。

まずリポジトリのルートで仮想環境を作り、上記のコマンドで起動してください。
ChatGPT WebはローカルURLへ直接接続できないため、接続時は認証付きHTTPS
または対応する安全なトンネルが必要です。

Proでは読み取り・取得用途のカスタムMCPを利用できますが、
**すべての会話に自動適用されるわけではありません**。
Project Instructionsに適用対象を指定すると使い分けやすくなります。

ユーザーの下書き・個人情報・APIキーをMCPへ送信しない設計です。
編集後の文章はMCPサーバーではなく、接続先のAIが返します。
