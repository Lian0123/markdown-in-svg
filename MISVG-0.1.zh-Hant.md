# Markdown-in-SVG（MISVG）文件交換規範

**Specification for Markdown-in-SVG Document Interchange**

| 文件控制 | 值 |
|---|---|
| 文件識別碼 | MISVG-SPEC-0001 |
| 草案版次 | 0.1.1 / Draft 02 |
| 線上格式版本（wire version） | `0.1` |
| 日期 | 2026-11-02 |
| 狀態 | 個人／專案技術規範草案，供實作與審查 |
| 規範語言 | 英文（en）為預設與規範正文；繁體中文（zh-Hant）、日文（ja）為完整譯本 |
| 編輯者／維護組織 | 待指定；本版由 AI 協助草擬 |
| 核准狀態 | 尚未經 IEEE、IETF、W3C 或其他標準組織核准 |

## 文件地位（Status of This Memo）

本文件提出一個新的 Markdown-in-SVG 交換格式，並非既有標準的轉載。文件編排參考 IEEE 技術標準的概述、規範性引用、定義、要求與附錄結構，要求程度採用 RFC 2119 與 RFC 8174。另設安全性、IANA 與互通性條款。

這是一份混合編排的獨立草案，**不宣稱通過 IEEE 編輯審查，也不是 RFC、已提交的 Internet-Draft 或 IEEE P 系列草案**。`MISVG-SPEC-0001` 是本專案識別碼，不是任何組織授予的編號。正式投稿時需另依所選組織的程序、範本、語言、權利聲明與編輯要求轉換。本文未替使用者選定公開授權條款；對外發布前由權利人決定。

英文是預設閱讀語言，也是處理譯文歧義的規範正文。繁體中文與日文為完整對照譯本，沿用相同章節與測試識別碼。語言選擇不改變交換格式、識別碼或要求。0.1.1 版新增三語出版與語言政策，不變更交換格式版本 0.1。

摘要、文件地位與目錄為資訊性內容。第 1–15 章及附錄 A、B 為規範性內容；附錄 C–F 為資訊性內容。機器可讀附件與正文若有差異，以正文及規範性附錄為準。

## 摘要（Abstract）

MISVG 將可編輯的 Markdown 原文、來源與視圖的對應關係，以及靜態 SVG 視圖封裝於同一個 UTF-8 XML 文件。Markdown 是內容的唯一權威來源；SVG 是由該來源產生的視覺表示。一般 SVG 檢視器可顯示圖文，了解 MISVG 的工具則可抽取、驗證、編輯並重新產生文件。本規範定義容器、字元處理、來源摘要、版本控制、靜態呈現子集、對應資訊、錯誤處理及符合性要求。摘要相符只能支持來源綁定檢查，不能證明畫面語意正確或文件可信。

## 目錄

1. 概述（Overview）
2. 規範性引用文件（Normative References）
3. 用語、定義與要求程度
4. 架構與權威來源
5. XML 容器與欄位
6. Markdown 與字元處理
7. 靜態呈現設定檔
8. 摘要、同步與編輯交易
9. 來源對應
10. 擴充、版本與保留規則
11. 符合性與互通性
12. 錯誤處理
13. 安全性與隱私考量
14. IANA 與識別碼考量
15. 版本治理與變更管理

附錄 A：詞彙與結構限制（規範性）  
附錄 B：符合性測試要求（規範性）  
附錄 C：完整範例與操作流程（資訊性）  
附錄 D：設計理由與取捨（資訊性）  
附錄 E：編排依據與參考資料（資訊性）  
附錄 F：交付附件與實作界限（資訊性）

## 1. 概述（Overview）

### 1.1 範圍（Scope）

本規範定義單一 `.svg` 檔案中的 Markdown 原文儲存、原文至 SVG 視圖的綁定、基本編輯流程，以及檔案與工具的符合性。適用於說明卡片、流程圖、架構圖、短篇規格與可視化知識文件。

本版只定義 `static` 呈現設定檔。它不定義 HTML 呈現設定檔、Markdown 與 SVG 的通用雙向轉換、完整排版引擎、多人協作傳輸協定、數位簽章、PDF 分頁、圖形語意本體或無障礙認證。

### 1.2 目的（Purpose）

實作 MUST 使文件可在不執行腳本、不下載相依資源的情況下抽取 Markdown。產生器 MUST 輸出可獨立顯示的靜態 SVG，並保留可搜尋、可抽取的文字。文件 MUST 明確區分內容來源、呈現結果及對應資料。

### 1.3 適用限制

MISVG 不承諾所有 SVG 軟體都保留 metadata，也不承諾跨字型或跨呈現器的像素一致。僅能看到圖片的 AI 不具備 MISVG 原文存取能力；系統 MUST 向執行原文處理的 AI 或工具提供 XML／抽取後文字。

## 2. 規範性引用文件（Normative References）

下列指定版次是實作所需依據。除本文件明列限制外，底層語法與語意依其定義；未自動納入未來版次。

