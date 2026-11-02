# Markdown-in-SVG (MISVG) Document Interchange Specification

**Specification for Markdown-in-SVG Document Interchange**

| Document control | Value |
|---|---|
| Document identifier | MISVG-SPEC-0001 |
| Draft revision | 0.1.1 / Draft 02 |
| Wire version | `0.1` |
| Date | 2026-11-02 |
| Status | Independent project specification draft for implementation and review |
| Specification language | English (en), default and authoritative; Traditional Chinese (zh-Hant) and Japanese (ja) translations |
| Editor / maintaining organization | To be designated; this revision was drafted with AI assistance |
| Approval status | Not approved by IEEE, IETF, W3C, or another standards organization |

## Status of This Memo

This document proposes a new Markdown-in-SVG interchange format; it is not a reproduction of an existing standard. Its organization draws on IEEE technical standards: overview, normative references, definitions, requirements, and annexes. Requirement levels follow RFC 2119 and RFC 8174. Security, IANA, and interoperability provisions are also included.

This is an independent draft using a combined editorial structure. **It does not claim IEEE editorial approval and is not an RFC, a submitted Internet-Draft, or an IEEE P-series draft.** `MISVG-SPEC-0001` is a project identifier, not a number assigned by any standards organization. Formal submission requires adaptation to the selected organization's procedures, templates, language, rights statements, and editorial requirements. This document does not select a public license on the user's behalf; the rights holder must decide before external publication.

English is the default reading language and the authoritative text for resolving discrepancies among translations. Traditional Chinese and Japanese are complete companion translations with matching clause and test identifiers. Language selection does not change the wire format, identifiers, or requirements. Revision 0.1.1 adds multilingual publication and language policy without changing wire version 0.1.

The abstract, status statement, and contents are informative. Clauses 1–15 and Annexes A and B are normative; Annexes C–F are informative. If a machine-readable attachment differs from the main text, the main text and normative annexes take precedence.

## Abstract

MISVG packages editable Markdown source, source-to-view bindings, and a static SVG view in a single UTF-8 XML document. Markdown is the sole authoritative source of content; SVG is its visual representation. Ordinary SVG viewers can display the document, while MISVG-aware tools can extract, validate, edit, and regenerate it. This specification defines the container, character handling, source digest, version control, static rendering subset, bindings, error handling, and conformance requirements. A matching digest supports only source-binding checks: it does not establish semantic correctness of the view or trustworthiness of the document.

## Contents

1. Overview
2. Normative References
3. Terms, Definitions, and Requirement Levels
4. Architecture and Authoritative Source
5. XML Container and Fields
6. Markdown and Character Handling
7. Static Rendering Profile
8. Digests, Synchronization, and Editing Transactions
9. Source Bindings
10. Extensions, Versions, and Preservation
11. Conformance and Interoperability
12. Error Handling
13. Security and Privacy Considerations
14. IANA and Identifier Considerations
15. Version Governance and Change Management

Annex A: Lexical and Structural Constraints (normative)  
Annex B: Conformance Test Requirements (normative)  
Annex C: Complete Example and Workflow (informative)  
Annex D: Design Rationale and Tradeoffs (informative)  
Annex E: Editorial Basis and Further References (informative)  
Annex F: Deliverables and Implementation Boundaries (informative)

## 1. Overview

### 1.1 Scope

This specification defines storage of Markdown source inside a single `.svg` file, binding of that source to an SVG view, a basic editing workflow, and file and tool conformance. It applies to explanatory cards, flowcharts, architecture diagrams, short specifications, and visual knowledge documents.

This revision defines only the `static` rendering profile. It does not define an HTML rendering profile, universal bidirectional Markdown/SVG conversion, a complete layout engine, a collaborative transport protocol, digital signatures, PDF pagination, a diagram semantics ontology, or accessibility certification.

### 1.2 Purpose

Implementations MUST allow extraction of Markdown without executing scripts or downloading dependencies. Producers MUST output independently displayable static SVG and preserve searchable, extractable text. Documents MUST distinguish content source, rendering output, and binding data.

### 1.3 Applicability Limits

MISVG does not guarantee that every SVG application preserves metadata or that different fonts or renderers produce identical pixels. An AI that sees only an image cannot access MISVG source. A system MUST provide XML or extracted text to an AI or tool performing source processing.

## 2. Normative References

The specified editions below are required for implementation. Except for restrictions explicitly stated here, underlying syntax and semantics follow these references. Future editions are not incorporated automatically.

