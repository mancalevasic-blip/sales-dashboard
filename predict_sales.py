"""End-to-end ML pipeline predicting per-order revenue from data/orders.csv.

Predicts revenue from order attributes available before price is known
(category, quantity, date, product) -- unit_price is deliberately excluded
since revenue = quantity * unit_price and including it would make this a
restatement of that formula rather than a genuine prediction problem.
"""

import json
from datetime import datetime, timezone

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = "data/orders.csv"
CHART_DIR = "charts"
import os

os.makedirs(CHART_DIR, exist_ok=True)

RANDOM_STATE = 42


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# 1. Load + missing data check
section("1. Missing Data Check")
df = pd.read_csv(DATA_PATH)
missing = df.isna().sum()
if missing.sum() == 0:
    print("No missing values found in any column.")
else:
    print(missing[missing > 0])
    df = df.dropna()
    print(f"Dropped rows with missing values. Remaining rows: {len(df)}")

df["order_date"] = pd.to_datetime(df["order_date"])
df["revenue"] = df["quantity"] * df["unit_price"]

# 2. EDA
section("2. Exploratory Data Analysis")
print(df[["quantity", "unit_price", "revenue"]].describe())
print("\nRevenue by category:")
print(df.groupby("category")["revenue"].agg(["mean", "sum", "count"]))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(df["revenue"], bins=40, color="#1f3a5f")
axes[0].set_title("Revenue distribution")
df.boxplot(column="revenue", by="category", ax=axes[1], rot=45)
axes[1].set_title("Revenue by category")
fig.tight_layout()
fig.savefig(f"{CHART_DIR}/eda.png", dpi=130)
plt.close(fig)
print(f"\nEDA charts saved to {CHART_DIR}/eda.png")

numeric_corr = df[["quantity", "unit_price", "revenue"]].corr()
print("\nNumeric correlation matrix:")
print(numeric_corr)

# 3. Feature engineering
section("3. Feature Engineering")
df["month"] = df["order_date"].dt.month
df["day_of_week"] = df["order_date"].dt.dayofweek
product_freq = df["product_id"].value_counts(normalize=True)
df["product_freq"] = df["product_id"].map(product_freq)
df = pd.get_dummies(df, columns=["category"], prefix="cat")
print("Engineered features: month, day_of_week, product_freq, one-hot category columns")

# 4. Feature selection
section("4. Feature Selection")
feature_cols = (
    ["quantity", "month", "day_of_week", "product_freq"]
    + [c for c in df.columns if c.startswith("cat_")]
)
print(f"Selected {len(feature_cols)} features (excludes order_id, customer_id, product_id, "
      f"product_name, order_date, unit_price -- unit_price excluded to avoid trivially "
      f"reconstructing revenue):")
print(feature_cols)

X = df[feature_cols]
y = df["revenue"]

# 5. Train/test split
section("5. Train/Test Split")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)
print(f"Train: {len(X_train)} rows, Test: {len(X_test)} rows")

# 6. Standardization/normalization
section("6. Standardization")
numeric_features = ["quantity", "month", "day_of_week", "product_freq"]
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[numeric_features] = scaler.fit_transform(X_train[numeric_features])
X_test_scaled[numeric_features] = scaler.transform(X_test[numeric_features])
print("Standardized numeric features (quantity, month, day_of_week, product_freq) to "
      "zero mean / unit variance using train-set statistics only.")

# 7. Model training: baseline vs comparison model
section("7. Model Training")


def evaluate(model, name, X_tr, X_te, y_tr, y_te):
    model.fit(X_tr, y_tr)
    preds = model.predict(X_te)
    rmse = float(np.sqrt(mean_squared_error(y_te, preds)))
    mae = float(mean_absolute_error(y_te, preds))
    r2 = float(r2_score(y_te, preds))
    print(f"\n{name}:")
    print(f"  RMSE: ${rmse:,.2f}")
    print(f"  MAE:  ${mae:,.2f}")
    print(f"  R2:   {r2:.3f}")
    return {"name": name, "rmse": rmse, "mae": mae, "r2": r2, "model": model}


baseline = evaluate(
    LinearRegression(), "Baseline: Linear Regression",
    X_train_scaled, X_test_scaled, y_train, y_test,
)
forest = evaluate(
    RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1),
    "Comparison: Random Forest",
    X_train, X_test, y_train, y_test,  # tree models don't need scaling
)

