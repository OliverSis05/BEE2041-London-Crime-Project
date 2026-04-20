from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW = PROJECT_ROOT / "data" / "raw"
CLEAN = PROJECT_ROOT / "data" / "clean"

CLEAN.mkdir(parents=True, exist_ok=True)

def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df

def clean_borough_name(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    replacements = {
        "city of westminster": "Westminster",
        "westminster city": "Westminster",
        "barking & dagenham": "Barking and Dagenham",
        "hammersmith & fulham": "Hammersmith and Fulham",
        "kensington & chelsea": "Kensington and Chelsea",
        "richmond upon thames": "Richmond upon Thames",
        "kingston upon thames": "Kingston upon Thames",
    }

    lower_value = value.lower()
    if lower_value in replacements:
        return replacements[lower_value]

    return value.title()

def save_clean(df: pd.DataFrame, filename: str) -> None:
    path = CLEAN / filename
    df.to_csv(path, index=False)
    print(f"Saved: {path}")

def print_check(name: str, df: pd.DataFrame) -> None:
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())
    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(10))
    print("\nDuplicate rows:", df.duplicated().sum())

def find_col(columns, candidates):
    for c in candidates:
        if c in columns:
            return c
    return None

# ============================================================
# 1. CLEAN CRIME DATA
# ============================================================

crime_recent_path = RAW / "crime" / "mps_borough_recent.csv"
crime_historical_path = RAW / "crime" / "mps_borough_historical.csv"

crime_recent = pd.read_csv(crime_recent_path, low_memory=False)
crime_historical = pd.read_csv(crime_historical_path, low_memory=False)

crime_recent = standardise_columns(crime_recent)
crime_historical = standardise_columns(crime_historical)

crime = pd.concat([crime_historical, crime_recent], ignore_index=True)
crime = standardise_columns(crime)

print_check("RAW CRIME DATA", crime)

borough_col = find_col(crime.columns, ["borough", "borough_name"])
crime_type_col = find_col(crime.columns, ["crime_type", "major_text", "offence_group"])
date_col = find_col(crime.columns, ["month", "date"])
count_col = find_col(crime.columns, ["count", "crime_count", "value"])

print("\nDetected crime columns:")
print("borough_col =", borough_col)
print("crime_type_col =", crime_type_col)
print("date_col =", date_col)
print("count_col =", count_col)

crime = crime[[borough_col, crime_type_col, date_col, count_col]].copy()
crime.columns = ["borough", "crime_type", "date", "crime_count"]

crime["borough"] = crime["borough"].apply(clean_borough_name)
crime["crime_type"] = crime["crime_type"].astype(str).str.strip()
crime["crime_count"] = pd.to_numeric(crime["crime_count"], errors="coerce")

crime["date"] = pd.to_datetime(crime["date"], errors="coerce")
crime["year"] = crime["date"].dt.year
crime["month"] = crime["date"].dt.month

crime = crime[
    (crime["year"] >= 2019) &
    (crime["year"] <= 2024)
].copy()

crime = crime.dropna(subset=["borough", "crime_type", "date", "crime_count"])

crime = (
    crime.groupby(["borough", "year", "month", "crime_type"], as_index=False)["crime_count"]
    .sum()
)

crime = crime.sort_values(["borough", "year", "month", "crime_type"]).reset_index(drop=True)

print_check("CLEAN CRIME DATA", crime)
save_clean(crime, "crime_clean.csv")

# ============================================================
# 2. CLEAN POPULATION DATA
# ============================================================

population_file = next((RAW / "population").glob("*.xlsx"))

population = pd.read_excel(population_file, sheet_name=0)
population = standardise_columns(population)

print_check("RAW POPULATION DATA", population)

borough_col = find_col(population.columns, ["name", "area_name", "borough", "local_authority"])
year_col = find_col(population.columns, ["year"])
population_col = find_col(population.columns, ["population", "all_ages", "persons"])

print("\nDetected population columns:")
print("borough_col =", borough_col)
print("year_col =", year_col)
print("population_col =", population_col)

population = population[[borough_col, year_col, population_col]].copy()
population.columns = ["borough", "year", "population"]

population["borough"] = population["borough"].apply(clean_borough_name)
population["year"] = pd.to_numeric(population["year"], errors="coerce")
population["population"] = pd.to_numeric(population["population"], errors="coerce")

population = population[
    (population["year"] >= 2019) &
    (population["year"] <= 2024)
].copy()

