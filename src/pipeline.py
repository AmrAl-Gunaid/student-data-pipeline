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
    logger.info("Loading data from %s",file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found at {file_path}")

    df = pd.read_csv(file_path)
    if df.empty:
        raise FileNotFoundError("Input dataset is empty.")

    logger.info("Loaded %d rows and %d columna",len(df),len(df.columns))
    return df


# ==========================================================
# Schema Validation
# ==========================================================
def validate_schema(df: pd.DataFrame)->None:
    missing_columns=REQUIRED_COLUMNS-set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")