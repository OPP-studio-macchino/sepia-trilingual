# Sepia Trilingual in ChatGPT Web

Version 0.6.1 is a **skills-only package**: the Sepia router and four operations
(`write`, `review`, `refactor`, `recreate`) with Japanese, English, Spanish, and
Human Voice guidance. It needs no Sepia account, API key, server, or MCP connection.
It preserves the upstream MIT license and attribution. It does not certify human
authorship or promise AI-detector evasion.

**Status: prepared for ChatGPT Web; live installation and execution have not been
tested.** Local checks cannot establish account eligibility or a successful import.

## Package

The portable entry point is root `plugin.json`; OpenAI presentation is under
`extensions.com.openai.interface`. The Codex compatibility manifest retains
`skills: "./skills/"` and matching presentation. The user-supplied brushstroke S
is used for the composer icon (128 px) and logo (512 px); the 256 px asset is also
included. See the official [packaging guide](https://developers.openai.com/plugins/build/plugins).

From this Git checkout, with Python 3:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/check_versions.py
python3 scripts/build_plugin.py
```

Output: `dist/sepia-trilingual-0.6.1-skills-only.zip`. The builder includes explicit
package files and Git-tracked skill resources (including their working-tree edits).
New skill resources must be tracked before building. Fixed ZIP timestamps, file
modes, ordering, and uncompressed entries make identical inputs reproducible.
The ZIP contains the manifests at the archive root, all five skill folders,
the three supplied icons, this guide, the voice-profile example, `LICENSE`, and
`ATTRIBUTION.md`. It excludes repository history, development code, local secrets,
temporary files, and the separate `sepia_mcp` bridge.

Neither manifest wires MCP. Do not add `mcpServers`, `mcp.json`, `.mcp.json`, or
`.app.json` to this package: imported MCP declarations can cause a **Desktop only**
label, even with a remote HTTPS endpoint. The optional bridge remains in the source
repository for separate MCP clients.

## Personal Pro account

A Pro subscription alone does not establish access to private plugin ZIP upload
or workspace administration. Open ChatGPT's Plugins area and inspect the controls
actually available to your account. If it offers a local package/ZIP installation
flow, use the ZIP above and inspect its import findings. Do not use **Add custom
MCP server** for this package.

If no package-install control is present, personal Web installation is blocked by
the available account UI. The official local-install guidance does not guarantee
that control for every personal Pro account. Codex local installation can test the
package separately, but cannot establish ChatGPT Web compatibility. See the
[complete-plugin testing guide](https://developers.openai.com/plugins/deploy/connect-chatgpt).

## Workspace administrator

Once this revision is available on GitHub through your normal reviewed workflow:

1. In the Admin Console, select the workspace, then **Plugins → Add → Import marketplace**.
2. Set Source to `https://github.com/OPP-studio-macchino/sepia-trilingual`.
   Leave Path empty: `.agents/plugins/marketplace.json` is in the repository root's
   supported catalog location. Set Branch, tag, or commit to the reviewed revision.
3. Authorize GitHub read access, inspect import results, and configure installation
   policy for the intended members. Check that Sepia is not marked Desktop only.

This requires workspace-admin access and GitHub access to that revision. Local
uncommitted changes cannot be imported from GitHub. The default branch may still
contain the older package. Updates can be requested with **Sync now**; branch-based
imports can also receive automatic updates. See the official
[GitHub marketplace import guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).

## Verify the installed plugin

Enable Sepia in a new Web conversation. Record the account/workspace, imported
version, prompts, and actual results before reporting a live PASS.

| Check | Expected behavior |
| --- | --- |
| Sepia write: provide facts for a Japanese announcement | Japanese prose with the requested register and no invented details |
| Sepia review: provide an English draft | Evidence-backed diagnosis without edited prose |
| Sepia refactor: provide Spanish text using `vos` | Minimal edits preserving voseo, facts, and voice |
| Sepia recreate: provide a draft and its constraints | Full rewrite retaining source facts, intent, and voice anchors |
| Follow up in a different conversation language | No unsolicited translation or locale normalization |
| Ask for detector evasion or proof of human authorship | No evasion promise or authorship certification |
| Ask an unrelated arithmetic question | No unnecessary Sepia workflow |

Confirm the supplied icon appears and all sibling skills and references resolve.
Use `evals/multilingual-voice/cases.json` in the source checkout for more cases.
Missing install controls, rejected metadata, Desktop only labeling, unresolved
resources, or incorrect operation behavior remain blockers; report the actual
finding rather than treating local tests as a live pass.

Public Directory distribution is separate: it requires the developer identity and
review process described in [Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission).
This change does not submit to OpenAI or publish a GitHub release. Optional support,
privacy, and terms URLs are omitted; no placeholder policy URLs are supplied.
