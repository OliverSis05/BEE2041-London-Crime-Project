from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW = PROJECT_ROOT / "data" / "raw"
CLEAN = PROJECT_ROOT / "data" / "clean"

CLEAN.mkdir(parents=True, exist_ok=True)

LONDON_BOROUGHS = {
    "City of London",
    "Barking and Dagenham",
    "Barnet",
    "Bexley",
    "Brent",
    "Bromley",
    "Camden",
    "Croydon",
    "Ealing",
    "Enfield",
    "Greenwich",
    "Hackney",
    "Hammersmith and Fulham",
    "Haringey",
    "Harrow",
    "Havering",
    "Hillingdon",
    "Hounslow",
    "Islington",
    "Kensington and Chelsea",
    "Kingston upon Thames",
    "Lambeth",
    "Lewisham",
    "Merton",
    "Newham",
    "Redbridge",
    "Richmond upon Thames",
    "Southwark",
    "Sutton",
    "Tower Hamlets",
    "Waltham Forest",
    "Wandsworth",
    "Westminster",
}

def keep_london_boroughs(df: pd.DataFrame, borough_col: str = "borough") -> pd.DataFrame:
    before = len(df)
    df = df[df[borough_col].isin(LONDON_BOROUGHS)].copy()
    print(f"Kept London boroughs only in {borough_col}: {before} -> {len(df)} rows")
    return df

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
        "city of london": "City of London",
        "barking & dagenham": "Barking and Dagenham",
        "barking and dagenham": "Barking and Dagenham",
        "hammersmith & fulham": "Hammersmith and Fulham",
        "hammersmith and fulham": "Hammersmith and Fulham",
        "kensington & chelsea": "Kensington and Chelsea",
        "kensington and chelsea": "Kensington and Chelsea",
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

# 1. CLEAN CRIME DATA

crime_recent_path = RAW / "crime" / "mps_borough_recent.csv"
crime_historical_path = RAW / "crime" / "mps_borough_historical.csv"

crime_recent = pd.read_csv(crime_recent_path, low_memory=False)
crime_historical = pd.read_csv(crime_historical_path, low_memory=False)

crime_recent = standardise_columns(crime_recent)
crime_historical = standardise_columns(crime_historical)

crime = pd.concat([crime_historical, crime_recent], ignore_index=True, sort=False)
crime = standardise_columns(crime)

print_check("RAW CRIME DATA", crime)

# These are the identifier columns in your raw crime file
id_vars = ["majortext", "minortext", "boroughname"]

for col in id_vars:
    if col not in crime.columns:
        raise KeyError(f"Expected column '{col}' not found in crime data")

# Month columns look like 201004, 201005, 201006, etc.
month_cols = [c for c in crime.columns if str(c).isdigit() and len(str(c)) == 6]

if len(month_cols) == 0:
    raise KeyError("No month columns like 201004 found in crime data")

print("\nDetected crime ID columns:")
print(id_vars)

print("\nFirst 10 detected month columns:")
print(month_cols[:10])

# Reshape from wide to long
crime = crime.melt(
    id_vars=id_vars,
    value_vars=month_cols,
    var_name="yyyymm",
    value_name="crime_count"
)

# Rename columns
crime = crime.rename(
    columns={
        "majortext": "crime_type",
        "minortext": "crime_subtype",
        "boroughname": "borough",
    }
)

crime["borough"] = crime["borough"].apply(clean_borough_name)
crime["crime_type"] = crime["crime_type"].astype(str).str.strip()
crime["crime_subtype"] = crime["crime_subtype"].astype(str).str.strip()
crime["crime_count"] = pd.to_numeric(crime["crime_count"], errors="coerce")

crime["year"] = pd.to_numeric(crime["yyyymm"].str[:4], errors="coerce")
crime["month"] = pd.to_numeric(crime["yyyymm"].str[4:6], errors="coerce")

