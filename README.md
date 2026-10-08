# Student Data Engineering Pipeline

## Project Description
This project transforms raw student data into a validated ML-ready dataset.

## Pipeline Stages
Raw CSV → Load → Schema Validation → Type Conversion → Cleaning → Validation → Save

## Data Quality Rules
- `student_id` must be unique and not NULL.
- `name` must not be NULL.
- `age` must be between 16 and 80.
- `gpa` must be between 0 and 4.
- `attendance` must be between 0 and 100.

## Input
`data/raw/students_raw.csv`

## Output
`data/processed/students_ml_ready.csv`

## Logs
`logs/pipeline.log`

## Technologies
- Python 3.14
- Pandas 3.x
- pathlib (standard library)
- logging (standard library)

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/pipeline.py

student_data_pipeline/
├── data/
│   ├── raw/
│   │   └── students_raw.csv
│   └── processed/
│       └── students_ml_ready.csv   # generated
├── logs/
│   └── pipeline.log                # generated
├── src/
│   └── pipeline.py
├── requirements.txt
└── README.md