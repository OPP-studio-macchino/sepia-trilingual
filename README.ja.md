# Sepia Trilingual

[English](README.md) | **日本語** | [Español](README.es.md)

Sepia Trilingualは、Sepiaを日本語・英語・スペイン語向けに拡張した文章編集Skillです。

本プロジェクトは[Nanako Tsai氏のSepia](https://github.com/Nanako0129/sepia)から派生した独立プロジェクトであり、upstream作者の公式版ではありません。upstream作者によるendorse、maintain、approveを示すものでもありません。

目的は「AI文章を人間の文章に偽装すること」ではありません。事実、意味、話し手の癖、敬意レベル、地域差を保ったまま、過剰説明や均一すぎる構造を減らします。

> 書き手を「上手な人」に作り変えない。本人のまま、伝わりやすくする。

## 対応言語

- 日本語：`ja-JP`
- English：原文の`en-US`、`en-GB`などを維持
- Español：`tú / usted / vos`、`vosotros / ustedes`、地域語彙を維持

明示されていない翻訳や地域表現の統一は行いません。

## 4つの操作

| 操作 | 内容 |
|---|---|
| `write` | 新しい文章を書く |
| `review` | 修正せず問題点だけ診断する |
| `refactor` | 元の構造と声を保ち、最小限修正する |
| `recreate` | 事実・意図・声を抽出して書き直す |

Codexでは`$sepia-write`、`$sepia-review`、`$sepia-refactor`、`$sepia-recreate`を使用します。

## 人間らしさの扱い

「人間らしさ」の数値は出しません。代わりに、次を確認します。

- 意味と事実が保たれたか
- 書き手の声が保たれたか
- 読み手との距離や敬語が変わっていないか
- 英語・スペイン語の地域差が保たれたか
- 整えすぎて別人の文章になっていないか

誤字、偽の体験談、偽の感情、不要な俗語を追加することは禁止しています。

## 自分で「人間らしさ」を設定する

AIに丸投げせず、明示的なVoice Profileを渡せます。`examples/voice-profile.example.yaml`をコピーし、分かる項目だけ設定します。

```yaml
relationship:
  self_reference: "俺"
  formality: "casual"
voice:
  directness: "direct"
lexicon:
  avoid: ["企業広告のような言い回し"]
```

このファイルは自動探索しません。使用するときだけ対象ファイルを明示してください。現在の依頼、事実、引用、コード、安全上の制約を上書きすることもできません。完全な仕様は`skills/sepia/references/voice-profile-config.md`にあります。

## MCP連携（任意）

[読み取り専用MCPの導入手順](sepia_mcp/README.md)を用意しました。既存のSepiaのルールを接続先AIへ渡します。MCP側は文章を受け取らず、編集も行いません。ChatGPT WebではHTTPS接続や安全なトンネルが必要です。

## インストール

リポジトリ公開後のCodex向けコマンド：

```bash
codex plugin marketplace add OPP-studio-macchino/sepia-trilingual
codex plugin add sepia@sepia
```

Skills CLI：

```bash
npx skills add OPP-studio-macchino/sepia-trilingual -g
```

## 検証

```bash
python3 scripts/check_versions.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## 原著作とライセンス

本プロジェクトはNanako Tsai氏のSepiaをMIT Licenseの下で改変したものです。詳細は[ATTRIBUTION.md](ATTRIBUTION.md)と`LICENSE`を参照してください。
