
"""Core and advanced analysis for the Student Performance Dashboard."""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

DATA_FILE = Path(__file__).parent / "data" / "students.csv"

SCORE_COLUMNS = [
    "python_score",
    "dsa_score",
    "math_score",
]

REQUIRED_COLUMNS = [
    "student_id",
    "study_hours",
    "python_score",
    "dsa_score",
    "math_score",
    "attendance_pct",
]


# ============================================================
# STEP 3: VALIDATION AND BASIC ANALYSIS
# ============================================================

def validate_score(score):
    """Return True if a score is a finite number from 0 to 100."""
    if isinstance(score, (bool, np.bool_)):
        return False

    try:
        value = float(score)
    except (TypeError, ValueError):
        return False

    return np.isfinite(value) and 0 <= value <= 100


def validate_study_hours(hours):
    """Return True if study hours are between 0 and 24 per day."""
    if isinstance(hours, (bool, np.bool_)):
        return False

    try:
        value = float(hours)
    except (TypeError, ValueError):
        return False

    return np.isfinite(value) and 0 <= value <= 24


def calculate_average(scores):
    """Calculate the arithmetic mean of valid scores."""
    if len(scores) == 0:
        raise ValueError("At least one score is required.")

    if not all(validate_score(score) for score in scores):
        raise ValueError("Every score must be a number between 0 and 100.")

    return sum(float(score) for score in scores) / len(scores)


