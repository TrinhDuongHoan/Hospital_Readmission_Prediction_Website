from pathlib import Path
import pandas as pd


MISSING_VALUES = ["?", "None", "NULL", "null", "NA", "N/A", ""]


def load_dataset(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(path, na_values=MISSING_VALUES)
    return df


if __name__ == "__main__":
    df = load_dataset("data/raw/diabetic_data.csv")
    print("Shape:", df.shape)
    print(df.head())
    print(df.columns.tolist())
    print("\nTop missing columns:")
    print(df.isna().mean().sort_values(ascending=False).head(15))