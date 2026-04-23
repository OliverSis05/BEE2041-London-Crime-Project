from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLEAN = PROJECT_ROOT / "data" / "clean"
FINAL = PROJECT_ROOT / "data" / "final"

FINAL.mkdir(parents=True, exist_ok=True)

def load_csv(filename: str) -> pd.DataFrame:
    path = CLEAN / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path)
    print(f"\nLoaded {filename}: {df.shape}")
    return df

def clean_borough(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()

# 1. LOAD CLEAN FILES

crime = load_csv("crime_clean.csv")
population = load_csv("population_clean.csv")
density = load_csv("density_clean.csv")
labour = load_csv("labour_clean.csv")
deprivation = load_csv("deprivation_clean.csv")

for df in [crime, population, density, labour, deprivation]:
    if "borough" in df.columns:
        df["borough"] = clean_borough(df["borough"])

# 2. MAKE CRIME MONTHLY TOTALS

crime_monthly = (
    crime.groupby(["borough", "year", "month"], as_index=False)["crime_count"]
    .sum()
)

print("\n" + "=" * 80)
print("CRIME MONTHLY")
print("=" * 80)
print("Shape:", crime_monthly.shape)
print(crime_monthly.head())

# 3. FIX LABOUR DUPLICATES 

labour_dupes = labour.duplicated(subset=["borough", "year", "month"]).sum()
print("\nLabour duplicate borough-year-month rows:", labour_dupes)

if labour_dupes > 0:
    print("Fixing labour duplicates by taking the maximum claimant_count per borough-year-month...")
    labour = (
        labour.groupby(["borough", "year", "month"], as_index=False)["claimant_count"]
        .max()
    )

print("Labour shape after fix:", labour.shape)

# 4. KEEP ONLY BOROUGHS THAT EXIST IN ALL FILES

borough_sets = [
    set(crime_monthly["borough"].dropna().unique()),
    set(population["borough"].dropna().unique()),
    set(density["borough"].dropna().unique()),
    set(labour["borough"].dropna().unique()),
    set(deprivation["borough"].dropna().unique()),
]

common_boroughs = sorted(set.intersection(*borough_sets))

print("\n" + "=" * 80)
print("COMMON BOROUGHS")
print("=" * 80)
print("Count:", len(common_boroughs))
print(common_boroughs)

crime_monthly = crime_monthly[crime_monthly["borough"].isin(common_boroughs)].copy()
population = population[population["borough"].isin(common_boroughs)].copy()
density = density[density["borough"].isin(common_boroughs)].copy()
labour = labour[labour["borough"].isin(common_boroughs)].copy()
deprivation = deprivation[deprivation["borough"].isin(common_boroughs)].copy()

# 5. MERGE EVERYTHING

merged = crime_monthly.merge(
    population,
    on=["borough", "year"],
    how="left"
)

merged = merged.merge(
    labour,
    on=["borough", "year", "month"],
    how="left"
)

merged = merged.merge(
    density,
    on="borough",
    how="left"
)

merged = merged.merge(
    deprivation,
    on="borough",
    how="left"
)

# 6. ADD USEFUL ANALYSIS COLUMNS

merged["date"] = pd.to_datetime(
    dict(year=merged["year"], month=merged["month"], day=1),
    errors="coerce"
)

merged["crime_per_1000"] = (merged["crime_count"] / merged["population"]) * 1000
merged["claimant_per_1000"] = (merged["claimant_count"] / merged["population"]) * 1000

merged = merged[
    [
        "borough",
        "date",
        "year",
        "month",
        "crime_count",
        "population",
        "crime_per_1000",
        "claimant_count",
        "claimant_per_1000",
        "population_density",
        "imd_value",
    ]
].copy()

merged = merged.sort_values(["borough", "year", "month"]).reset_index(drop=True)

# 7. SAVE FINAL DATASET

output_path = FINAL / "london_borough_month_panel.csv"
merged.to_csv(output_path, index=False)

print("\n" + "=" * 80)
print("FINAL MERGED DATASET")
print("=" * 80)
print("Saved to:", output_path)
print("Shape:", merged.shape)
print("Columns:", merged.columns.tolist())
print("\nFirst 10 rows:")
print(merged.head(10))

print("\nMissing values:")
print(merged.isna().sum().sort_values(ascending=False))

print("\nDuplicate rows:", merged.duplicated().sum())
print("Unique boroughs:", merged["borough"].nunique())
print("Year range:", merged["year"].min(), "to", merged["year"].max())