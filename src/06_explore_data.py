from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FINAL = PROJECT_ROOT / "data" / "final"
OUTPUT = PROJECT_ROOT / "output" / "exploration"
FIGURES = OUTPUT / "figures"
TABLES = OUTPUT / "tables"

OUTPUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

DATA_PATH = FINAL / "london_borough_month_panel.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Missing merged dataset: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("\n" + "=" * 80)
print("MERGED DATASET OVERVIEW")
print("=" * 80)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nFirst 10 rows:")
print(df.head(10).to_string())

print("\nMissing values:")
print(df.isna().sum().sort_values(ascending=False))

print("\nDuplicate rows:", df.duplicated().sum())
print("Unique boroughs:", df["borough"].nunique())
print("Year range:", df["year"].min(), "to", df["year"].max())

# 1. SUMMARY STATISTICS

numeric_cols = [
    "crime_count",
    "population",
    "crime_per_1000",
    "claimant_count",
    "claimant_per_1000",
    "population_density",
    "imd_value",
]

summary_stats = df[numeric_cols].describe().T
summary_stats.to_csv(TABLES / "summary_statistics.csv")

print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print(summary_stats)

# 2. BOROUGH-LEVEL SUMMARY

borough_summary = (
    df.groupby("borough", as_index=False)
    .agg(
        avg_crime_count=("crime_count", "mean"),
        avg_crime_per_1000=("crime_per_1000", "mean"),
        avg_claimant_count=("claimant_count", "mean"),
        avg_claimant_per_1000=("claimant_per_1000", "mean"),
        population_density=("population_density", "mean"),
        imd_value=("imd_value", "mean"),
    )
    .sort_values("avg_crime_per_1000", ascending=False)
    .reset_index(drop=True)
)

borough_summary.to_csv(TABLES / "borough_summary.csv", index=False)

print("\n" + "=" * 80)
print("TOP 10 BOROUGHS BY AVERAGE CRIME PER 1000")
print("=" * 80)
print(borough_summary.head(10).to_string(index=False))

print("\n" + "=" * 80)
print("BOTTOM 10 BOROUGHS BY AVERAGE CRIME PER 1000")
print("=" * 80)
print(borough_summary.tail(10).to_string(index=False))

# 3. TIME TRENDS

monthly_summary = (
    df.groupby("date", as_index=False)
    .agg(
        total_crime=("crime_count", "sum"),
        mean_crime_per_1000=("crime_per_1000", "mean"),
        total_claimants=("claimant_count", "sum"),
        mean_claimant_per_1000=("claimant_per_1000", "mean"),
    )
    .sort_values("date")
)

monthly_summary.to_csv(TABLES / "monthly_summary.csv", index=False)

yearly_summary = (
    df.groupby("year", as_index=False)
    .agg(
        total_crime=("crime_count", "sum"),
        mean_crime_per_1000=("crime_per_1000", "mean"),
        total_claimants=("claimant_count", "sum"),
        mean_claimant_per_1000=("claimant_per_1000", "mean"),
    )
    .sort_values("year")
)

yearly_summary.to_csv(TABLES / "yearly_summary.csv", index=False)

print("\n" + "=" * 80)
print("YEARLY SUMMARY")
print("=" * 80)
print(yearly_summary.to_string(index=False))

# 4. CORRELATIONS

corr_cols = [
    "crime_count",
    "crime_per_1000",
    "claimant_count",
    "claimant_per_1000",
    "population_density",
    "imd_value",
]

corr_matrix = df[corr_cols].corr(numeric_only=True)
corr_matrix.to_csv(TABLES / "correlation_matrix.csv")

print("\n" + "=" * 80)
print("CORRELATION MATRIX")
print("=" * 80)
print(corr_matrix)

# 5. CHARTS

# Chart 1: Total crime over time
plt.figure(figsize=(12, 6))
plt.plot(monthly_summary["date"], monthly_summary["total_crime"])
plt.title("Total Crime Over Time")
plt.xlabel("Date")
plt.ylabel("Total Crime Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURES / "total_crime_over_time.png", dpi=300)
plt.close()

# Chart 2: Mean crime per 1000 over time
plt.figure(figsize=(12, 6))
plt.plot(monthly_summary["date"], monthly_summary["mean_crime_per_1000"])
plt.title("Mean Crime per 1000 Over Time")
plt.xlabel("Date")
plt.ylabel("Mean Crime per 1000")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURES / "mean_crime_per_1000_over_time.png", dpi=300)
plt.close()

