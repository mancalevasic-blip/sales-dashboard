# Requirements: Sales PowerPoint Deck for Leadership/Board

**Date:** 2026-06-22
**Status:** Ready for implementation

## Problem

Management/board reviews need a polished, self-contained sales summary they can present or read offline — not the interactive dashboard or the raw Quarto report. A static, board-appropriate deck is the expected format for this audience.

## What we're building

A ~9-slide `.pptx` file generated from `data/orders.csv`, in a light-editorial visual style (hero number + supporting stats), covering the same validated analysis already produced in `monthly_sales_report.qmd`.

## Scope

**In scope (slide-by-slide):**
1. Title slide
2. KPI summary — hero: total revenue; supporting: total orders, AOV, best month
3. Revenue trend — monthly revenue chart + seasonality caption
4. Seasonality narrative — Dec 2024 peak driven by order volume not AOV; Jan 2025 pullback; steady recovery
5. Category breakdown — revenue by category (6 categories)
6. Category detail — orders/AOV by category
7. Underlying growth — H2 2024 vs H1 2025 revenue comparison
8. Takeaways/conclusion
9. (Title/closing may combine with #1/#8 if content is light — slide count is a target, not a hard requirement)

**Visual style:** Light editorial — warm light background, large hero number leading the KPI slide, smaller supporting stat callouts elsewhere. Chosen by the user from a 3-option visual sketch (corporate blue, dark modern, light editorial); light editorial was selected.

**Deferred / out of scope:**
- Forward-looking projections or strategic recommendations — not in the existing data, not requested
- Speaker notes — add only if requested later
- Company branding/logo — no specification given; use a clean generic look

## Key assumptions

- Analytical content (figures, seasonality conclusions, growth comparison) is reused verbatim from `monthly_sales_report.qmd`, not re-derived or reinterpreted.
- This is a one-time deck generation, not tied to a recurring data refresh, consistent with `data/orders.csv` being a one-time snapshot (per `docs/brainstorms/2026-06-22-sales-dashboard-requirements.md`).
- Audience is leadership/board-level — tone is headline-driven and concise, not a full data dump.

## Data grounding

Same dataset as the existing dashboard and report: `data/orders.csv`, 4,644 orders, Jul 2024–Jun 2025, 6 categories, gross revenue (`quantity × unit_price`), no discount/return columns.

## Success criteria

- A `.pptx` file is produced that opens cleanly in PowerPoint/Keynote/Google Slides
- KPI and chart figures match the validated numbers from `monthly_sales_report.qmd` (e.g. Dec 2024 peak $97,138.60, total revenue $822,037.04)
- Deck reads coherently as a standalone leadership summary without needing the dashboard or report alongside it