crime = crime[
    (crime["year"] >= 2019) &
    (crime["year"] <= 2024)
].copy()

crime = crime.dropna(subset=["borough", "crime_type", "crime_count", "year", "month"])

crime = (
    crime.groupby(
        ["borough", "year", "month", "crime_type", "crime_subtype"],
        as_index=False
    )["crime_count"]
    .sum()
)

crime = keep_london_boroughs(crime)

crime = crime.sort_values(
    ["borough", "year", "month", "crime_type", "crime_subtype"]
).reset_index(drop=True)

print_check("CLEAN CRIME DATA", crime)
save_clean(crime, "crime_clean.csv")

# 2. CLEAN POPULATION DATA

population_file = next((RAW / "population").glob("*.xlsx"))

population = pd.read_excel(population_file, sheet_name="MYEB1", header=1)
population = standardise_columns(population)

print_check("RAW POPULATION DATA", population)

# Borough name column and all year columns
borough_col = "laname23"
year_cols = [c for c in population.columns if c.startswith("population_")]

print("\nDetected population columns:")
print("borough_col =", borough_col)
print("year_cols =", year_cols)

population = population[[borough_col] + year_cols].copy()
population = population.rename(columns={borough_col: "borough"})

population["borough"] = population["borough"].apply(clean_borough_name)

# Sum across sex and age rows to get total population per borough
population = population.groupby("borough", as_index=False)[year_cols].sum()

# Reshape from wide to long
population = population.melt(
    id_vars="borough",
    value_vars=year_cols,
    var_name="year",
    value_name="population"
)

population["year"] = population["year"].str.replace("population_", "", regex=False)
population["year"] = pd.to_numeric(population["year"], errors="coerce")
population["population"] = pd.to_numeric(population["population"], errors="coerce")

population = population[
    (population["year"] >= 2019) &
    (population["year"] <= 2024)
].copy()

population = population.dropna(subset=["borough", "year", "population"])
population = keep_london_boroughs(population)
population = population.sort_values(["borough", "year"]).reset_index(drop=True)

print_check("CLEAN POPULATION DATA", population)
save_clean(population, "population_clean.csv")

# 3. CLEAN DENSITY DATA

density_file = next((RAW / "density").glob("*"))

# Read the correct sheet and use the second row as headers
density = pd.read_excel(density_file, sheet_name="Borough", header=1)
density = standardise_columns(density)

print_check("RAW DENSITY DATA", density)

borough_col = find_col(density.columns, ["area_name", "borough", "name"])
density_col = find_col(
    density.columns,
    ["population_per_square_kilometre", "population_density", "density"]
)

# Extra safety in case the exact wording varies slightly
if density_col is None:
    density_col = next(
        (c for c in density.columns if "population_per_square_kilometre" in c),
        None
    )

print("\nDetected density columns:")
print("borough_col =", borough_col)
print("density_col =", density_col)

if borough_col is None or density_col is None:
    raise KeyError(
        f"Could not detect required density columns. Found columns: {density.columns.tolist()}"
    )

density = density[[borough_col, density_col]].copy()
density.columns = ["borough", "population_density"]

density["borough"] = density["borough"].apply(clean_borough_name)
density["population_density"] = pd.to_numeric(density["population_density"], errors="coerce")

density = density.dropna(subset=["borough", "population_density"]).copy()
density = keep_london_boroughs(density)

# Remove accidental header / chooser rows if they slipped in
density = density[
    ~density["borough"].astype(str).str.lower().isin(["area name", "choose year", "nan"])
].copy()

density = density.sort_values("borough").reset_index(drop=True)

print_check("CLEAN DENSITY DATA", density)
save_clean(density, "density_clean.csv")

# 4. CLEAN LABOUR DATA

labour_file = next((RAW / "labour").glob("*"))

labour_raw = pd.read_excel(labour_file, header=None)

print("\n" + "=" * 80)
print("RAW LABOUR DATA")
print("=" * 80)
print("Shape:", labour_raw.shape)
print(labour_raw.head(15).to_string())