| 代號 | 文件與用途 |
|---|---|
| [BCP14a] | [RFC 2119, Key words for use in RFCs to Indicate Requirement Levels, 1997](https://www.rfc-editor.org/rfc/rfc2119.html)：要求程度，第 3 章使用。 |
| [BCP14b] | [RFC 8174, Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words, 2017](https://www.rfc-editor.org/rfc/rfc8174.html)：大寫詞解釋，第 3 章使用。 |
| [XML] | [XML 1.0, Fifth Edition, 2008](https://www.w3.org/TR/2008/REC-xml-20081126/)：XML 語法、字元與換行處理，第 5、6 章使用。 |
| [XMLNS] | [Namespaces in XML 1.0, Third Edition, 2009](https://www.w3.org/TR/2009/REC-xml-names-20091208/)：命名空間識別，第 5 章使用。 |
| [SVG11] | [SVG 1.1, Second Edition, 2011](https://www.w3.org/TR/2011/REC-SVG11-20110816/)：靜態圖形、文字、metadata 與 `image/svg+xml`，第 5、7、14 章使用。 |
| [CM] | [CommonMark 0.31.2, 2024-01-28](https://spec.commonmark.org/0.31.2/)：Markdown 解析，第 6 章使用。 |
| [MDTYPE] | [RFC 7763, The text/markdown Media Type, 2016](https://www.rfc-editor.org/rfc/rfc7763.html)：原文媒體類型，第 5、14 章使用。 |
| [SHA256] | [FIPS 180-4, Secure Hash Standard, August 2015](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)：SHA-256 演算法，第 8 章使用。 |
| [UUID] | [RFC 9562, Universally Unique IDentifiers, 2024](https://www.rfc-editor.org/rfc/rfc9562.html)：UUIDv4，第 5、8 章使用。 |

## 3. 用語、定義與要求程度

### 3.1 規範用語

本文大寫的 `MUST`、`MUST NOT`、`SHALL`、`SHALL NOT`、`SHOULD`、`SHOULD NOT`、`MAY`，依 [BCP14a] 與 [BCP14b] 解釋。只有全大寫使用時具有該規範意義。本文以 `MUST` 為主要強制用語，不混用中文「可以」表示強制要求。

| 用語 | 意義 |
|---|---|
| MUST / SHALL | 符合規範必須遵守。 |
| MUST NOT / SHALL NOT | 符合規範不得採取。 |
| SHOULD / SHOULD NOT | 原則上應／不應；偏離需理解後果並記錄理由。 |
| MAY | 允許的選項。 |

### 3.2 定義

| 術語 | 定義 |
|---|---|
| 來源（source） | `m:source` 解析後的 Markdown 字元序列。 |
| 視圖（view） | 根元素下由 `m:presentation/@root-ref` 指向的唯一 SVG `g` 子樹。 |
| 來源摘要（source digest） | 對第 8.1 節指定來源位元組計算的 SHA-256 值。 |
| 綁定（binding） | 來源行範圍至視圖元素 ID 的映射，不代表雙向可逆。 |
| 文件識別碼（document ID） | 跨修訂保持不變的 UUIDv4 URN。 |
| 修訂（revision） | 同一文件已提交內容或呈現的遞增整數。 |
| 設定檔（profile） | 對容器內呈現能力施加的共同限制。 |
| 未知擴充 | 工具不能完整解釋的外部命名空間 metadata。 |

### 3.3 處理角色

Reader 抽取並報告內容；Producer 建立有效封裝；Editor 修改既有封裝；Validator 執行其宣稱範圍的檢查。一般 SVG Viewer 僅顯示圖形，不因此成為 MISVG Reader。

## 4. 架構與權威來源

### 4.1 邏輯模型

一份文件 MUST 恰有一個來源、一個呈現描述及一個視圖。Markdown 是內容權威；對應資料是索引；SVG 是內容的視覺表示。

```text
SVG 容器
├── title + desc              人類與輔助工具用摘要
├── metadata
│   └── m:document
│       ├── m:source          唯一內容來源
│       ├── m:presentation    來源摘要、產生器與視圖參照
│       ├── m:bindings?       來源行 → 視圖 ID
│       └── m:extensions?     非必要、不改變內容意義的 metadata
└── g                         靜態圖文視圖
```

### 4.2 內容完整性

Producer MUST 保留來源所表達的可見內容與關係，並 MUST NOT 在視圖中加入來源沒有的實質敘述。裝飾、背景、版次與文件識別碼 MAY 顯示，但 MUST 與內容區分。Markdown 語法符號、連結參照定義等不要求逐字顯示。

若視圖採流程圖形式，箭頭的方向、條件及意義 MUST 能從來源中的明確敘述導出。僅憑幾何位置或顏色推定關係不符合本要求。0.1 不提供通用機器關係圖；需查詢節點／邊的系統 SHOULD 另外制定具有獨立版本的擴充規範。

### 4.3 不一致時的行為

來源與視圖不一致時，Reader MUST 回報來源為權威並警示視圖不可靠。Editor MUST 從來源重新產生，或以明確的內容編輯將視圖變更寫回來源再產生。Editor MUST NOT 自動以 OCR 或幾何推論覆蓋來源。

## 5. XML 容器與欄位

### 5.1 序列化與命名空間

容器 MUST 為符合 [XML] 與 [XMLNS] 的 UTF-8 XML 1.0。Producer MUST NOT 輸出 UTF-8 BOM；Reader MUST 接受檔案開頭的 UTF-8 BOM。若有 XML 宣告，版本 MUST 為 `1.0`，encoding 若出現 MUST 為 `UTF-8`（不分大小寫）。

根元素 MUST 是 `{http://www.w3.org/2000/svg}svg`。MISVG 0.1 的命名空間固定為：

```text
https://example.org/ns/markdown-in-svg/0.1
```

這是草案測試用識別符，不是已註冊或由本專案控制的服務網址。工具 MUST 以完整命名空間 URI 及 local name 比較元素，MUST NOT 依賴範例的 `m` 前綴，也 MUST NOT 為解析命名空間而發出網路請求。

根元素 MUST 依序包含且只包含一個 `title`、一個 `desc`、一個 `metadata`、一個 `g`。根元素 MUST 有 `version="1.1"`、`width`、`height`、`viewBox`。尺寸及其他屬性依第 7 章。`title`、`desc` MUST 是非空純文字且描述本文件；這是最低描述要求，不等於無障礙認證。

除 `m:source` 外，元素間縮排空白 MAY 存在；其他非空白游離文字 MUST NOT 出現在 element-only 容器。註解 MAY 存在於來源以外位置，且不具規範意義。所有 processing instruction（XML 宣告除外）、DOCTYPE 與自訂實體宣告 MUST NOT 出現。

### 5.2 文件 metadata

`svg:metadata` MUST 只包含一個 `m:document`。`m:document` MUST 按以下順序包含 `m:source`、`m:presentation`、可選 `m:bindings`、可選 `m:extensions`，各至多一個。MISVG 元素的屬性皆無命名空間，唯明列的 `xml:space` 例外。

| `m:document` 屬性 | 必要性 | 定義 |
|---|---|---|
| `version` | MUST | 固定 `0.1`，與文件草案版次不同。 |
| `profile` | MUST | 固定 `static`。 |
| `doc-id` | MUST | 小寫 `urn:uuid:` 加符合 [UUID] 的 UUIDv4；格式見附錄 A。 |
| `revision` | MUST | 1 至 9007199254740991 的十進位整數，不得有前導零。 |

### 5.3 來源元素

| `m:source` 屬性 | 必要性 | 定義 |
|---|---|---|
| `media-type` | MUST | 固定 `text/markdown`，依 [MDTYPE]。 |
| `dialect` | MUST | 固定 `commonmark-0.31.2`；這是 MISVG token，不是 IANA variant 註冊。 |
| `xml:space` | MUST | 固定 `preserve`。 |

`m:source` MUST 只含文字及／或 CDATA，不得含子元素、註解或 processing instruction；內容 MAY 為空。`xml:space` 不會取消 XML 換行正規化。

### 5.4 呈現描述

`m:presentation` MUST 為空元素，並具有以下屬性：

| 屬性 | 定義 |
|---|---|
| `root-ref` | 視圖 `g` 的 ID；裸 ID，不含 `#`。 |
| `source-digest` | `sha256:` 加 64 個小寫十六進位字元。 |
| `renderer` | 非空的產生器名稱，長度 1–128 個 Unicode 碼點。 |
| `renderer-version` | 非空的產生器版次，長度 1–64 個 Unicode 碼點；不強制 SemVer。 |

產生器識別供診斷使用，MUST NOT 被視為可信來源證明。相同名稱與版次不承諾像素一致。`root-ref` MUST 指向根元素下的唯一 `g`。

### 5.5 關閉的核心詞彙

核心 MISVG 元素 MUST NOT 包含未定義的屬性或子元素。未知核心詞彙 MUST 視為無效，不能以「忽略未知內容」通過本版驗證。外部擴充僅依第 10 章進入 `m:extensions`。

## 6. Markdown 與字元處理

### 6.1 正規來源

原文匯入時，Producer MUST 將 CRLF 及單獨 CR 正規化為 LF。除這個轉換外，MUST 保留所有來源字元，包括尾端空白、tab、空行、是否含最後 LF 及 Unicode 組合形式。MUST NOT 自動 trim、補末尾換行或執行 NFC／NFD。

Reader MUST 使用 XML 解析後的字元序列。依 [XML]，檔案中的實體換行先被正規化；但由 `&#13;` 產生的 U+000D 不會被該步驟消除。解析後來源含任何 U+000D 時，Reader MUST 拒絕符合性並回報 `E_SOURCE`，不得悄悄修正後宣稱原檔有效。

XML 1.0 不允許的字元（例如 U+0000）MUST 導致匯入失敗，Producer MUST NOT 靜默刪除。檔案開頭 BOM 不屬於來源；來源內的 U+FEFF 則是普通資料且 MUST 保留。

### 6.2 Markdown 語意

來源 MUST 依 [CM] 解析。GFM 表格、刪除線、任務清單、YAML front matter、數學公式、Mermaid 執行及 include 指令不是本版的擴充語法。工具 MUST NOT 在宣稱 0.1 核心呈現時，悄悄採用會改變語意的方言。

CommonMark raw HTML 節點 MUST 以其原始標記作為可見文字呈現，MUST NOT 作為活動 HTML 執行。程式碼區塊 MUST 作為文字，且 MUST NOT 執行。一般連結 MUST 顯示連結標籤，且將解析後目的地以可見文字緊隨標籤呈現；自動連結本身已顯示目的地時不必重複。影像 MUST 以可見的替代文字及目的地文字呈現，替代文字為空時使用固定文字 `[image]`。這些是本設定檔的靜態輸出規則；解析仍使用 CommonMark。

連結目的地在文件內僅是資料，Producer／Reader MUST NOT 因為解析或呈現而自動存取。來源中的相對路徑 MUST 以原值保留與顯示，不依文件路徑或 `xml:base` 自動解析。

### 6.3 XML 跳脫與往返

Producer MAY 使用 XML 文字跳脫或 CDATA；兩者抽取後 MUST 得到相同來源。來源含 `]]>` 時，使用 CDATA 的 Producer MUST 拆分 CDATA，例如以 `]]]]><![CDATA[>` 表示該序列，或改用一般 XML 文字跳脫。雜湊 MUST 在 XML 解碼後計算，而非對 CDATA 標籤或 `&amp;` 字面值計算。

所謂無損抽取僅指正規來源字元序列，不承諾原始 `.md` 的 BOM、CRLF 位元組或 XML 前綴與屬性排列復原。

## 7. 靜態呈現設定檔（Static Profile）

### 7.1 元素白名單

下列限制是對 [SVG11] 的封閉子集；未允許的元素、屬性與命名空間 MUST NOT 出現在視圖中。

| 位置／元素 | 子元素 |
|---|---|
| 根 `svg` | 僅第 5.1 節的四個子元素。 |
| 視圖 `g` 與巢狀 `g` | `g`、`text`、`rect`、`circle`、`ellipse`、`line`、`polyline`、`polygon`、`path`。 |
| `text`、`tspan` | 文字及 `tspan`。 |
| 幾何圖形 | 無子元素。 |

`foreignObject`、`script`、`style`、`image`、`a`、`use`、`defs`、濾鏡、動畫及外部字型不屬於本設定檔。Producer MUST NOT 用路徑取代承載文件內容的文字；純裝飾或箭頭 MAY 使用 path。

### 7.2 屬性白名單

所有屬性均無命名空間，命名空間宣告不計作屬性。除根元素外，視圖元素皆 MAY 有 `id`。根元素只允許 `version`、`width`、`height`、`viewBox`。

| 元素 | 可用屬性（除 `id` 外） |
|---|---|
| `g` | `transform` 及下列共用呈現屬性。 |
| `text`, `tspan` | `x`, `y`, `dx`, `dy` 及共用呈現屬性；`text` 另可有 `transform`, `xml:space="preserve"`。 |
| `rect` | `x`, `y`, `width`, `height`, `rx`, `ry`, `transform` 及共用呈現屬性。 |
| `circle` | `cx`, `cy`, `r`, `transform` 及共用呈現屬性。 |
| `ellipse` | `cx`, `cy`, `rx`, `ry`, `transform` 及共用呈現屬性。 |
| `line` | `x1`, `y1`, `x2`, `y2`, `transform` 及共用呈現屬性。 |
| `polyline`, `polygon` | `points`, `transform` 及共用呈現屬性。 |
| `path` | `d`, `transform` 及共用呈現屬性。 |

共用呈現屬性僅為 `fill`, `stroke`, `stroke-width`, `stroke-linecap`, `stroke-linejoin`, `font-family`, `font-size`, `font-weight`, `font-style`, `text-anchor`。無其他 CSS 入口。

`fill` 與 `stroke` 只允許 `none` 或 `#RRGGBB`（十六進位大小寫皆可）。`font-family` 是以逗號分隔的非空名稱串列，每個名稱只含 Unicode 字母、十進位數字、ASCII 空格與連字號，不含引號、括號或跳脫；MUST 最後提供 `sans-serif`、`serif` 或 `monospace` 之一。其餘列舉值依 [SVG11]；`font-weight` 限 `normal`, `bold`, `100` 至 `900` 的百位整數，`font-style` 限 `normal`, `italic`, `oblique`。

### 7.3 幾何與畫布

根 `width`、`height` MUST 是 1–16384 的無單位十進位整數且無前導零；兩者乘積 MUST NOT 超過 16777216。`viewBox` MUST 表示 `0 0 width height` 四個數值。其餘長度 MUST 是有限、無單位的 SVG 數字；font-size MUST 大於零，stroke-width 與尺寸／半徑 MUST 非負。text／tspan 的 `x`, `y`, `dx`, `dy` 在本版只允許單一數字；不允許百分比、單位、CSS 變數、`calc()` 或非有限值。

`d`、`points`、`transform` 的文法依 [SVG11]，所有數值 MUST 有限。`path` MUST 有非空有效的 `d`；`polyline`／`polygon` MUST 有有效的 `points`。元素缺省值、繪製順序與呈現屬性繼承依 [SVG11]。

Producer MUST 將可見文字排入畫布，避免裁切、文字互相遮蔽或無法辨識的前景／背景配色。來源語言所需字型不足時，Producer MUST 回報呈現限制，不能將缺字方塊視為成功。精確字型度量與像素對齊不作為跨實作符合性的要求。

### 7.4 文字與閱讀順序

視圖的 XML 順序 SHOULD 對應合理閱讀順序。內容文字 MUST 使用 `text`／`tspan`。Producer SHOULD 以適當的文字分行與樣式呈現標題、段落、清單、引用、強調及程式碼；不得依賴腳本完成初始排版。保留來源全文並不自動滿足螢幕閱讀器或 WCAG 要求。

## 8. 摘要、同步與編輯交易

### 8.1 摘要演算法

`source-digest` MUST 由以下步驟產生：

1. 使用安全 XML 解析器取得 `m:source` 的全部文字／CDATA 字元，依文件順序串接。
2. 確認來源符合第 6 章；不得移除任何空白或補 LF。
3. 將字元序列編碼為 UTF-8，不加 BOM。
4. 依 [SHA256] 計算 SHA-256，轉成 64 個小寫十六進位字元。
5. 前置 ASCII 字串 `sha256:`。

```text
source_digest = "sha256:" + lower_hex(SHA256(UTF8(source)))
```

摘要範圍只含來源，不含文件 ID、revision、renderer、綁定、擴充或 SVG。沒有循環摘要或 XML canonicalization 的需求。修改版面但不改來源時摘要不變。

### 8.2 綁定狀態

Reader MUST 比對計算值與宣告值。不同時 MUST 回報 `E_DIGEST_MISMATCH`；MAY 以未通過驗證的復原模式抽取來源，但 MUST NOT 宣稱封裝有效。

相符時只能報告 `source-binding=matched`。工具 MUST NOT 將此狀態稱為簽章有效、作者已驗證、畫面已驗證或安全可信。即使摘要相符，畫面仍可能被單獨修改，或惡意作者可能同時修改來源與摘要。

### 8.3 原子更新

Editor 提交一次變更時 MUST：

1. 記錄原檔的完整位元組 SHA-256 作為本地前置條件；這個交易指紋不寫入格式。
2. 依使用者意圖修改來源及／或版面，依需求重新產生視圖與 bindings。
3. 保持同一 `doc-id`，將 `revision` 增加 1；達到最大值時拒絕提交。
4. 更新 `source-digest`，驗證候選檔；不得只更新摘要來掩蓋過期視圖。
5. 寫入前在鎖定或儲存端比較並交換機制下驗證前置條件仍成立。
6. 以不可見中間狀態的原子替換／交易提交候選檔。失敗則保留原檔。

只有前置條件成立的結果可覆寫；不成立時 MUST 回報 `E_CONFLICT`。單純「先檢查再寫入」而無鎖或條件寫入，不能滿足本節。revision 相同不代表檔案相同；MUST NOT 僅以 revision 判斷衝突。

重新序列化而不改任何來源、呈現、綁定或 metadata 的工具 MAY 保持 revision。以來源建新文件時初始 revision MUST 為 1；複製成獨立文件 MUST 依 [UUID] 產生新 UUIDv4，不能沿用範例 UUID。一般搬移／複製備份不算建立新文件。

### 8.4 合併與復原

實作 SHOULD 先以來源為單位執行三方合併，再重新產生視圖；MUST NOT 把 Git 的 XML 文字合併成功視為語意合併成功。含未解決來源衝突標記的候選檔 MUST NOT 作為已完成編輯提交；若衝突標記原本就是文件討論內容，實作 MAY 依明確上下文保留。

來源遺失或無法抽取時，僅剩一般 SVG，MUST NOT 宣稱它仍是有效 MISVG。修復操作 MUST 產生可區分的新結果，且 MUST NOT 靜默變更輸入檔。

## 9. 來源對應（Source Bindings）

`m:bindings` MAY 省略；存在時 MUST 含一個或多個空的 `m:bind`。每個 bind MUST 有 `target`、`start-line`、`end-line`，不得有其他屬性。

`target` MUST 是視圖內既存元素的裸 ID，且每個 target 在 bindings 中 MUST 至多出現一次。所有視圖 ID MUST 唯一，並符合附錄 A 的 ID 文法；視圖根 `g` MUST 有 ID。多個 target MAY 對應同一來源行範圍。

行範圍是 **1 起算、兩端包含**。來源先用 LF 分割；若最後一個字元是 LF，移除分割結果最後那個終止用空片段；空來源的行數定義為 0。因此 `"a\n"` 有 1 行、`"a\n\n"` 有 2 行、`"\n"` 有 1 行。MUST 滿足 `1 ≤ start-line ≤ end-line ≤ 行數`。

空來源 MUST 不含 bindings。綁定不要求覆蓋所有來源行，亦不證明畫面已完整呈現。Editor 在來源變動後 MUST 重算受影響的綁定，或整體移除 bindings，MUST NOT 保留已知過期的行號。視覺元件意義未變時 SHOULD 保持 ID 穩定。

## 10. 擴充、版本與保留規則

### 10.1 版本協商

Reader MUST 明確比對 `version`、命名空間及 profile。只實作 0.1 的 Reader 收到 0.2、1.0、其他命名空間或非 `static` profile 時 MUST 回報 `E_UNSUPPORTED`，不得猜測相容。可用未驗證復原模式讀取資料，但 MUST 標示支援範圍。

0.x 版間不承諾相容。文件版次 `0.1.1` MAY 是不改變 wire format 的編輯修訂；若新增必要欄位、改變摘要或內容語意，MUST 使用新的 wire version 與命名空間。

### 10.2 非必要擴充

`m:extensions` MAY 包含一個或多個外部命名空間元素。頂層擴充命名空間 MUST 非空，且 MUST NOT 是 SVG、MISVG 或 XML 命名空間。整個擴充子樹 MUST NOT 出現 SVG 或 MISVG 命名空間元素。其文字與屬性皆是惰性資料，不得用來要求程式執行。

擴充只能攜帶可忽略的補充 metadata；MUST NOT 改變核心來源的權威性、解釋方式、安全要求或視圖生成語意。若忽略就會誤解內容，該功能需要另行制定新 profile／版本，不能塞入本節的可選擴充。

Reader MAY 忽略未知擴充，但 MUST 保留來源解讀。Editor 對未知擴充進行無內容變更的往返時 MUST 保留其元素／屬性的 expanded name、字串值、子節點順序與文字；前綴、屬性順序與 CDATA 邊界不必一致。

Editor 若不能判斷未知擴充在修改後是否有效，MUST 中止一般保存並回報 `E_EXTENSION_EDIT`，或以明確的「移除未知擴充」操作另存結果。不能把未知的舊摘要或行號原樣保留後宣稱已同步。只有使用者或呼叫端明確選擇移除的操作才可丟棄它們。

## 11. 符合性與互通性（Conformance）

### 11.1 文件符合性

宣稱 `MISVG 0.1 static` 的文件 MUST 符合第 4–10 章、附錄 A 的全部適用 MUST／MUST NOT 要求。XML Schema 通過是必要結構證據之一，不能代替來源摘要、參照、SVG 子集或語意／視覺檢查。

### 11.2 角色符合性

| 角色 | 必須具備的能力 |
|---|---|
| Reader | 安全解析、核心結構與版本識別、原文無損抽取、摘要檢查、錯誤／限制報告。不得把未檢查的視圖稱為已驗證。 |
| Producer | 產生符合容器與 static profile 的文件；保留內容與文字；提供摘要與產生器資訊；履行視覺／內容完整性檢查。 |
| Editor | Reader 與 Producer 要求，加上原子更新、衝突、revision、綁定及未知擴充處理。 |
| Validator | 明列檢查範圍；按第 11.3 節報告，不把部分檢查結果當作全面符合性。 |

### 11.3 檢查層次

Validator MUST 分開報告：

- `structure`：XML、metadata、欄位、唯一性與參照。
- `source-binding`：來源規則、摘要與行範圍。
- `static-profile`：全部元素、屬性、值域及底層 SVG 文法。
- `content-fidelity`：來源與畫面是否保留相同實質內容。
- `visual-review`：實際呈現的文字、閱讀順序、裁切、重疊與缺字。

每項狀態 MUST 為 `pass`、`fail`、`not-checked` 或 `unsupported`。未執行的項目 MUST 使用 `not-checked`，不得用 pass。摘要通過不推出其他項目通過。完整符合性聲明 MUST 有全部五項通過的證據；後兩項 MAY 包含人工審查。

### 11.4 互通性驗證

宣稱角色符合性的實作 MUST 執行附錄 B 中適用該角色的案例並記錄結果。Producer 與 Editor 的發布測試 SHOULD 包含兩個獨立 SVG 呈現器，以及跨工具的抽取—重新封裝測試。只完成本專案附帶範例的檢查，不構成普遍互通性認證。

### 11.5 資源限制

實作 MUST 為檔案大小、來源大小、XML 深度、節點數、字串長度、圖形複雜度及執行時間設定可公布的限制。起始部署 SHOULD 採取：檔案 8 MiB、來源 1 MiB、深度 64、節點 50000、單一 path 65536 字元。這些是實作建議，不是格式合法性上限。因限制而停止時 MUST 回報 `E_LIMIT`／`unsupported`，不能宣稱輸入必然格式錯誤。

## 12. 錯誤處理（Error Handling）

| 錯誤碼 | 含義／最低行為 |
|---|---|
| `E_XML` | XML 不合法、編碼不支援或含禁止宣告；停止正常解析。 |
| `E_STRUCTURE` | 必要欄位、順序、基數、型別或核心詞彙不符。 |
| `E_UNSUPPORTED` | 未支援版本、命名空間、方言或 profile；不猜測。 |
| `E_SOURCE` | 來源字元／節點違反規則。 |
| `E_DIGEST_MISMATCH` | 計算摘要與宣告值不同。 |
| `E_REFERENCE` | 重複 ID、無效 root-ref、無效 target 或行範圍。 |
| `E_PROFILE` | 違反靜態元素／屬性／值域限制。 |
| `E_CONTENT` | 視圖遺漏、改寫或新增實質內容。 |
| `E_VISUAL` | 已觀察到裁切、遮蔽、缺字或不可讀內容。 |
| `E_CONFLICT` | 原檔已變更；不得覆寫。 |
| `E_EXTENSION_EDIT` | 無法安全更新或保留未知擴充。 |
| `E_LIMIT` | 超出已公布處理限制，並非格式不合法的證明。 |

若多項錯誤同時存在，實作 MAY 回報第一項或全部，MUST NOT 為取得更多錯誤而執行危險內容。診斷 SHOULD 附元素路徑、欄位或來源行號；MUST NOT 默認將整份來源、祕密或本機完整路徑送往外部服務。

## 13. 安全性與隱私考量（Security and Privacy Considerations）

### 13.1 XML 與主動內容

所有處理器 MUST 停用外部實體、DTD 載入、網路 schema 解析及 XInclude 展開。MUST 在導入 DOM、瀏覽器或其他可執行環境前檢查不可信輸入。不得先顯示活動 SVG，再進行消毒。CDATA 是字串容器，並非消毒器。

靜態白名單排除事件屬性、腳本、CSS `url()`、外部資源與外部 HTML。即使來源包含 HTML、JavaScript、連結或指令，也 MUST 僅作資料處理。工具 MUST 限制資源消耗，且在錯誤時停止相關處理。

### 13.2 AI 信任邊界

文件中的 Markdown、註解、擴充及產生器名稱皆是不可信文件資料。接收端 MUST NOT 因為其中寫有「系統指令」、工具呼叫、上傳要求或權限宣告，就提升其權限。將文件送給 AI 時，應用程式 MUST 區分使用者授權與文件內容；執行來源內程式碼、網路請求或檔案操作不屬於 MISVG 解析。

### 13.3 隱私與內容隱藏

可見 SVG 沒有顯示的內容仍可能存在來源或 metadata。發布工具 MUST 提供檢查完整來源與 metadata 的能力，MUST NOT 把畫面遮罩視為刪除資料。移除敏感資料時 MUST 同時處理來源、視圖、綁定與擴充；若產生新的公開衍生文件，SHOULD 給予新 doc-id。

### 13.4 完整性與真實性

SHA-256 摘要沒有金鑰，不能認證作者或防止攻擊者同時重寫內容及摘要。本版不定義數位簽章、信任根、時間戳或撤銷機制。實作 MUST NOT 宣稱 `source-digest` 提供這些保證。

## 14. IANA 與識別碼考量（IANA Considerations）

本草案不要求任何新的 IANA 登錄。外層媒體類型 MUST 使用 [SVG11] 的 `image/svg+xml`；內嵌原文以 [MDTYPE] 的 `text/markdown` 描述，沒有新增媒體類型或已註冊的 Markdown variant。

檔名 SHOULD 使用 `.misvg.svg` 方便識別；一般 `.svg` 亦有效。檔名不能代替命名空間與結構偵測。工具 MUST NOT 以未註冊的 `application/misvg` 作為本規範的正式媒體類型。

命名空間是第 5.1 節的草案識別符。正式發布前維護者 MUST 選擇可長期治理的命名空間並定義遷移；若變更 URI，舊檔不會自動成為新版本。不得在未授權情況下使用 IEEE、IETF 或 W3C 的識別碼作為本規範的官方註冊標記。

## 15. 版本治理與變更管理

發布者 MUST 分別記錄「規範草案版次」「wire version」「個別文件 revision」。勘誤 MUST 指明受影響條款及是否影響互通性；改變線上語意的修訂 MUST 使用新 wire version。

實作若要從 0.x 走向穩定 1.0，維護者 SHOULD 完成：固定命名空間與授權、至少兩個獨立 Reader／Producer 的交換測試、字元與衝突測試、威脅模型審查及正式相容性政策。後續 `html` profile、圖形關係模型、資源封裝、樣式資源與簽章 SHOULD 分開提案，不能未經版本化直接改變 static。

## 附錄 A（規範性）：詞彙與結構限制

下列正規表示式 MUST 作完整字串匹配；字元範圍均為 ASCII，除非另述。

```text
ID        = [A-Za-z][A-Za-z0-9._-]{0,63}
DIGEST    = sha256:[0-9a-f]{64}
POSINT    = [1-9][0-9]*
UUID4URN  = urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}
```

POSINT 仍受各欄位值域約束。元素基數如下：

```text
svg := title, desc, metadata, g
metadata := m:document
m:document := m:source, m:presentation, m:bindings?, m:extensions?
m:source := XML character data / CDATA only
m:presentation := empty
m:bindings := m:bind+
m:bind := empty
m:extensions := foreign-element+
```

附件 `schema/misvg-metadata-0.1.xsd` 是 metadata 結構的輔助 schema，並非整份 SVG 的 schema。它不涵蓋所有詞彙細節、來源摘要、參照、SVG 值域、資源安全或視覺要求；不得單憑 XSD 驗證宣稱符合本規範。

## 附錄 B（規範性）：符合性測試要求

實作 MUST 依角色覆蓋下列適用測試。表中「有效」仍須其他條件成立；修改樣本後若不是在測試摘要失配，測試程式 MUST 重算正確摘要，避免錯誤被其他原因掩蓋。

| 編號 | 測試輸入／操作 | 預期結果 | 適用角色 |
|---|---|---|---|
| T01 | 完整有效範例 | 精確抽取來源、摘要相符、顯示可讀。 | 全部 |
| T02 | `m` 改成其他前綴，URI 不變 | 同樣有效；結果不依前綴。 | R/P/E/V |
| T03 | 等價的 CDATA 與 XML 跳脫 | 抽取文字與摘要完全相同。 | R/P/E/V |
| T04 | 來源包含 `]]>`、`&`、`<` | 可安全序列化並往返。 | R/P/E/V |
| T05 | 來源 `abc`，無 LF | 摘要為 `sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`。 | R/P/E/V |
| T06 | 空來源 | 摘要為 `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`，無 bindings。 | R/P/E/V |
| T07 | `abc` 改為 `abc` 加 LF | 摘要不同；不得 trim。 | R/P/E/V |
| T08 | 來源內實體 CRLF 與 LF 的 XML | XML 解碼後等價，摘要相同。 | R/E/V |
| T09 | 來源內 `&#13;` | `E_SOURCE`。 | R/E/V |
| T10 | `é` 與 `e` 加 U+0301 | 保留不同位元組、摘要不同。 | R/P/E/V |
| T11 | 改來源但保留舊摘要 | `E_DIGEST_MISMATCH`，不得宣稱已同步。 | R/E/V |
| T12 | 改畫面文字、來源與摘要不變 | 摘要可能相符；內容審查應為 fail，僅摘要工具須標示 content-fidelity 未檢查。 | P/E/V |
| T13 | 第二個 source／document、未知核心屬性 | `E_STRUCTURE`。 | R/E/V |
| T14 | 重複視圖 ID、失效 root-ref／target、範圍越界 | `E_REFERENCE`。 | R/E/V |
| T15 | source 內子元素或註解 | `E_SOURCE` 或 `E_STRUCTURE`。 | R/E/V |
| T16 | DOCTYPE／外部實體／processing instruction | 拒絕；零網路與檔案外部讀取。 | R/E/V |
| T17 | script、事件屬性、foreignObject、style、href、data URI、URL paint | `E_PROFILE`；不得先執行或載入。 | P/E/V |
| T18 | 未知版本／profile／方言 | `E_UNSUPPORTED`，不假定相容。 | R/E/V |
| T19 | 一般 Reader 讀未知惰性擴充 | 可忽略資料、不改核心解釋；不得執行。 | R/V |
| T20 | 編輯具有未知擴充的來源 | `E_EXTENSION_EDIT`，或呼叫端明確選擇移除後另存。 | E |
| T21 | 讀取後另一程序更改檔案，即使 revision 相同 | `E_CONFLICT`，原檔保留。 | E |
| T22 | 提交中斷／模擬寫入失敗 | 既有檔案保持完整；不暴露半成品。 | E |
| T23 | 內容文字改成 paths、裁切、缺字 | profile／visual-review 或 content-fidelity 失敗。 | P/E/V |
| T24 | 超過已公布處理限制 | `E_LIMIT`／unsupported，非必然 invalid。 | R/P/E/V |
| T25 | 移除 metadata 後只留 SVG | 可為一般 SVG；不是 MISVG。 | R/E/V |
| T26 | 來源含圖片、raw HTML、程式碼及相對連結 | 依第 6.2 節靜態顯示、無自動請求或執行。 | P/E |
| T27 | 空來源、末尾 LF 與連續 LF 的行數 | 依第 9 章；不得建立不存在的行。 | R/P/E/V |
| T28 | 檔案 BOM 與來源 U+FEFF | 接受前者；後者保留且參與摘要。 | R/E/V |
| T29 | 不改內容的 XML 重新序列化 | 來源、摘要、擴充語意保持；revision 可不變。 | E |
| T30 | 根尺寸超界、非有限數、非法 path／transform | static-profile 失敗。 | P/E/V |

R/P/E/V 分別代表 Reader、Producer、Editor、Validator。Validator 僅對其明列的範圍適用，但 MUST 報告未執行的檢查。

## 附錄 C（資訊性）：完整範例與操作流程

預設英文範例見 `examples/order-flow.en.misvg.svg`，抽取對照原文見 `examples/order-flow.en.md`。繁體中文與日文範例分別使用 `.zh-Hant`、`.ja` 語言尾碼。`examples/order-flow.misvg.svg` 與 `.md` 保留為原有繁體中文相容試料。樣本 UUID 僅供測試，不應用來建立新文件。

```text
# 訂單流程

1. 客戶完成付款。
2. 倉庫確認付款成功後安排出貨。

規則：付款未成功，不得出貨。
```

正常工作流程：安全讀取 → 抽取來源 → 檢查綁定 → 編輯 Markdown → 產生畫面 → 更新行對應與摘要 → 檢查內容與渲染 → 原子提交。版面編輯同樣增加 revision，但來源未改時 source-digest 不變。

來源摘要的最小 Python 示意：

```python
import hashlib

def source_digest(parsed_source: str) -> str:
    if "\r" in parsed_source:
        raise ValueError("E_SOURCE")
    return "sha256:" + hashlib.sha256(
        parsed_source.encode("utf-8")
    ).hexdigest()
```

此函式不負責安全 XML 解析，也不負責驗證畫面。完整範例中的畫面是按來源人工編排的參考視圖；本交付包不提供通用 Markdown 排版引擎。

## 附錄 D（資訊性）：設計理由與取捨

| 決策 | 理由與代價 |
|---|---|
| Markdown 單一內容權威 | 避免兩份內容競爭；代價是拖曳改字後必須有明確寫回流程。 |
| 使用 SVG metadata | 同檔攜帶原文且不參與畫面；但繪圖／最佳化工具可能刪除它。 |
| 原生 SVG static 子集 | 降低外部資源與活動內容依賴；無法直接使用 HTML 表格、圖片或完整 CSS。 |
| 固定 CommonMark 版次 | 避免方言漂移；GFM／Mermaid 需另立擴充或新版本。 |
| 只雜湊來源 | 簡單、可重現、避免自我參照；不提供視圖完整性或簽章。 |
| 可選行範圍對應 | 容易實作與除錯；不能單獨代表 AST 身分或任意雙向編輯。 |
| 關閉核心詞彙 | 使錯字與版本差異可被檢出；新增核心能力必須版本化。 |
| 不宣稱像素一致 | 字型、平台與引擎影響呈現；必須另做視覺檢查。 |

第一版刻意保持交換協定精簡。若主要目標是長篇文件與複雜表格，Markdown／HTML 文件加 SVG 插圖通常仍更合適。這份格式適合「需要同一張圖保留可編輯原文」的場景。

## 附錄 E（資訊性）：編排依據與參考資料

- [RFC 7322, RFC Style Guide](https://www.rfc-editor.org/rfc/rfc7322.html)：參考摘要、文件地位、章節交叉引用、引用分類與安全性章節；本文不是其全部排版規則的逐條實作。
- [IEEE SA Standards Style Manual, 2021](https://development.standards.ieee.org/myproject/Public/mytools/draft/styleman.pdf)：參考概述／引用／定義順序、可驗證要求與規範性／資訊性附錄分離。
- [IEEE SA — Drafting the Standard](https://standards.ieee.org/develop/drafting-standard/)：正式 IEEE 草案使用其程序與範本；本文件未經該程序。
- [RFC 2606, Reserved Top Level DNS Names](https://www.rfc-editor.org/rfc/rfc2606.html)：說明示例網域的用途；本草案使用 example.org 表示尚未建立正式命名空間治理。
- [SVG 1.1 Metadata](https://www.w3.org/TR/2011/REC-SVG11-20110816/metadata.html)：底層 SVG 支援其他 XML 命名空間的 metadata；MISVG 的具體資料模型由本草案新定義。

## 附錄 F（資訊性）：交付附件與實作界限

| 附件 | 用途／界限 |
|---|---|
| `MISVG-0.1.en.md`、`.zh-Hant.md`、`.ja.md` | 三語規範全文；英文為預設與規範正文。 |
| `index.html`、`MISVG-0.1.en.html` | 預設英文入口與離線閱讀版。 |
| `MISVG-0.1.zh-Hant.html`、`MISVG-0.1.ja.html` | 含語言切換的離線譯本。 |
| `schema/misvg-metadata-0.1.xsd` | metadata 子樹結構檢查；不是完整 SVG 或安全性驗證器。 |
| `examples/order-flow.{en,zh-Hant,ja}.misvg.svg` | 三語範例，內含對應原文、真實摘要與行對應。 |
| `examples/order-flow.{en,zh-Hant,ja}.md` | 抽取對照文字，不是第二份權威來源。 |
| `examples/order-flow.misvg.svg`、`.md` | 原有繁體中文相容試料。 |
| `tests/hash-vectors.json` | UTF-8 摘要與行數測試向量。 |
| `tests/check_package.py` | 交付一致性與部分負向測試，不是符合性認證器。 |
| `tests/verification-report.json` | 本交付實際執行結果與未檢查項目。 |
| `tests/render-checks.json`、`tests/visual-review.md` | 原有單一 Chromium 呈現器量測與視覺審查紀錄。 |
| `tests/localization-report.json` | 譯本結構、識別碼、範例與導覽檢查。 |
| `tests/localization-render-checks.json` | 三語桌面／手機版面量測。 |
| `README.md`、`README.zh-Hant.md`、`README.ja.md` | 預設英文操作說明與翻譯。 |

附錄 B 的完整角色驗證需要另行實作測試工具與實際編輯器。附件測試未覆蓋完整 SVG 文法、所有 CommonMark 渲染、並行交易或跨呈現器互通性；不得將附件通過解讀為完整實作已完成。