def get_grade(average):
    """Return a grade category for a valid average score."""
    if not validate_score(average):
        raise ValueError("Average must be between 0 and 100.")

    average = float(average)

    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def load_student_data(file_path=DATA_FILE):
    """Load and validate the structure and values of the CSV dataset."""
    df = pd.read_csv(file_path)

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("The dataset contains no student records.")

    if df["student_id"].isna().any():
        raise ValueError("Student IDs cannot be missing.")

    if df["student_id"].astype(str).str.strip().eq("").any():
        raise ValueError("Student IDs cannot be blank.")

    if df["student_id"].duplicated().any():
        raise ValueError("Student IDs must be unique.")

    numeric_columns = [
        "study_hours",
        *SCORE_COLUMNS,
        "attendance_pct",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

        if df[column].isna().any():
            raise ValueError(
                f"Column '{column}' contains missing or non-numeric values."
            )

        if not np.isfinite(df[column].to_numpy(dtype=float)).all():
            raise ValueError(
                f"Column '{column}' contains non-finite values."
            )

    for column in SCORE_COLUMNS:
        if not df[column].map(validate_score).all():
            raise ValueError(
                f"Column '{column}' contains scores outside 0-100."
            )

    if not df["study_hours"].map(validate_study_hours).all():
        raise ValueError("Study hours must be between 0 and 24.")

    if not df["attendance_pct"].map(validate_score).all():
        raise ValueError("Attendance must be between 0 and 100.")

    return df


def add_performance_metrics(df):
    """Return a copy of the dataset with average scores and grades."""
    missing = set(SCORE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing score columns: {sorted(missing)}")

    result = df.copy()

    for column in SCORE_COLUMNS:
        if not result[column].map(validate_score).all():
            raise ValueError(
                f"Column '{column}' contains invalid scores."
            )

    result["average_score"] = result[SCORE_COLUMNS].mean(axis=1)
    result["grade"] = result["average_score"].map(get_grade)

    return result


def analyze_performance(df):
    """Generate summary statistics and student performance insights."""
    if df.empty:
        raise ValueError("Cannot analyze an empty dataset.")

    scored_df = add_performance_metrics(df)

    summary = {
        "student_count": len(scored_df),
        "class_average": float(scored_df["average_score"].mean()),
        "highest_average": float(scored_df["average_score"].max()),
        "lowest_average": float(scored_df["average_score"].min()),
        "average_study_hours": float(scored_df["study_hours"].mean()),
        "average_attendance": float(scored_df["attendance_pct"].mean()),
        "grade_distribution": (
            scored_df["grade"]
            .value_counts()
            .reindex(["A+", "A", "B", "C", "D", "F"], fill_value=0)
            .to_dict()
        ),
        "subject_averages": (
            scored_df[SCORE_COLUMNS].mean().to_dict()
        ),
    }

    top_score = scored_df["average_score"].max()
    top_students = scored_df.loc[
        scored_df["average_score"] == top_score,
        ["student_id", "average_score", "grade"],
    ].to_dict(orient="records")

    summary["top_students"] = top_students

    if (
        len(scored_df) >= 2
        and scored_df["study_hours"].nunique() > 1
        and scored_df["average_score"].nunique() > 1
    ):
        summary["study_hours_score_correlation"] = float(
            scored_df["study_hours"].corr(scored_df["average_score"])
        )
    else:
        summary["study_hours_score_correlation"] = None

    return summary


# ============================================================
# STEP 5: NUMPY DESCRIPTIVE STATISTICS
# ============================================================

def calculate_score_statistics(scores):
    """
    Calculate descriptive statistics using NumPy.

    Standard deviation uses ddof=0 (population standard deviation).
    Quartiles use NumPy's default percentile interpolation method.
    """
    try:
        values = np.asarray(scores, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Scores must be numeric.") from exc

    if values.size == 0:
        raise ValueError("At least one score is required.")

    if not np.isfinite(values).all():
        raise ValueError("Scores must be finite numeric values.")

    if ((values < 0) | (values > 100)).any():
        raise ValueError("Scores must be between 0 and 100.")

    return {
        "count": int(values.size),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std_dev": float(np.std(values, ddof=0)),
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
        "q1": float(np.percentile(values, 25)),
        "q3": float(np.percentile(values, 75)),
    }


# ============================================================
# STEP 5: SCORE DISTRIBUTION
# ============================================================

def get_score_distribution(scores, bins=None):
    """
    Count scores in non-overlapping intervals.

    Default intervals:
    0-<50, 50-<60, 60-<70, 70-<80, 80-<90, and 90-100.
    The final interval includes 100.
    """
    try:
        values = np.asarray(scores, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("Scores must be numeric.") from exc

    if values.size == 0:
        raise ValueError("At least one score is required.")

    if not np.isfinite(values).all():
        raise ValueError("Scores must be finite numeric values.")

    if ((values < 0) | (values > 100)).any():
        raise ValueError("Scores must be between 0 and 100.")

    if bins is None:
        intervals = [
            ("0-49", 0, 50, False),
            ("50-59", 50, 60, False),
            ("60-69", 60, 70, False),
            ("70-79", 70, 80, False),
            ("80-89", 80, 90, False),
            ("90-100", 90, 100, True),
        ]
    else:
        intervals = []
        for lower, upper in bins:
            if lower > upper:
                raise ValueError(
                    "Bin lower bound cannot exceed upper bound."
                )
            intervals.append(
                (f"{lower}-{upper}", lower, upper, upper == 100)
            )

    distribution = {}

    for label, lower, upper, include_upper in intervals:
        if include_upper:
            mask = (values >= lower) & (values <= upper)
        else:
            mask = (values >= lower) & (values < upper)

        distribution[label] = int(mask.sum())

    return distribution


# ============================================================
# STEP 5: SUBJECT COMPARISON
# ============================================================

def compare_subjects(df):
    """Compare subject means, medians, variability, minima and maxima."""
    missing = set(SCORE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing score columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Cannot compare subjects in an empty dataset.")

    rows = []

    for subject in SCORE_COLUMNS:
        values = pd.to_numeric(df[subject], errors="coerce")

        if values.isna().any():
            raise ValueError(
                f"Subject '{subject}' contains missing or non-numeric values."
            )

        if not np.isfinite(values.to_numpy(dtype=float)).all():
            raise ValueError(
                f"Subject '{subject}' contains non-finite values."
            )

        stats = calculate_score_statistics(values)

        rows.append({
            "subject": subject,
            "mean": stats["mean"],
            "median": stats["median"],
            "std_dev": stats["std_dev"],
            "minimum": stats["minimum"],
            "maximum": stats["maximum"],
        })

    return pd.DataFrame(rows)


# ============================================================
# STEP 5: IQR OUTLIER DETECTION
# ============================================================

def detect_score_outliers(df):
    """
    Detect potential outliers in each subject using the IQR rule.

    An observation is flagged if it is below Q1 - 1.5*IQR
    or above Q3 + 1.5*IQR. A flagged value is not necessarily
    an error; it should be investigated in context.
    """
    missing = {"student_id", *SCORE_COLUMNS} - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df.empty:
        raise ValueError("Cannot detect outliers in an empty dataset.")

    outliers = []

    for subject in SCORE_COLUMNS:
        values = pd.to_numeric(df[subject], errors="coerce")

        if values.isna().any():
            raise ValueError(
                f"Subject '{subject}' contains missing or non-numeric values."
            )

        if not np.isfinite(values.to_numpy(dtype=float)).all():
            raise ValueError(
                f"Subject '{subject}' contains non-finite values."
            )

        if ((values < 0) | (values > 100)).any():
            raise ValueError(
                f"Subject '{subject}' has scores outside 0-100."
            )

        q1 = float(values.quantile(0.25))
        q3 = float(values.quantile(0.75))
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (values < lower_bound) | (values > upper_bound)

        for index in df.index[mask]:
            outliers.append({
                "student_id": df.loc[index, "student_id"],
                "subject": subject,
                "score": float(values.loc[index]),
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
            })

    return pd.DataFrame(
        outliers,
        columns=[
            "student_id",
            "subject",
            "score",
            "lower_bound",
            "upper_bound",
        ],
    )


# ============================================================
# STEP 5: COMPLETE ADVANCED ANALYSIS
# ============================================================

def create_advanced_analysis(df):
    """Combine basic analysis and advanced statistical results."""
    if df.empty:
        raise ValueError("Cannot analyze an empty dataset.")

    scored_df = add_performance_metrics(df)

    subject_comparison = compare_subjects(scored_df)

    subject_statistics = {
        subject: calculate_score_statistics(scored_df[subject])
        for subject in SCORE_COLUMNS
    }

    return {
        "class_summary": analyze_performance(scored_df),
        "subject_comparison": subject_comparison,
        "subject_statistics": subject_statistics,
        "average_score_statistics": calculate_score_statistics(
            scored_df["average_score"]
        ),
        "average_score_distribution": get_score_distribution(
            scored_df["average_score"]
        ),
        "outliers": detect_score_outliers(scored_df),
    }


# ============================================================
# RUN BASIC ANALYSIS DIRECTLY
# ============================================================

if __name__ == "__main__":
    students = load_student_data()
    students = add_performance_metrics(students)
    report = analyze_performance(students)

    print("STUDENT PERFORMANCE SUMMARY")
    print("=" * 40)
    print(f"Number of students: {report['student_count']}")
    print(f"Class average: {report['class_average']:.2f}")
    print(f"Highest average: {report['highest_average']:.2f}")
    print(f"Lowest average: {report['lowest_average']:.2f}")
    print(
        "Average study hours per day: "
        f"{report['average_study_hours']:.2f}"
    )
    print(f"Average attendance: {report['average_attendance']:.2f}%")

    print("\nSubject averages:")
    for subject, average in report["subject_averages"].items():
        print(f"  {subject}: {average:.2f}")

    print("\nGrade distribution:")
    for grade, count in report["grade_distribution"].items():
        print(f"  {grade}: {count}")

    print("\nTop-performing student(s):")
    for student in report["top_students"]:
        print(
            f"  {student['student_id']}: "
            f"{student['average_score']:.2f} ({student['grade']})"
        )

    correlation = report["study_hours_score_correlation"]
    print("\nStudy-hours/average-score correlation:")
    if correlation is None:
        print("  Not defined for these data.")
    else:
        print(f"  {correlation:.3f}")