| Label | Reference and use |
|---|---|
| [BCP14a] | [RFC 2119, Key words for use in RFCs to Indicate Requirement Levels, 1997](https://www.rfc-editor.org/rfc/rfc2119.html): requirement levels, Clause 3. |
| [BCP14b] | [RFC 8174, Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words, 2017](https://www.rfc-editor.org/rfc/rfc8174.html): uppercase interpretation, Clause 3. |
| [XML] | [XML 1.0, Fifth Edition, 2008](https://www.w3.org/TR/2008/REC-xml-20081126/): XML syntax, characters, and line endings, Clauses 5 and 6. |
| [XMLNS] | [Namespaces in XML 1.0, Third Edition, 2009](https://www.w3.org/TR/2009/REC-xml-names-20091208/): namespace identity, Clause 5. |
| [SVG11] | [SVG 1.1, Second Edition, 2011](https://www.w3.org/TR/2011/REC-SVG11-20110816/): static graphics, text, metadata, and `image/svg+xml`, Clauses 5, 7, and 14. |
| [CM] | [CommonMark 0.31.2, 2024-01-28](https://spec.commonmark.org/0.31.2/): Markdown parsing, Clause 6. |
| [MDTYPE] | [RFC 7763, The text/markdown Media Type, 2016](https://www.rfc-editor.org/rfc/rfc7763.html): source media type, Clauses 5 and 14. |
| [SHA256] | [FIPS 180-4, Secure Hash Standard, August 2015](https://csrc.nist.gov/pubs/fips/180-4/upd1/final): SHA-256, Clause 8. |
| [UUID] | [RFC 9562, Universally Unique IDentifiers, 2024](https://www.rfc-editor.org/rfc/rfc9562.html): UUIDv4, Clauses 5 and 8. |

## 3. Terms, Definitions, and Requirement Levels

### 3.1 Requirement Language

The uppercase terms `MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are interpreted according to [BCP14a] and [BCP14b]. They have these normative meanings only when written entirely in uppercase. This document primarily uses `MUST` for mandatory requirements.

| Term | Meaning |
|---|---|
| MUST / SHALL | Required for conformance. |
| MUST NOT / SHALL NOT | Prohibited for conformance. |
| SHOULD / SHOULD NOT | Recommended / discouraged; a deviation requires understanding the consequences and documenting the reason. |
| MAY | A permitted option. |

### 3.2 Definitions

| Term | Definition |
|---|---|
| Source | The Markdown character sequence obtained by parsing `m:source`. |
| View | The unique SVG `g` subtree directly under the root and referenced by `m:presentation/@root-ref`. |
| Source digest | The SHA-256 value of the source bytes specified in 8.1. |
| Binding | A mapping from a source line range to a view element ID; it does not imply bidirectional reversibility. |
| Document ID | A UUIDv4 URN retained across revisions of the same document. |
| Revision | An increasing integer for committed content or presentation changes to a document. |
| Profile | Common restrictions on rendering capabilities inside the container. |
| Unknown extension | Metadata in an external namespace that the tool cannot fully interpret. |

### 3.3 Processing Roles

A Reader extracts and reports content; a Producer creates valid packages; an Editor modifies existing packages; a Validator performs checks within its declared scope. An ordinary SVG Viewer displays graphics and does not thereby qualify as a MISVG Reader.

## 4. Architecture and Authoritative Source

### 4.1 Logical Model

A document MUST contain exactly one source, one presentation descriptor, and one view. Markdown is authoritative for content; bindings are indexes; SVG is a visual representation of the content.

```text
SVG container
├── title + desc              summaries for people and assistive tools
├── metadata
│   └── m:document
│       ├── m:source          sole content source
│       ├── m:presentation    source digest, renderer, and view reference
│       ├── m:bindings?       source lines → view IDs
│       └── m:extensions?     optional metadata that does not change meaning
└── g                         static graphical and textual view
```

### 4.2 Content Fidelity

A Producer MUST preserve the visible content and relationships expressed by the source and MUST NOT add substantive statements to the view that are absent from the source. Decoration, backgrounds, revision information, and the document identifier MAY be displayed but MUST be distinguishable from content. Markdown syntax markers and link reference definitions need not be displayed verbatim.

For a flowchart view, arrow directions, conditions, and meanings MUST be derivable from explicit source statements. Inferring relationships solely from geometric position or color does not meet this requirement. Version 0.1 does not provide a general machine-readable relationship graph. Systems requiring node/edge queries SHOULD define a separately versioned extension specification.

### 4.3 Inconsistency Handling

If source and view disagree, a Reader MUST report the source as authoritative and warn that the view is unreliable. An Editor MUST regenerate from the source, or explicitly edit the source to incorporate view changes before regeneration. An Editor MUST NOT automatically overwrite the source using OCR or geometric inference.

## 5. XML Container and Fields

### 5.1 Serialization and Namespaces

The container MUST be a UTF-8 XML 1.0 document conforming to [XML] and [XMLNS]. A Producer MUST NOT emit a UTF-8 BOM; a Reader MUST accept a UTF-8 BOM at the beginning of the file. If an XML declaration is present, its version MUST be `1.0`; if encoding is specified, it MUST be `UTF-8`, case-insensitively.

The root MUST be `{http://www.w3.org/2000/svg}svg`. The MISVG 0.1 namespace is fixed as:

```text
https://example.org/ns/markdown-in-svg/0.1
```

This is a draft testing identifier, not a registered endpoint or a service URL controlled by this project. Tools MUST compare elements using the complete namespace URI and local name, MUST NOT depend on the example prefix `m`, and MUST NOT issue network requests to resolve the namespace.

The root MUST contain exactly one `title`, one `desc`, one `metadata`, and one `g`, in that order, and no other child elements. The root MUST have `version="1.1"`, `width`, `height`, and `viewBox`. Dimensions and other attributes follow Clause 7. `title` and `desc` MUST contain nonempty plain text describing the document. This is a minimum descriptive requirement, not accessibility certification.

Indentation whitespace MAY occur between elements except inside `m:source`; other non-whitespace character data MUST NOT occur in element-only containers. Comments MAY occur outside the source and have no normative meaning. Processing instructions other than the XML declaration, DOCTYPE declarations, and custom entity declarations MUST NOT occur.

### 5.2 Document Metadata

`svg:metadata` MUST contain only one `m:document`. `m:document` MUST contain `m:source`, `m:presentation`, optional `m:bindings`, and optional `m:extensions` in that order, each at most once. Attributes on MISVG elements are unqualified except the explicitly specified `xml:space`.

| `m:document` attribute | Requirement | Definition |
|---|---|---|
| `version` | MUST | Exactly `0.1`; distinct from the specification draft revision. |
| `profile` | MUST | Exactly `static`. |
| `doc-id` | MUST | Lowercase `urn:uuid:` followed by a UUIDv4 conforming to [UUID]; see Annex A. |
| `revision` | MUST | Decimal integer from 1 through 9007199254740991, without leading zeros. |

### 5.3 Source Element

| `m:source` attribute | Requirement | Definition |
|---|---|---|
| `media-type` | MUST | Exactly `text/markdown`, according to [MDTYPE]. |
| `dialect` | MUST | Exactly `commonmark-0.31.2`; a MISVG token, not an IANA variant registration. |
| `xml:space` | MUST | Exactly `preserve`. |

`m:source` MUST contain only text and/or CDATA, with no child elements, comments, or processing instructions. Its content MAY be empty. `xml:space` does not disable XML line-ending normalization.

### 5.4 Presentation Descriptor

`m:presentation` MUST be an empty element with these attributes:

| Attribute | Definition |
|---|---|
| `root-ref` | The view `g` ID, a bare ID without `#`. |
| `source-digest` | `sha256:` followed by 64 lowercase hexadecimal characters. |
| `renderer` | Nonempty renderer name, 1–128 Unicode code points. |
| `renderer-version` | Nonempty renderer version, 1–64 Unicode code points; SemVer is not required. |

Renderer identity is diagnostic information and MUST NOT be treated as proof of a trusted origin. Matching renderer names and versions do not guarantee identical pixels. `root-ref` MUST reference the unique `g` directly under the root.

### 5.5 Closed Core Vocabulary

Core MISVG elements MUST NOT contain undefined attributes or child elements. Unknown core vocabulary MUST be treated as invalid and cannot pass this version's validation by being ignored. External extensions are admitted only through `m:extensions` under Clause 10.

## 6. Markdown and Character Handling

### 6.1 Normalized Source

On import, a Producer MUST normalize CRLF and standalone CR to LF. Apart from that conversion, it MUST preserve all source characters, including trailing spaces, tabs, blank lines, the presence or absence of a final LF, and Unicode composition forms. It MUST NOT automatically trim, append a final newline, or apply NFC/NFD.

A Reader MUST use the character sequence after XML parsing. Under [XML], physical line endings are normalized first; U+000D introduced by `&#13;` is not removed by that step. If any U+000D occurs in the parsed source, a Reader MUST reject conformance and report `E_SOURCE`, rather than silently repair it and claim the original file is valid.

Characters prohibited by XML 1.0, such as U+0000, MUST cause import failure; a Producer MUST NOT silently delete them. A file-leading BOM is not source content. U+FEFF inside the source is ordinary data and MUST be preserved.

### 6.2 Markdown Semantics

The source MUST be parsed according to [CM]. GFM tables, strikethrough, task lists, YAML front matter, mathematics, Mermaid execution, and include directives are not extension syntax in this version. Tools MUST NOT silently apply a meaning-changing dialect while claiming core 0.1 rendering.

CommonMark raw HTML nodes MUST be rendered as visible text containing their original markup and MUST NOT execute as active HTML. Code blocks MUST be treated as text and MUST NOT be executed. Ordinary links MUST show their labels and immediately follow them with visible text of the resolved destination; an autolink already displaying its destination need not repeat it. Images MUST be represented by visible alternative text and destination text; if alternative text is empty, use the fixed string `[image]`. These are static output rules for this profile; parsing still follows CommonMark.

Link destinations are data only. A Producer or Reader MUST NOT access them automatically during parsing or rendering. Relative paths in the source MUST be preserved and displayed as written, without automatic resolution against the document path or `xml:base`.

### 6.3 XML Escaping and Round Trips

A Producer MAY use XML text escaping or CDATA; both MUST yield the same source after extraction. If the source contains `]]>`, a Producer using CDATA MUST split the section, for example using `]]]]><![CDATA[>` for that sequence, or use ordinary XML text escaping. Hashing MUST occur after XML decoding, not over CDATA tags or the literal spelling `&amp;`.

Lossless extraction means preservation of the normalized source character sequence. It does not promise reconstruction of an original `.md` file's BOM, CRLF bytes, XML prefixes, or attribute ordering.

## 7. Static Rendering Profile

### 7.1 Element Allowlist

The following restrictions define a closed subset of [SVG11]. Elements, attributes, and namespaces not allowed here MUST NOT occur in the view.

| Location / element | Children |
|---|---|
| Root `svg` | Only the four children in 5.1. |
| View `g` and nested `g` | `g`, `text`, `rect`, `circle`, `ellipse`, `line`, `polyline`, `polygon`, `path`. |
| `text`, `tspan` | Text and `tspan`. |
| Geometric shapes | No child elements. |

`foreignObject`, `script`, `style`, `image`, `a`, `use`, `defs`, filters, animation, and external fonts are outside this profile. A Producer MUST NOT replace document content text with paths. Pure decoration or arrows MAY use paths.

### 7.2 Attribute Allowlist

All attributes are unqualified; namespace declarations do not count as attributes. All view elements other than the root `svg` MAY have `id`. The root allows only `version`, `width`, `height`, and `viewBox`.

| Element | Allowed attributes, in addition to `id` |
|---|---|
| `g` | `transform` and the common presentation attributes below. |
| `text`, `tspan` | `x`, `y`, `dx`, `dy`, and common presentation attributes; `text` additionally allows `transform` and `xml:space="preserve"`. |
| `rect` | `x`, `y`, `width`, `height`, `rx`, `ry`, `transform`, and common presentation attributes. |
| `circle` | `cx`, `cy`, `r`, `transform`, and common presentation attributes. |
| `ellipse` | `cx`, `cy`, `rx`, `ry`, `transform`, and common presentation attributes. |
| `line` | `x1`, `y1`, `x2`, `y2`, `transform`, and common presentation attributes. |
| `polyline`, `polygon` | `points`, `transform`, and common presentation attributes. |
| `path` | `d`, `transform`, and common presentation attributes. |

The common presentation attributes are limited to `fill`, `stroke`, `stroke-width`, `stroke-linecap`, `stroke-linejoin`, `font-family`, `font-size`, `font-weight`, `font-style`, and `text-anchor`. There is no other CSS entry point.

`fill` and `stroke` allow only `none` or `#RRGGBB`, with either hexadecimal case. `font-family` is a comma-separated list of nonempty names; each name contains only Unicode letters, decimal digits, ASCII spaces, and hyphens, with no quotes, parentheses, or escapes. It MUST end with one of `sans-serif`, `serif`, or `monospace`. Other enumerated values follow [SVG11]; `font-weight` is limited to `normal`, `bold`, or multiples of 100 from `100` through `900`; `font-style` is limited to `normal`, `italic`, or `oblique`.

### 7.3 Geometry and Canvas

Root `width` and `height` MUST be unitless decimal integers from 1 through 16384 without leading zeros; their product MUST NOT exceed 16777216. `viewBox` MUST express the four numeric values `0 0 width height`. Other lengths MUST be finite, unitless SVG numbers; font-size MUST be positive; stroke-width, dimensions, and radii MUST be nonnegative. In this version, `x`, `y`, `dx`, and `dy` on text/tspan allow only a single number. Percentages, units, CSS variables, `calc()`, and nonfinite values are not allowed.

The grammars of `d`, `points`, and `transform` follow [SVG11], and all numeric values MUST be finite. `path` MUST have nonempty valid `d`; `polyline` and `polygon` MUST have valid `points`. Defaults, drawing order, and presentation attribute inheritance follow [SVG11].

A Producer MUST place visible text within the canvas, avoiding clipping, overlapping text, or illegible foreground/background combinations. If fonts cannot cover the source language, the Producer MUST report a rendering limitation and cannot treat missing-glyph boxes as success. Exact font metrics and pixel alignment are not cross-implementation conformance requirements.

### 7.4 Text and Reading Order

The XML order of the view SHOULD follow a reasonable reading order. Content text MUST use `text`/`tspan`. A Producer SHOULD use appropriate line breaks and styling for headings, paragraphs, lists, quotations, emphasis, and code; it must not depend on scripts for initial layout. Retaining the complete source does not automatically satisfy screen-reader or WCAG requirements.

## 8. Digests, Synchronization, and Editing Transactions

### 8.1 Digest Algorithm

`source-digest` MUST be produced as follows:

1. Use a secure XML parser to obtain all text/CDATA characters in `m:source`, concatenated in document order.
2. Check Clause 6; do not remove whitespace or append LF.
3. Encode the sequence as UTF-8 without a BOM.
4. Compute SHA-256 according to [SHA256] and encode it as 64 lowercase hexadecimal characters.
5. Prepend the ASCII string `sha256:`.

```text
source_digest = "sha256:" + lower_hex(SHA256(UTF8(source)))
```

The digest covers only the source, excluding document ID, revision, renderer, bindings, extensions, and SVG. No circular digest or XML canonicalization is required. Layout-only changes leave the digest unchanged.

### 8.2 Binding Status

A Reader MUST compare the computed value with the declared value. A mismatch MUST produce `E_DIGEST_MISMATCH`. A Reader MAY extract the source in an unvalidated recovery mode but MUST NOT claim the package is valid.

A match permits only the report `source-binding=matched`. Tools MUST NOT call this a valid signature, authenticated authorship, verified view, or trusted/safe content. Even with a matching digest, the view may have been independently changed, or an attacker may have changed both source and digest.

### 8.3 Atomic Updates

For each committed change, an Editor MUST:

1. Record SHA-256 of the original complete file bytes as a local precondition. This transaction fingerprint is not stored in the format.
2. Modify source and/or layout according to user intent and regenerate the view and bindings as needed.
3. Retain the `doc-id` and increment `revision` by 1; refuse the commit at the maximum revision value.
4. Update `source-digest` and validate the candidate. Updating only the digest to hide a stale view is prohibited.
5. Before writing, verify that the precondition still holds under a lock or storage-side compare-and-swap mechanism.
6. Commit by atomic replacement or a transaction without an observable intermediate state. On failure, preserve the original.

Only a result whose precondition holds may overwrite the original; otherwise the Editor MUST report `E_CONFLICT`. An unlocked check followed by a write does not satisfy this clause. Equal revisions do not imply equal files; an Editor MUST NOT detect conflicts using revision alone.

A tool merely reserializing XML without changing source, presentation, bindings, or metadata MAY retain revision. A newly created document MUST begin at revision 1. A copy made into an independent document MUST receive a new UUIDv4 according to [UUID] and cannot reuse the example UUID. Moving a file or making a backup is not creating an independent document.

### 8.4 Merging and Recovery

Implementations SHOULD perform a three-way merge of source and then regenerate the view. They MUST NOT treat a successful Git XML text merge as a successful semantic merge. A candidate containing unresolved source conflict markers MUST NOT be committed as a completed edit. If the markers are already intentional discussion content, an implementation MAY preserve them based on explicit context.

If the source is lost or cannot be extracted, what remains is ordinary SVG and MUST NOT be claimed as valid MISVG. Repair MUST produce a distinguishable new result and MUST NOT silently modify the input file.

## 9. Source Bindings

`m:bindings` MAY be omitted. If present, it MUST contain one or more empty `m:bind` elements. Every bind MUST have `target`, `start-line`, and `end-line`, and no other attributes.

`target` MUST be the bare ID of an existing view element and MUST occur at most once among bindings. All view IDs MUST be unique and conform to the ID grammar in Annex A. The view root `g` MUST have an ID. Multiple targets MAY map to the same source range.

Ranges are **one-based and inclusive at both ends**. Split the source on LF; if its last character is LF, remove the final terminating empty split fragment. The empty source has zero lines. Thus `"a\n"` has 1 line, `"a\n\n"` has 2, and `"\n"` has 1. The constraint `1 ≤ start-line ≤ end-line ≤ line count` MUST hold.

An empty source MUST have no bindings. Bindings need not cover every source line and do not prove complete rendering. After source changes, an Editor MUST recompute affected bindings or remove all bindings and MUST NOT retain known-stale line numbers. IDs SHOULD remain stable when a visual component's meaning has not changed.

## 10. Extensions, Versions, and Preservation

### 10.1 Version Negotiation

A Reader MUST explicitly compare version, namespace, and profile. A Reader supporting only 0.1 that receives 0.2, 1.0, another namespace, or a non-`static` profile MUST report `E_UNSUPPORTED` rather than guess compatibility. It may recover data in an unvalidated recovery mode but MUST state its support limits.

No compatibility is promised between 0.x versions. Specification revision `0.1.1` MAY be an editorial revision without a wire-format change. Adding mandatory fields or changing digest or content semantics MUST use a new wire version and namespace.

### 10.2 Optional Extensions

`m:extensions` MAY contain one or more elements in external namespaces. A top-level extension namespace MUST be nonempty and MUST NOT be the SVG, MISVG, or XML namespace. SVG and MISVG elements MUST NOT occur anywhere in the extension subtree. Extension text and attributes are inert data and cannot require code execution.

Extensions may carry only ignorable supplementary metadata. They MUST NOT change core source authority, interpretation, security requirements, or view-generation semantics. A feature that would cause content to be misunderstood if ignored needs a separately specified profile/version; it cannot be placed in this optional extension mechanism.

A Reader MAY ignore unknown extensions but MUST retain the core source interpretation. For a round trip with no content change, an Editor MUST preserve unknown extension element and attribute expanded names, string values, child-node order, and text. Prefixes, attribute order, and CDATA boundaries need not be preserved.

If an Editor cannot determine whether an unknown extension remains valid after an edit, it MUST abort ordinary saving and report `E_EXTENSION_EDIT`, or save a separate result through an explicit “remove unknown extensions” operation. It cannot preserve an unknown stale digest or line range and claim synchronization. Only an explicit removal choice by the user or caller permits discarding such extensions.

## 11. Conformance and Interoperability

### 11.1 Document Conformance

A document claiming `MISVG 0.1 static` MUST satisfy every applicable MUST/MUST NOT in Clauses 4–10 and Annex A. Passing an XML Schema is one item of structural evidence and cannot replace source digest, reference, SVG subset, semantic, or visual checks.

### 11.2 Role Conformance

| Role | Required capabilities |
|---|---|
| Reader | Secure parsing; core structure/version recognition; lossless source extraction; digest checks; error and limitation reporting. An unchecked view cannot be called verified. |
| Producer | Conforming container and static profile; content/text preservation; digest and renderer metadata; content-fidelity and visual checks. |
| Editor | Reader and Producer requirements plus atomic updates, conflicts, revision, bindings, and unknown-extension handling. |
| Validator | Explicit check scope and reports under 11.3; partial checks cannot be presented as full conformance. |

### 11.3 Validation Dimensions

A Validator MUST report separately:

- `structure`: XML, metadata, fields, uniqueness, and references.
- `source-binding`: source rules, digest, and line ranges.
- `static-profile`: all elements, attributes, value ranges, and underlying SVG grammar.
- `content-fidelity`: preservation of the same substantive content in source and view.
- `visual-review`: rendered text, reading order, clipping, overlap, and missing glyphs.

Each status MUST be `pass`, `fail`, `not-checked`, or `unsupported`. A check not performed MUST be `not-checked`, never pass. Digest success implies no other dimension's success. A full conformance claim MUST have evidence of success in all five dimensions; the final two MAY involve human review.

### 11.4 Interoperability Verification

Implementations claiming role conformance MUST execute applicable Annex B cases and record results. Release testing for Producers and Editors SHOULD include two independent SVG renderers and cross-tool extraction/repackaging. Passing only this project's bundled example does not constitute general interoperability certification.

### 11.5 Resource Limits

Implementations MUST set publishable limits on file size, source size, XML depth, node count, string length, graphics complexity, and processing time. Initial deployments SHOULD use 8 MiB per file, 1 MiB of source, depth 64, 50000 nodes, and 65536 characters per path. These are implementation recommendations, not format validity ceilings. A stop due to limits MUST report `E_LIMIT`/`unsupported` and cannot establish that the input is malformed.

## 12. Error Handling

| Code | Meaning / minimum behavior |
|---|---|
| `E_XML` | Malformed XML, unsupported encoding, or prohibited declaration; stop normal parsing. |
| `E_STRUCTURE` | Invalid required field, order, cardinality, type, or core vocabulary. |
| `E_UNSUPPORTED` | Unsupported version, namespace, dialect, or profile; do not guess. |
| `E_SOURCE` | Source character/node rule violation. |
| `E_DIGEST_MISMATCH` | Computed and declared digests differ. |
| `E_REFERENCE` | Duplicate ID, invalid root-ref/target, or invalid line range. |
| `E_PROFILE` | Static element, attribute, or value restriction violation. |
| `E_CONTENT` | View omits, changes, or adds substantive content. |
| `E_VISUAL` | Observed clipping, overlap, missing glyphs, or unreadability. |
| `E_CONFLICT` | Original file changed; do not overwrite. |
| `E_EXTENSION_EDIT` | Unknown extension cannot safely be updated or preserved. |
| `E_LIMIT` | Published processing limit exceeded; not proof of format invalidity. |

When multiple errors coexist, an implementation MAY report the first or all, but MUST NOT execute dangerous content to obtain more diagnostics. Diagnostics SHOULD include an element path, field, or source line. They MUST NOT send the complete source, secrets, or full local paths to external services by default.

## 13. Security and Privacy Considerations

### 13.1 XML and Active Content

All processors MUST disable external entities, DTD loading, network schema resolution, and XInclude expansion. They MUST check untrusted input before introducing it into a DOM, browser, or other executable environment; displaying active SVG before sanitization is prohibited. CDATA is a string container, not a sanitizer.

The static allowlist excludes event attributes, scripts, CSS `url()`, external resources, and external HTML. Source HTML, JavaScript, links, and instructions MUST remain data. Tools MUST limit resource use and stop affected processing on error.

### 13.2 AI Trust Boundary

Markdown, comments, extensions, and renderer names are untrusted document data. A receiver MUST NOT elevate their privileges because they claim to be “system instructions,” tool calls, upload requests, or permission declarations. An application sending a document to an AI MUST distinguish user authorization from document content. Source-driven code execution, network access, and file operations are outside MISVG parsing.

### 13.3 Privacy and Hidden Content

Content absent from the visible view may still exist in source or metadata. Publication tools MUST permit inspection of complete source and metadata and MUST NOT treat visual masking as deletion. Removing sensitive information MUST cover source, view, bindings, and extensions. A new public derivative document SHOULD receive a new doc-id.

### 13.4 Integrity and Authenticity

An unkeyed SHA-256 digest cannot authenticate authors or prevent an attacker from rewriting both content and digest. This version defines no digital signature, trust root, timestamp, or revocation mechanism. Implementations MUST NOT claim that `source-digest` provides these guarantees.

## 14. IANA and Identifier Considerations

This draft requests no new IANA registration. The outer media type MUST be `image/svg+xml` from [SVG11]. The embedded source is described with `text/markdown` from [MDTYPE]; no new media type or registered Markdown variant is introduced.

Filenames SHOULD use `.misvg.svg` for recognition; ordinary `.svg` is also valid. Filenames do not replace namespace and structure detection. Tools MUST NOT present the unregistered `application/misvg` as this specification's official media type.

The namespace is the draft identifier in 5.1. Before formal publication, maintainers MUST choose a sustainably governed namespace and define migration. Changing its URI does not automatically upgrade old files. IEEE, IETF, or W3C identifiers cannot be used without authorization as official registration marks for this specification.

## 15. Version Governance and Change Management

Publishers MUST track specification draft revision, wire version, and individual document revision separately. Errata MUST identify affected clauses and interoperability impact. A change to wire semantics MUST use a new wire version.

Before moving from 0.x to stable 1.0, maintainers SHOULD fix namespace governance and licensing, exchange documents between at least two independent Reader/Producer implementations, test characters and conflicts, review the threat model, and establish a formal compatibility policy. Future `html` profiles, diagram relationship models, resource packaging, style resources, and signatures SHOULD be separate proposals rather than unversioned changes to static.

## Annex A (normative): Lexical and Structural Constraints

The following regular expressions MUST match the whole string. Character ranges are ASCII unless stated otherwise.

```text
ID        = [A-Za-z][A-Za-z0-9._-]{0,63}
DIGEST    = sha256:[0-9a-f]{64}
POSINT    = [1-9][0-9]*
UUID4URN  = urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}
```

POSINT remains subject to each field's range. Element cardinality is:

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

`schema/misvg-metadata-0.1.xsd` is a helper schema for the metadata subtree, not the entire SVG. It does not cover every lexical detail, source digests, references, SVG value ranges, resource security, or visual requirements. XSD success alone cannot establish conformance.

## Annex B (normative): Conformance Test Requirements

Implementations MUST cover applicable cases for their roles. “Valid” assumes all other conditions hold. After mutating a sample, tests MUST recompute its digest unless specifically testing a mismatch, to avoid masking the intended failure.

| ID | Input / operation | Expected result | Roles |
|---|---|---|---|
| T01 | Complete valid example | Exact extraction, matching digest, readable rendering. | All |
| T02 | Replace `m` prefix, retain URI | Equally valid; prefix-independent result. | R/P/E/V |
| T03 | Equivalent CDATA and XML escaping | Identical extracted text and digest. | R/P/E/V |
| T04 | Source contains `]]>`, `&`, `<` | Safe serialization and round trip. | R/P/E/V |
| T05 | Source `abc`, no LF | `sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`. | R/P/E/V |
| T06 | Empty source | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; no bindings. | R/P/E/V |
| T07 | Append LF to `abc` | Different digest; no trimming. | R/P/E/V |
| T08 | Physical CRLF versus LF in XML source | Equivalent after XML decoding; same digest. | R/E/V |
| T09 | `&#13;` in source | `E_SOURCE`. | R/E/V |
| T10 | `é` versus `e` + U+0301 | Distinct bytes preserved; distinct digests. | R/P/E/V |
| T11 | Change source, retain digest | `E_DIGEST_MISMATCH`; no synchronization claim. | R/E/V |
| T12 | Change view text only | Digest may match; fidelity fails. Digest-only tools report fidelity not checked. | P/E/V |
| T13 | Second source/document or unknown core attribute | `E_STRUCTURE`. | R/E/V |
| T14 | Duplicate view IDs, invalid root-ref/target, out-of-range lines | `E_REFERENCE`. | R/E/V |
| T15 | Source child element or comment | `E_SOURCE` or `E_STRUCTURE`. | R/E/V |
| T16 | DOCTYPE, external entity, processing instruction | Reject; no external network/file reads. | R/E/V |
| T17 | Script, event attribute, foreignObject, style, href, data URI, URL paint | `E_PROFILE`; no prior execution/loading. | P/E/V |
| T18 | Unknown version/profile/dialect | `E_UNSUPPORTED`; do not assume compatibility. | R/E/V |
| T19 | Reader encounters unknown inert extension | May ignore; core interpretation unchanged; no execution. | R/V |
| T20 | Edit source with unknown extension | `E_EXTENSION_EDIT`, or explicitly chosen removal and separate save. | E |
| T21 | File changes after reading, even at same revision | `E_CONFLICT`; preserve original. | E |
| T22 | Interrupted commit / simulated write failure | Existing file intact; no partial output exposed. | E |
| T23 | Content text becomes paths; clipping or missing glyphs | Profile/visual-review or content-fidelity fails. | P/E/V |
| T24 | Published processing limits exceeded | `E_LIMIT`/unsupported, not necessarily invalid. | R/P/E/V |
| T25 | Remove metadata, leave SVG | May be ordinary SVG; not MISVG. | R/E/V |
| T26 | Images, raw HTML, code, relative links in source | Static output under 6.2; no automatic request/execution. | P/E |
| T27 | Line counts for empty source, trailing LF, consecutive LF | Clause 9; no nonexistent lines may be bound. | R/P/E/V |
| T28 | File BOM versus source U+FEFF | Accept former; preserve and hash latter. | R/E/V |
| T29 | Reserialize XML without content change | Preserve source, digest, extension semantics; revision may stay. | E |
| T30 | Canvas bounds, nonfinite number, invalid path/transform | static-profile fails. | P/E/V |

R/P/E/V mean Reader, Producer, Editor, and Validator. Validator applicability is limited to its declared scope, but unchecked dimensions MUST be reported.

## Annex C (informative): Complete Example and Workflow

The default English example is `examples/order-flow.en.misvg.svg`, with extracted comparison source `examples/order-flow.en.md`. Japanese and Traditional Chinese counterparts use `.ja` and `.zh-Hant`. `examples/order-flow.misvg.svg` and `.md` remain the original Traditional Chinese fixture for compatibility. Example UUIDs are for testing and should not be reused for new documents.

```text
# Order workflow

1. The customer completes payment.
2. The warehouse confirms successful payment, then arranges shipment.

Rule: Do not ship if payment has not succeeded.
```

Normal workflow: secure read → source extraction → binding checks → Markdown edit → view generation → line bindings and digest update → content and rendering checks → atomic commit. Layout changes also increment revision; unchanged source keeps its digest.

A minimal Python digest illustration:

```python
import hashlib

def source_digest(parsed_source: str) -> str:
    if "\r" in parsed_source:
        raise ValueError("E_SOURCE")
    return "sha256:" + hashlib.sha256(
        parsed_source.encode("utf-8")
    ).hexdigest()
```

This function does not handle secure XML parsing or validate the view. The example views are manually laid out from their sources; this package does not provide a general Markdown layout engine.

## Annex D (informative): Design Rationale and Tradeoffs

| Decision | Rationale and cost |
|---|---|
| Markdown as sole content authority | Avoids competing sources; drag-and-edit changes need an explicit write-back workflow. |
| SVG metadata | Carries source in the same file without rendering it; drawing/optimization tools may remove it. |
| Native static SVG subset | Reduces external dependencies and active content; no direct HTML tables, images, or full CSS. |
| Fixed CommonMark edition | Prevents dialect drift; GFM/Mermaid require a separate extension or version. |
| Hash source only | Simple, reproducible, no self-reference; no view integrity or signature guarantee. |
| Optional line bindings | Easy to implement and debug; not AST identity or arbitrary bidirectional editing. |
| Closed core vocabulary | Detects typos and version differences; new core capabilities require versioning. |
| No pixel identity claim | Fonts, platforms, and engines affect output; separate visual checks are necessary. |

The first version deliberately keeps interchange small. For long documents and complex tables, Markdown/HTML with SVG illustrations may remain more appropriate. This format serves cases where one graphic must retain its editable source.

## Annex E (informative): Editorial Basis and Further References

- [RFC 7322, RFC Style Guide](https://www.rfc-editor.org/rfc/rfc7322.html): abstract, status, clause cross-references, reference classification, and security organization; not every formatting rule is implemented here.
- [IEEE SA Standards Style Manual, 2021](https://development.standards.ieee.org/myproject/Public/mytools/draft/styleman.pdf): overview/references/definitions order, verifiable requirements, and separation of normative and informative annexes.
- [IEEE SA — Drafting the Standard](https://standards.ieee.org/develop/drafting-standard/): formal IEEE drafts follow that process and its templates; this draft has not undergone it.
- [RFC 2606, Reserved Top Level DNS Names](https://www.rfc-editor.org/rfc/rfc2606.html): example domains; example.org indicates that formal namespace governance is not established.
- [SVG 1.1 Metadata](https://www.w3.org/TR/2011/REC-SVG11-20110816/metadata.html): SVG supports metadata in other XML namespaces; this draft newly defines the MISVG data model.

## Annex F (informative): Deliverables and Implementation Boundaries

| Attachment | Purpose / boundary |
|---|---|
| `MISVG-0.1.en.md`, `.zh-Hant.md`, `.ja.md` | Maintainable full specification texts; English is default and authoritative. |
| `index.html`, `MISVG-0.1.en.html` | English default entry and offline reading edition. |
| `MISVG-0.1.zh-Hant.html`, `MISVG-0.1.ja.html` | Offline translations with language navigation. |
| `schema/misvg-metadata-0.1.xsd` | Metadata subtree structure; not full SVG/security validation. |
| `examples/order-flow.{en,zh-Hant,ja}.misvg.svg` | Localized examples with matching source, actual digests, and line bindings. |
| `examples/order-flow.{en,zh-Hant,ja}.md` | Extraction comparison texts, not second authoritative sources. |
| `examples/order-flow.misvg.svg`, `.md` | Original Traditional Chinese compatibility fixture. |
| `tests/hash-vectors.json` | UTF-8 digest and line-count vectors. |
| `tests/check_package.py` | Package consistency and selected negative tests; not certification. |
| `tests/verification-report.json` | Executed package tests and unchecked dimensions. |
| `tests/render-checks.json`, `tests/visual-review.md` | Original single-Chromium bounds checks and visual review record. |
| `tests/localization-report.json` | Translation structure, identifiers, examples, and navigation checks. |
| `tests/localization-render-checks.json` | Multilingual desktop/mobile layout measurements. |
| `README.md`, `README.zh-Hant.md`, `README.ja.md` | English default instructions and translated companion instructions. |

Full role testing under Annex B requires additional test tooling and an actual editor. Bundled checks do not cover complete SVG grammar, all CommonMark rendering, concurrent transactions, or cross-renderer interoperability; passing them does not establish a complete implementation.
