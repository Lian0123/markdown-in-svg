# Markdown-in-SVG 0.1 — Trilingual Specification

**Default and authoritative language: English.** [English](MISVG-0.1.en.html) · [繁體中文](MISVG-0.1.zh-Hant.html) · [日本語](MISVG-0.1.ja.html)

MISVG-SPEC-0001 revision 0.1.1 / Draft 02 contains full English, Traditional Chinese, and Japanese editions. Open `index.html` for the default English reading edition; each edition provides language navigation. `MISVG-0.1.md` is the default English Markdown copy. Edit the language-specific Markdown files and regenerate the publication.

This independent draft follows an IEEE-style technical structure and RFC requirement language. It has not been approved by IEEE or IETF. English governs translation discrepancies. The wire version remains `0.1`; language selection does not change the format or requirements.

## Contents

- Full specification: 15 main clauses, 6 annexes, 30 conformance test requirements.
- Offline HTML and editable Markdown in all three languages.
- Metadata XML Schema, digest vectors, and selected package checks.
- Localized SVG examples and matching extraction comparison files under `examples/`.
- Default example: `examples/order-flow.en.misvg.svg`. The unsuffixed example remains the original Traditional Chinese compatibility fixture.

## Build and check

Requires Python 3, `markdown`, and `lxml`. No network access is required. From this directory:

```sh
python3 scripts/build_publication.py
python3 tests/check_package.py
python3 tests/check_localization.py
```

The first command regenerates HTML, English default entry points, and localized examples. The other commands regenerate `tests/verification-report.json` and `tests/localization-report.json`. Structural translation checks do not prove semantic equivalence; all translations retain the same clause numbers, requirement levels, technical tokens, and test identifiers for review.

The package checker is not a complete MISVG validator, Markdown layout engine, or editor. It does not cover full SVG attribute grammar, all CommonMark output, atomic editing, or cross-renderer interoperability. The 36 original package checks passed; localization checks and multilingual layout results are recorded separately. Original and multilingual rendering reports are under `tests/`.

## Design and publication status

Markdown is the sole authority for document content; SVG is its presentation. A matching digest does not verify the view, author, or signature. Example views are manually laid out from their sources; companion `.md` files are extraction comparisons, not second authoritative sources.

Only `static` is defined. HTML `foreignObject` layout, image resources, GFM/Mermaid execution, and signatures are not defined in this revision. The example.org namespace is a draft testing identifier; governance and migration must be decided before formal publication. No public license has been selected; the rights holder must decide before external publication.