population = population.dropna(subset=["borough", "year", "population"])
population = population.sort_values(["borough", "year"]).reset_index(drop=True)

print_check("CLEAN POPULATION DATA", population)
save_clean(population, "population_clean.csv")

# ============================================================
# 3. CLEAN DENSITY DATA
# ============================================================

density_file = next((RAW / "density").glob("*"))

if density_file.suffix.lower() == ".csv":
    density = pd.read_csv(density_file, low_memory=False)
else:
    density = pd.read_excel(density_file)

density = standardise_columns(density)

print_check("RAW DENSITY DATA", density)

borough_col = find_col(density.columns, ["borough", "name", "area_name"])
density_col = find_col(density.columns, ["population_density", "density"])
year_col = find_col(density.columns, ["year"])

print("\nDetected density columns:")
print("borough_col =", borough_col)
print("density_col =", density_col)
print("year_col =", year_col)

if year_col is not None:
    density = density[[borough_col, year_col, density_col]].copy()
    density.columns = ["borough", "year", "population_density"]
    density["year"] = pd.to_numeric(density["year"], errors="coerce")
else:
    density = density[[borough_col, density_col]].copy()
    density.columns = ["borough", "population_density"]

density["borough"] = density["borough"].apply(clean_borough_name)
density["population_density"] = pd.to_numeric(density["population_density"], errors="coerce")

density = density.dropna(subset=["borough", "population_density"]).copy()

print_check("CLEAN DENSITY DATA", density)
save_clean(density, "density_clean.csv")

# ============================================================
# 4. CLEAN LABOUR DATA
# ============================================================

labour_file = next((RAW / "labour").glob("*"))

if labour_file.suffix.lower() == ".csv":
    labour = pd.read_csv(labour_file, low_memory=False)
else:
    labour = pd.read_excel(labour_file)

labour = standardise_columns(labour)

print_check("RAW LABOUR DATA", labour)

borough_col = find_col(labour.columns, ["borough", "geography_name", "name", "area_name"])
date_col = find_col(labour.columns, ["date", "month"])
value_col = find_col(labour.columns, ["obs_value", "value", "claimant_count", "claimants"])

print("\nDetected labour columns:")
print("borough_col =", borough_col)
print("date_col =", date_col)
print("value_col =", value_col)

labour = labour[[borough_col, date_col, value_col]].copy()
labour.columns = ["borough", "date", "claimant_count"]

labour["borough"] = labour["borough"].apply(clean_borough_name)
labour["claimant_count"] = pd.to_numeric(labour["claimant_count"], errors="coerce")

labour["date"] = pd.to_datetime(labour["date"], errors="coerce")
labour["year"] = labour["date"].dt.year
labour["month"] = labour["date"].dt.month

labour = labour[
    (labour["year"] >= 2019) &
    (labour["year"] <= 2024)
].copy()

labour = labour.dropna(subset=["borough", "date", "claimant_count"])

labour = (
    labour.groupby(["borough", "year", "month"], as_index=False)["claimant_count"]
    .mean()
)

labour = labour.sort_values(["borough", "year", "month"]).reset_index(drop=True)

print_check("CLEAN LABOUR DATA", labour)
save_clean(labour, "labour_clean.csv")

# ============================================================
# 5. CLEAN DEPRIVATION DATA
# ============================================================

deprivation_file = list((RAW / "deprivation").glob("*"))[0]

deprivation = pd.read_excel(deprivation_file, sheet_name=0)
deprivation = standardise_columns(deprivation)

print_check("RAW DEPRIVATION DATA", deprivation)

borough_col = find_col(deprivation.columns, ["borough", "local_authority_district_name", "name"])
imd_col = find_col(
    deprivation.columns,
    [
        "index_of_multiple_deprivation_imd_score",
        "imd_score",
        "average_score",
        "imd_rank",
        "average_rank",
    ],
)

print("\nDetected deprivation columns:")
print("borough_col =", borough_col)
print("imd_col =", imd_col)

deprivation = deprivation[[borough_col, imd_col]].copy()
deprivation.columns = ["borough", "imd_value"]

deprivation["borough"] = deprivation["borough"].apply(clean_borough_name)
deprivation["imd_value"] = pd.to_numeric(deprivation["imd_value"], errors="coerce")

deprivation = deprivation.dropna(subset=["borough", "imd_value"]).copy()
deprivation = deprivation.sort_values("borough").reset_index(drop=True)

print_check("CLEAN DEPRIVATION DATA", deprivation)
save_clean(deprivation, "deprivation_clean.csv")