# Chart 3: Top 10 boroughs by average crime per 1000
top10 = borough_summary.head(10).sort_values("avg_crime_per_1000")
plt.figure(figsize=(10, 6))
plt.barh(top10["borough"], top10["avg_crime_per_1000"])
plt.title("Top 10 Boroughs by Average Crime per 1000")
plt.xlabel("Average Crime per 1000")
plt.ylabel("Borough")
plt.tight_layout()
plt.savefig(FIGURES / "top10_boroughs_crime_per_1000.png", dpi=300)
plt.close()

# For scatter plots use borough averages to avoid heavy overplotting
scatter_df = borough_summary.copy()

# Chart 4: Claimant rate vs crime rate
plt.figure(figsize=(8, 6))
plt.scatter(scatter_df["avg_claimant_per_1000"], scatter_df["avg_crime_per_1000"])
for _, row in scatter_df.iterrows():
    plt.annotate(row["borough"], (row["avg_claimant_per_1000"], row["avg_crime_per_1000"]), fontsize=7)
plt.title("Claimant Rate vs Crime Rate")
plt.xlabel("Average Claimant Count per 1000")
plt.ylabel("Average Crime per 1000")
plt.tight_layout()
plt.savefig(FIGURES / "claimant_vs_crime_rate.png", dpi=300)
plt.close()

# Chart 5: Deprivation vs crime rate
plt.figure(figsize=(8, 6))
plt.scatter(scatter_df["imd_value"], scatter_df["avg_crime_per_1000"])
for _, row in scatter_df.iterrows():
    plt.annotate(row["borough"], (row["imd_value"], row["avg_crime_per_1000"]), fontsize=7)
plt.title("Deprivation vs Crime Rate")
plt.xlabel("Average IMD Value")
plt.ylabel("Average Crime per 1000")
plt.tight_layout()
plt.savefig(FIGURES / "deprivation_vs_crime_rate.png", dpi=300)
plt.close()

# Chart 6: Population density vs crime rate
plt.figure(figsize=(8, 6))
plt.scatter(scatter_df["population_density"], scatter_df["avg_crime_per_1000"])
for _, row in scatter_df.iterrows():
    plt.annotate(row["borough"], (row["population_density"], row["avg_crime_per_1000"]), fontsize=7)
plt.title("Population Density vs Crime Rate")
plt.xlabel("Population Density")
plt.ylabel("Average Crime per 1000")
plt.tight_layout()
plt.savefig(FIGURES / "density_vs_crime_rate.png", dpi=300)
plt.close()

# 6. SAVE KEY OUTPUTS

top10_table = borough_summary.head(10)
bottom10_table = borough_summary.tail(10)

top10_table.to_csv(TABLES / "top10_boroughs_by_crime_per_1000.csv", index=False)
bottom10_table.to_csv(TABLES / "bottom10_boroughs_by_crime_per_1000.csv", index=False)

print("\n" + "=" * 80)
print("FILES CREATED")
print("=" * 80)
print("Tables folder:", TABLES)
print("Figures folder:", FIGURES)

print("\nSaved tables:")
for path in sorted(TABLES.glob("*.csv")):
    print("-", path.name)

print("\nSaved figures:")
for path in sorted(FIGURES.glob("*.png")):
    print("-", path.name)

# 7. QUICK TAKEAWAYS

highest_borough = borough_summary.iloc[0]
lowest_borough = borough_summary.iloc[-1]

print("\n" + "=" * 80)
print("QUICK TAKEAWAYS")
print("=" * 80)
print(
    f"Highest average crime per 1000: {highest_borough['borough']} "
    f"({highest_borough['avg_crime_per_1000']:.2f})"
)
print(
    f"Lowest average crime per 1000: {lowest_borough['borough']} "
    f"({lowest_borough['avg_crime_per_1000']:.2f})"
)

print("\nStrongest simple correlations with crime_per_1000:")
crime_corr = corr_matrix["crime_per_1000"].drop("crime_per_1000").sort_values(key=lambda s: s.abs(), ascending=False)
print(crime_corr)