# 8. Metrics summary + feature importance
section("8. Metrics Summary")
print(f"{'Model':<30}{'RMSE':>12}{'MAE':>12}{'R2':>8}")
for r in (baseline, forest):
    print(f"{r['name']:<30}${r['rmse']:>10,.2f}${r['mae']:>10,.2f}{r['r2']:>8.3f}")

importances = pd.Series(forest["model"].feature_importances_, index=feature_cols).sort_values(
    ascending=False
)
print("\nRandom Forest feature importances:")
print(importances)

fig, ax = plt.subplots(figsize=(8, 5))
importances.sort_values().plot(kind="barh", ax=ax, color="#1f3a5f")
ax.set_xlabel("Importance")
ax.set_title("Random Forest Feature Importance")
fig.tight_layout()
fig.savefig(f"{CHART_DIR}/feature_importance.png", dpi=130)
plt.close(fig)
print(f"Feature importance chart saved to {CHART_DIR}/feature_importance.png")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
models = [baseline, forest]
names = [r["name"] for r in models]
axes[0].bar(names, [r["rmse"] for r in models], color=["#888888", "#c0392b"])
axes[0].set_ylabel("RMSE ($)")
axes[0].set_title("RMSE by Model")
axes[0].tick_params(axis="x", rotation=15)
axes[1].bar(names, [r["r2"] for r in models], color=["#888888", "#c0392b"])
axes[1].set_ylabel("R2")
axes[1].set_ylim(0, 1)
axes[1].set_title("R2 by Model")
axes[1].tick_params(axis="x", rotation=15)
fig.tight_layout()
fig.savefig(f"{CHART_DIR}/model_comparison.png", dpi=130)
plt.close(fig)
print(f"Model comparison chart saved to {CHART_DIR}/model_comparison.png")

# 9. Verdict
section("9. Verdict")
best = max((baseline, forest), key=lambda r: r["r2"])
mean_revenue = y.mean()
relative_error = best["mae"] / mean_revenue * 100

if best["r2"] >= 0.7:
    quality = "good"
elif best["r2"] >= 0.4:
    quality = "moderate"
else:
    quality = "weak"

print(
    f"Best model: {best['name']}\n"
    f"  Explains {best['r2']*100:.1f}% of the variance in order revenue (R2 = {best['r2']:.3f}).\n"
    f"  Typical prediction error: ${best['mae']:,.2f} per order "
    f"({relative_error:.1f}% of the average order revenue of ${mean_revenue:,.2f}).\n"
    f"  Overall assessment: {quality.upper()} -- "
)
if quality == "good":
    print("  the model captures most of the predictable signal in revenue from category, "
          "quantity, product, and timing alone, without seeing price.")
elif quality == "moderate":
    print("  the model captures a real signal but leaves meaningful error -- useful as a "
          "rough estimate, not for precise revenue commitments.")
else:
    print("  category/quantity/product/timing alone don't explain order revenue well -- "
          "price-related information would likely be needed for a materially better model.")

outperforms_baseline = forest["r2"] - baseline["r2"] > 0.05
print(
    f"\nComparison check: Random Forest R2 ({forest['r2']:.3f}) vs. Linear baseline R2 "
    f"({baseline['r2']:.3f}) -- "
    + (
        "the more complex model meaningfully outperforms the baseline."
        if outperforms_baseline
        else "the more complex model does not meaningfully outperform the simple baseline, "
             "suggesting the relationship between these features and revenue is close to linear."
    )
)

# 10. Save metrics (CSV + JSON, for reuse e.g. in the Streamlit dashboard)
section("10. Saving Metrics")
metrics_df = pd.DataFrame(
    [{"model": r["name"], "rmse": r["rmse"], "mae": r["mae"], "r2": r["r2"]} for r in (baseline, forest)]
)
metrics_csv_path = "model_metrics.csv"
metrics_df.to_csv(metrics_csv_path, index=False)
print(f"Model metrics saved to {metrics_csv_path}")

metrics_json = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "models": [
        {"model": r["name"], "rmse": r["rmse"], "mae": r["mae"], "r2": r["r2"]}
        for r in (baseline, forest)
    ],
    "best_model": best["name"],
    "mean_revenue": float(mean_revenue),
    "relative_error_pct": float(relative_error),
    "quality": quality,
    "outperforms_baseline": bool(outperforms_baseline),
    "feature_importance": importances.to_dict(),
}
metrics_json_path = "model_metrics.json"
with open(metrics_json_path, "w") as f:
    json.dump(metrics_json, f, indent=2)
print(f"Model metrics saved to {metrics_json_path}")
