# Requirements: ML Pipeline to Predict Order Revenue

**Date:** 2026-06-22
**Status:** Ready for implementation

## Problem

There's a request to apply machine learning to the sales data, covering the standard pipeline steps end to end, with a clear verdict at the end on how good the resulting model is.

## What we're building

A Python script (`predict_sales.py`) that predicts **per-order revenue** from `data/orders.csv` using order attributes available before the price is known, runs the full standard ML pipeline, and prints a final report with metrics and a plain-language quality verdict.

## Scope

**Prediction target:** Revenue per order line (`quantity × unit_price`), predicted from features that do **not** include `unit_price`. Including `unit_price` would make the task a restatement of the multiplication formula rather than a genuine prediction problem — this was explicitly decided against.

**Features used:** `category`, `quantity`, date-derived features (month, day of week) from `order_date`, and `product_id` (frequency-encoded). `order_id` and `customer_id` are excluded as non-predictive identifiers.

**Pipeline steps (in scope):**
1. Missing data check and handling
2. Exploratory data analysis (distributions, revenue by category/month, correlations)
3. Feature engineering (date parts, product frequency encoding, category encoding)
4. Feature selection (drop identifiers; review feature importance)
5. Standardization/normalization of numeric features
6. Train/test split
7. Model training: Linear Regression baseline **and** Random Forest, both evaluated for comparison
8. Metrics: RMSE, MAE, R² on the held-out test set
9. Closing verdict: plain-language assessment of whether the model is good enough to trust, based on the metrics and the baseline comparison

**Deferred / out of scope:**
- Forecasting future monthly totals — ruled out; only 12 monthly data points exist, too few for a reliable time-series model
- Hyperparameter tuning beyond reasonable defaults
- Model deployment or serving — this is a one-time analysis script, not a service
- Cross-validation — a single train/test split is sufficient unless results look unstable

## Key assumptions

- "Predicting sales" means predicting revenue at the order-line level, not forecasting aggregate future revenue
- A single baseline-vs-comparison-model setup (not full model search) is sufficient to answer "how good is it"

## Data grounding

Same dataset as prior deliverables: `data/orders.csv`, 4,644 order line items, Jul 2024–Jun 2025, 6 categories, 60 products, 1,093 customers, no missing-value or data-quality issues found in prior analysis.

## Success criteria

- Script runs end to end on `data/orders.csv` without errors
- Final printed report includes RMSE, MAE, R² for both the baseline and the comparison model
- Report ends with a clear, plain-language statement of model quality (e.g., "explains X% of revenue variance, error of roughly $Y per order — [good/moderate/weak] for this use case")
