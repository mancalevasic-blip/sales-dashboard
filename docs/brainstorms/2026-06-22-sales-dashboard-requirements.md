# Requirements: Sales Dashboard for Management

**Date:** 2026-06-22
**Status:** Ready for implementation

## Problem

A static Quarto report (`monthly_sales_report.qmd`, rendered to HTML/PDF) already covers monthly revenue, AOV, and seasonality analysis. The content is fine, but it isn't convenient for non-technical managers to open, browse, or check on their own — there's no easy way to share or self-serve it.

## What we're building

A public, no-login Streamlit dashboard that reads `data/orders.csv` (4,644 orders, Jul 2024–Jun 2025, 6 categories, 60 products, 1,093 customers) and is deployed to Streamlit Community Cloud with a shareable URL.

## Scope

**In scope:**
- KPI cards: total revenue, total orders, AOV, best month
- Revenue-by-month trend chart, with the existing seasonality narrative (Dec peak driven by order volume not AOV, Jan pullback, steady recovery) carried over as a short caption
- Category breakdown: revenue / orders / AOV by category (6 categories)
- Sidebar filters: category, date range
- Deployment to Streamlit Community Cloud, public URL, no authentication

**Deferred / out of scope:**
- Product-level and customer-level drill-down — not requested
- Live or recurring data refresh — this is a one-time snapshot of the current CSV; no plan to update `orders.csv` going forward
- Authentication / access gating — explicitly confirmed acceptable as public

## Layout decision

Single page with sidebar filters (KPI cards → trend chart → category breakdown), rather than a multi-tab layout. Chosen because the requested scope (KPIs + category drill-down only) doesn't need separate screens, and a single view has lower carrying cost.

## Key assumptions

- "Management" needs self-serve access to existing analysis, not new analytical findings — the `.qmd` report's narrative (seasonality, AOV stability) is the analytical content; this dashboard's job is access, not new analysis.
- Streamlit Community Cloud's free tier is sufficient for a single small CSV-backed app.
- Sales figures (revenue, order counts) are not sensitive enough to require gating — confirmed by the user.

## Data grounding

- `data/orders.csv`: columns `order_id, order_date, customer_id, product_id, product_name, category, quantity, unit_price`
- 4,644 orders, Jul 2024–Jun 2025, 6 categories (Beauty, Electronics, Home & Kitchen, Office, Sports & Outdoor, Toys), 60 products, 1,093 customers
- No discount/return/refund columns — revenue is gross (`quantity × unit_price`), matching the existing report's stated limitation

## Success criteria

- Dashboard is live at a public Streamlit Cloud URL
- KPI cards and charts match the figures already validated in `monthly_sales_report.qmd` (e.g. total revenue, Dec 2024 peak, Jan 2025 dip)
- A manager can filter by category and date range without needing to ask anyone for help