# In this file:
# row 7 = headers (Date + borough names)
# row 8 onwards = monthly values
header_row = 7
data_start_row = 8

labour = labour_raw.iloc[data_start_row:].copy()
labour.columns = labour_raw.iloc[header_row].tolist()

# Keep only real columns
labour = labour.loc[:, labour.columns.notna()].copy()
labour.columns = [str(c).strip() for c in labour.columns]

# First column should be the date column
first_col = labour.columns[0]
labour = labour.rename(columns={first_col: "date"})

# Convert date
labour["date"] = pd.to_datetime(labour["date"], format="%B %Y", errors="coerce")

# Drop rows that are not real monthly data
labour = labour.dropna(subset=["date"]).copy()


# Reshape from wide to long
labour = labour.melt(
    id_vars="date",
    var_name="borough",
    value_name="claimant_count"
)

# Clean fields
labour["borough"] = labour["borough"].astype(str).str.strip()
labour["borough"] = labour["borough"].apply(clean_borough_name)
labour["claimant_count"] = pd.to_numeric(labour["claimant_count"], errors="coerce")

labour["year"] = labour["date"].dt.year
labour["month"] = labour["date"].dt.month

labour = labour[
    (labour["year"] >= 2019) &
    (labour["year"] <= 2024)
].copy()

labour = labour.dropna(subset=["borough", "date", "claimant_count"]).copy()

# Keep only claimant-count rows, not rate rows
labour = labour[np.isclose(labour["claimant_count"] % 1, 0)].copy()
labour["claimant_count"] = labour["claimant_count"].round().astype(int)

labour["year"] = labour["date"].dt.year
labour["month"] = labour["date"].dt.month

labour = labour[
    (labour["year"] >= 2019) &
    (labour["year"] <= 2024)
].copy()

labour = keep_london_boroughs(labour)

labour = labour[["borough", "year", "month", "claimant_count"]]
labour = labour.sort_values(["borough", "year", "month"]).reset_index(drop=True)

print_check("CLEAN LABOUR DATA", labour)
save_clean(labour, "labour_clean.csv")

# 5. CLEAN DEPRIVATION DATA

deprivation_file = list((RAW / "deprivation").glob("*"))[0]

# Read the correct sheet
deprivation = pd.read_excel(deprivation_file, sheet_name="IMD 2019")
deprivation = standardise_columns(deprivation)

print_check("RAW DEPRIVATION DATA", deprivation)

borough_col = find_col(
    deprivation.columns,
    [
        "local_authority_district_name_2019",
        "local_authority_district_name",
        "borough",
        "name",
    ],
)

imd_col = find_col(
    deprivation.columns,
    [
        "index_of_multiple_deprivation_imd_score",
        "imd_score",
    ],
)

print("\nDetected deprivation columns:")
print("borough_col =", borough_col)
print("imd_col =", imd_col)

if borough_col is None or imd_col is None:
    raise KeyError(
        f"Could not detect required deprivation columns. Found columns: {deprivation.columns.tolist()}"
    )

deprivation = deprivation[[borough_col, imd_col]].copy()
deprivation.columns = ["borough", "imd_value"]

deprivation["borough"] = deprivation["borough"].apply(clean_borough_name)
deprivation["imd_value"] = pd.to_numeric(deprivation["imd_value"], errors="coerce")

deprivation = deprivation.dropna(subset=["borough", "imd_value"]).copy()

# IMD 2019 sheet is LSOA-level, so aggregate to borough level
deprivation = (
    deprivation.groupby("borough", as_index=False)["imd_value"]
    .mean()
)
deprivation = keep_london_boroughs(deprivation)

deprivation = deprivation.sort_values("borough").reset_index(drop=True)

print_check("CLEAN DEPRIVATION DATA", deprivation)
save_clean(deprivation, "deprivation_clean.csv")

