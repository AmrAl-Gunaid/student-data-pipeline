from pathlib import Path
import logging

import pandas as pd

# ==========================================================
# Configuration
# ==========================================================
RAW_FILE = Path("data/raw/students_raw.csv")
OUTPUT_FILE = Path("data/processed/students_ml_ready.csv")
LOG_FILE = Path("logs/pipeline.log")

REQUIRED_COLUMNS = {
    "student_id",
    "name",
    "age",
    "gpa",
    "attendance",
    "city"
}

# ==========================================================
# Logging
# ==========================================================
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=("%(asctime)s | %(levelname)s | %(message)s")
)

logger = logging.getLogger(__name__)


# ==========================================================
# Load
# ==========================================================
def load_data(file_path: Path) -> pd.DataFrame:
    logger.info("Loading data from %s", file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("Input dataset is empty.")

    logger.info("Loaded %d rows and %d columns", len(df), len(df.columns))
    return df


# ==========================================================
# Schema Validation
# ==========================================================
def validate_schema(df: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")


# ==========================================================
# Type Conversion
# ==========================================================
def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    numeric_columns = ["student_id", "age", "gpa", "attendance"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


# ==========================================================
# Cleaning
# ==========================================================
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Remove duplicate student IDs
    df = df.drop_duplicates(subset=["student_id"], keep="first")

    # Clean text
    df["name"] = df["name"].astype("string").str.strip()
    df["city"] = df["city"].astype("string").str.strip().str.title()

    # Invalid GPA
    df.loc[~df["gpa"].between(0, 4), "gpa"] = pd.NA

    # Invalid Age
    df.loc[~df["age"].between(16, 80), "age"] = pd.NA

    # Invalid attendance
    df.loc[~df["attendance"].between(0, 100), "attendance"] = pd.NA

    # Fill missing numeric values
    for column in ["age", "gpa", "attendance"]:
        df[column] = df[column].fillna(df[column].median())

    return df


# ==========================================================
# Validation
# ==========================================================
def validate_data(df: pd.DataFrame) -> None:
    errors = []

    if df.empty:
        errors.append("Dataset is empty.")

    if df["student_id"].isnull().any():
        errors.append("student_id contains NULL.")

    if df["student_id"].duplicated().any():
        errors.append("student_id is not unique.")

    if df["name"].isnull().any():
        errors.append("name contains NULL.")

    if not df["age"].between(16, 80).all():
        errors.append("Invalid age values.")

    if not df["gpa"].between(0, 4).all():
        errors.append("Invalid GPA values.")

    if not df["attendance"].between(0, 100).all():
        errors.append("Invalid attendance values.")

    if errors:
        raise ValueError(
            "Validation failed:\n"
            + "\n".join(f"- {error}" for error in errors)
        )


# ==========================================================
# Save
# ==========================================================
def save_data(df: pd.DataFrame, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    logger.info("Saved processed data to %s", output_file)


# ==========================================================
# Pipeline
# ==========================================================
def run_pipeline() -> None:
    try:
        logger.info("Pipeline started.")

        df = load_data(RAW_FILE)
        validate_schema(df)
        df = convert_data_types(df)
        df = clean_data(df)
        validate_data(df)
        save_data(df, OUTPUT_FILE)

        logger.info("Pipeline completed successfully.")
        print("Pipeline completed successfully.")

    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        print(f"Pipeline failed: {exc}")
        raise


if __name__ == "__main__":
    run_pipeline()