# Markdown-in-SVG 0.1 — 日中英の三言語仕様

**既定言語および正文：英語。** [English](MISVG-0.1.en.html) · [繁體中文](MISVG-0.1.zh-Hant.html) · [日本語](MISVG-0.1.ja.html)

MISVG-SPEC-0001 改訂 0.1.1 / Draft 02 は英語、繁体字中国語、日本語の全文を提供する。`index.html` は英語の既定閲覧版であり、各版に言語切替がある。`MISVG-0.1.md` は既定の英語 Markdown のコピーである。言語別 Markdown を編集してから出版物を再生成する。

IEEE 形式の技術構造と RFC の要求用語を用いた独立草案であり、IEEE／IETF の承認は受けていない。翻訳の不一致は英語を基準に解決する。ワイヤ形式は `0.1` のままで、言語選択によって形式や要件は変わらない。

## 内容

- 全文仕様：主要 15 箇条、6 附属書、30 項目の適合性試験要件。
- 三言語のオフライン HTML と編集可能な Markdown。
- metadata XML Schema、ダイジェスト試験ベクトル、一部の提供物検査。
- `examples/` の各言語 SVG 例と抽出比較用原文。
- 既定例：`examples/order-flow.en.misvg.svg`。言語接尾辞のない例は従来の繁体字中国語互換試料として保持する。

## 生成と検査

Python 3、`markdown`、`lxml` が必要。ネットワークは不要。このディレクトリで実行する。

```sh
python3 scripts/build_publication.py
python3 tests/check_package.py
python3 tests/check_localization.py
```

最初のコマンドは HTML、英語の既定入口、各言語の例を再生成する。後のコマンドは `tests/verification-report.json` と `tests/localization-report.json` を生成する。構造検査だけでは意味の完全一致を証明しない。三版は同じ箇条番号、要求水準、技術トークン、試験識別子を保持し、対照レビューを可能にする。

提供物検査器は完全な MISVG 検証器、Markdown 組版エンジン、編集器ではない。完全な SVG 属性文法、すべての CommonMark 出力、原子的編集、描画器間相互運用性は対象外である。従来の 36 件の検査は成功した。言語検査と三言語配置検査は別途報告する。従来および多言語の描画記録は `tests/` にある。

## 設計と公開状態

Markdown が内容の唯一の正本であり、SVG は表示である。ダイジェスト一致はビュー、著者、署名を検証しない。例のビューは原文から手動配置したもの。付属 `.md` は抽出比較用で、第二の正本ではない。

本版は `static` のみを定義し、HTML `foreignObject` 配置、画像資源、GFM／Mermaid 実行、署名は定義しない。example.org 名前空間は草案試験用であり、正式公開前に管理と移行を決める必要がある。公開ライセンスは未選択であり、外部公開前に権利者が決定する。
