
from pathlib import Path
import pandas as pd

# Locate the CSV relative to this Python file
DATA_FILE = Path(__file__).parent / "data" / "students.csv"

# Check that the dataset exists
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

# Load the CSV into a Pandas DataFrame
df = pd.read_csv(DATA_FILE)

# Display the results
print("DATASET LOADED SUCCESSFULLY")
print("-" * 40)

print("\nFirst five records:")
print(df.head())

print("\nDataset shape:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values per column:")
print(df.isnull().sum())

print("\nNumerical summary:")
print(df.describe().round(2))

# Basic validation
required_columns = [
    "student_id",
    "study_hours",
    "python_score",
    "dsa_score",
    "math_score",
    "attendance_pct",
]

assert df.columns.tolist() == required_columns, "Column names or order are incorrect."
assert len(df) == 20, "Expected 20 student records."
assert df["student_id"].is_unique, "Student IDs must be unique."
assert df[required_columns].notnull().all().all(), "Missing values found."

print("\nAll basic dataset checks passed!")
