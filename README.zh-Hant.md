# Markdown-in-SVG 0.1 — 中日英三語規範

**預設與規範正文：英文。** [English](MISVG-0.1.en.md) · [繁體中文](MISVG-0.1.zh-Hant.md) · [日本語](MISVG-0.1.ja.md)

MISVG-SPEC-0001 修訂 0.1.1 / Draft 02 提供完整英文、繁體中文、日文。開啟 `index.html` 即為預設英文閱讀版，各版均提供語言切換。`MISVG-0.1.md` 是預設英文 Markdown 副本。請修改各語言的 Markdown 檔，再重新產生出版內容。

本文件為採 IEEE 式結構與 RFC 要求詞的獨立草案，未經 IEEE／IETF 核准。譯文歧義以英文為準。交換格式版本維持 `0.1`，語言選擇不影響格式與要求。

## 內容

- 完整規範：15 章、6 附錄、30 項符合性測試要求。
- 三語離線 HTML 與可編輯 Markdown。
- metadata XML Schema、摘要向量與部分交付檢查。
- `examples/` 內的三語 SVG 範例及相應抽取對照原文。
- 預設範例：`examples/order-flow.en.misvg.svg`。無語言尾碼的範例保留為原有繁體中文相容試料。

## 產生與檢查

需要 Python 3、`markdown`、`lxml`。不需網路。在本資料夾執行：

```sh
python3 scripts/build_publication.py
python3 tests/check_package.py
python3 tests/check_localization.py
```

第一個命令重新產生 HTML、預設英文入口與三語範例。其餘命令產生 `tests/verification-report.json` 與 `tests/localization-report.json`。譯本結構檢查不能證明語意完全等價；三版沿用相同章節、要求水準、技術詞彙與測試識別碼，便於審查。

交付檢查工具不是完整 MISVG 驗證器、Markdown 排版引擎或編輯器，未涵蓋完整 SVG 屬性文法、所有 CommonMark 輸出、原子編輯或跨呈現器互通性。原有 36 項檢查通過；語言與三語排版檢查另有報告。原有及多語渲染紀錄位於 `tests/`。

## 設計與發布狀態

Markdown 是文件內容的唯一權威來源，SVG 是呈現。摘要相符不能驗證畫面、作者或簽章。範例畫面依原文人工編排；附帶 `.md` 是抽取對照，不是第二份權威來源。

本版只定義 `static`，不含 HTML `foreignObject` 排版、圖片資源、GFM／Mermaid 執行、簽章。example.org 命名空間是草案測試識別符，正式發布前需決定治理與遷移。本包未選定公開授權；對外發布前由權利人決定。
