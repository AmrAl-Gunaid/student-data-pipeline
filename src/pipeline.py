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