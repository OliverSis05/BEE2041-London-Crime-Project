from pathlib import Path
import pandas as pd

CLEAN = Path(__file__).resolve().parents[1] / "data" / "clean"

for file in CLEAN.glob("*.csv"):
    print("\n" + "=" * 80)
    print(f"FILE: {file.name}")
    print("=" * 80)

    df = pd.read_csv(file)

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())
    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(10))
    print("\nDuplicate rows:", df.duplicated().sum())

    