from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

crime_dir = PROJECT_ROOT / "data/raw/crime"
population_dir = PROJECT_ROOT / "data/raw/population"
density_dir = PROJECT_ROOT / "data/raw/density"
labour_dir = PROJECT_ROOT / "data/raw/labour"
deprivation_dir = PROJECT_ROOT / "data/raw/deprivation"

files = {
    "crime_recent": crime_dir / "mps_borough_recent.csv",
    "crime_historical": crime_dir / "mps_borough_historical.csv",
}

for folder_name, folder_path in {
    "population": population_dir,
    "density": density_dir,
    "labour": labour_dir,
    "deprivation": deprivation_dir,
}.items():
    found = list(folder_path.glob("*"))
    if found:
        files[folder_name] = found[0]

def load_file(path):
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, low_memory=False)
    elif path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")

def inspect_df(name, df):
    print("\n" + "=" * 70)
    print(f"DATASET: {name}")
    print("=" * 70)
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(10))
    print("\nDuplicate rows:", df.duplicated().sum())

for name, path in files.items():
    print(f"\nLoading {name}: {path}")
    if not path.exists():
        print("File not found")
        continue
    try:
        df = load_file(path)
        inspect_df(name, df)
    except Exception as e:
        print("Error:", e)