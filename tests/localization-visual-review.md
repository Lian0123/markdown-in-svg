# Multilingual publication visual review

Date: 2026-11-02. Renderer: Chromium through Playwright; one engine only.

English and Japanese specification pages were rendered and their desktop and mobile first-screen screenshots inspected. The language navigation, full titles, and document-control tables were readable. The Traditional Chinese edition was also rendered and measured; the original edition's visual record remains in `visual-review.md`.

All three reading editions measured exactly 1100 px at a 1100 px desktop viewport and 390 px at a 390 px mobile viewport, without horizontal overflow. All measured SVG text bounds remained within each 920 × 510 canvas. Details are in `localization-render-checks.json`.

English and Japanese example screenshots were inspected against their localized sources. The payment prerequisite, shipment sequence, and prohibition on shipment before successful payment were retained. English shipment text was moved below its step badge to provide clear separation. No text clipping or overlap was observed in the reviewed examples.

These checks cover the supplied examples and publication layout. They do not establish independent translation certification, page-by-page print layout, accessibility compliance, or cross-renderer interoperability.
