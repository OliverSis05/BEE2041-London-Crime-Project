from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FINAL = PROJECT_ROOT / "data" / "final"
OUTPUT = PROJECT_ROOT / "output" / "analysis"
FIGURES = OUTPUT / "figures"
TABLES = OUTPUT / "tables"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

DATA_PATH = FINAL / "london_borough_month_panel.csv"

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ============================================================
# 1. BOROUGH-LEVEL AVERAGES
# ============================================================

borough_df = (
    df.groupby("borough", as_index=False)
    .agg(
        crime_per_1000=("crime_per_1000", "mean"),
        claimant_per_1000=("claimant_per_1000", "mean"),
        population_density=("population_density", "mean"),
        imd_value=("imd_value", "mean"),
    )
)

borough_df.to_csv(TABLES / "borough_level_analysis_data.csv", index=False)

print("\n" + "=" * 80)
print("BOROUGH-LEVEL ANALYSIS DATA")
print("=" * 80)
print("Shape:", borough_df.shape)
print(borough_df.head(10).to_string(index=False))

# ============================================================
# 2. SIMPLE CORRELATIONS
# ============================================================

predictors = ["claimant_per_1000", "population_density", "imd_value"]

simple_corrs = []
for col in predictors:
    corr = borough_df["crime_per_1000"].corr(borough_df[col])
    simple_corrs.append({"predictor": col, "correlation_with_crime_per_1000": corr})

simple_corrs_df = pd.DataFrame(simple_corrs).sort_values(
    "correlation_with_crime_per_1000",
    key=lambda s: s.abs(),
    ascending=False
)

simple_corrs_df.to_csv(TABLES / "simple_correlations.csv", index=False)

print("\n" + "=" * 80)
print("SIMPLE CORRELATIONS WITH CRIME PER 1000")
print("=" * 80)
print(simple_corrs_df.to_string(index=False))

# ============================================================
# 3. STANDARDISED MULTIPLE REGRESSION USING NUMPY
# ============================================================

analysis_df = borough_df[["crime_per_1000", "claimant_per_1000", "population_density", "imd_value"]].copy()

# standardise all variables
for col in analysis_df.columns:
    analysis_df[col] = (analysis_df[col] - analysis_df[col].mean()) / analysis_df[col].std(ddof=0)

y = analysis_df["crime_per_1000"].to_numpy()
X = analysis_df[["claimant_per_1000", "population_density", "imd_value"]].to_numpy()

# add intercept
X = np.column_stack([np.ones(len(X)), X])

# OLS coefficients
beta = np.linalg.inv(X.T @ X) @ X.T @ y

coef_df = pd.DataFrame({
    "term": ["intercept", "claimant_per_1000", "population_density", "imd_value"],
    "standardised_coefficient": beta
})

coef_df.to_csv(TABLES / "standardised_regression_coefficients.csv", index=False)

print("\n" + "=" * 80)
print("STANDARDISED REGRESSION COEFFICIENTS")
print("=" * 80)
print(coef_df.to_string(index=False))

# calculate fitted values and R-squared
y_hat = X @ beta
ss_total = np.sum((y - y.mean()) ** 2)
ss_resid = np.sum((y - y_hat) ** 2)
r_squared = 1 - (ss_resid / ss_total)

print("\nR-squared:", round(r_squared, 4))

# ============================================================
# 4. RANK PREDICTORS BY ABSOLUTE EFFECT SIZE
# ============================================================

ranked_effects = coef_df[coef_df["term"] != "intercept"].copy()
ranked_effects["abs_effect"] = ranked_effects["standardised_coefficient"].abs()
ranked_effects = ranked_effects.sort_values("abs_effect", ascending=False)

ranked_effects.to_csv(TABLES / "ranked_predictor_effects.csv", index=False)

print("\n" + "=" * 80)
print("RANKED PREDICTOR EFFECTS")
print("=" * 80)
print(ranked_effects.to_string(index=False))

# ============================================================
# 5. CHARTS
# ============================================================

# Bar chart of absolute effect sizes
plt.figure(figsize=(8, 5))
plt.bar(ranked_effects["term"], ranked_effects["abs_effect"])
plt.title("Relative Strength of Predictors")
plt.xlabel("Predictor")
plt.ylabel("Absolute Standardised Coefficient")
plt.tight_layout()
plt.savefig(FIGURES / "predictor_strengths.png", dpi=300)
plt.close()

# Scatter plots
for col in predictors:
    plt.figure(figsize=(7, 5))
    plt.scatter(borough_df[col], borough_df["crime_per_1000"])
    for _, row in borough_df.iterrows():
        plt.annotate(row["borough"], (row[col], row["crime_per_1000"]), fontsize=7)
    plt.title(f"{col} vs crime_per_1000")
    plt.xlabel(col)
    plt.ylabel("crime_per_1000")
    plt.tight_layout()
    plt.savefig(FIGURES / f"{col}_vs_crime_per_1000.png", dpi=300)
    plt.close()

# ============================================================
# 6. QUICK CONCLUSION
# ============================================================

strongest = ranked_effects.iloc[0]
weakest = ranked_effects.iloc[-1]

summary_lines = [
    f"R-squared: {r_squared:.4f}",
    f"Strongest predictor: {strongest['term']} ({strongest['standardised_coefficient']:.4f})",
    f"Weakest predictor: {weakest['term']} ({weakest['standardised_coefficient']:.4f})",
]

with open(TABLES / "analysis_summary.txt", "w") as f:
    for line in summary_lines:
        f.write(line + "\n")

print("\n" + "=" * 80)
print("QUICK CONCLUSION")
print("=" * 80)
for line in summary_lines:
    print(line)

    