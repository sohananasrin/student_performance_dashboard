
"""Tests for the dashboard visualization functions."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from analysis import load_student_data
from visualizations import (
    plot_study_hours_vs_average_score,
    plot_subject_comparison,
    plot_average_score_histogram,
    plot_grade_distribution,
    plot_outlier_visualization,
    create_all_visualizations,
)


# Test 1: Every chart is saved successfully.
df = load_student_data()

with TemporaryDirectory() as temp_dir:
    paths = create_all_visualizations(df, temp_dir)

    expected_names = {
        "study_hours_vs_average_score.png",
        "subject_comparison.png",
        "average_score_histogram.png",
        "grade_distribution.png",
        "outlier_visualization.png",
    }

    assert len(paths) == 5
    assert {Path(path).name for path in paths} == expected_names

    for path in paths:
        assert Path(path).exists(), f"Chart was not saved: {path}"
        assert Path(path).stat().st_size > 0, f"Chart is empty: {path}"


# Test 2: Each individual plotting function returns an existing file.
with TemporaryDirectory() as temp_dir:
    plotting_functions = [
        plot_study_hours_vs_average_score,
        plot_subject_comparison,
        plot_average_score_histogram,
        plot_grade_distribution,
        plot_outlier_visualization,
    ]

    for function in plotting_functions:
        path = function(df, temp_dir)
        assert Path(path).exists()
        assert Path(path).stat().st_size > 0


# Test 3: Outlier visualization handles a dataset with no outliers.
# All scores are identical, so no score should be flagged as an outlier.
no_outlier_df = pd.DataFrame({
    "student_id": ["A", "B", "C", "D"],
    "study_hours": [2, 3, 4, 5],
    "python_score": [70, 70, 70, 70],
    "dsa_score": [70, 70, 70, 70],
    "math_score": [70, 70, 70, 70],
    "attendance_pct": [80, 80, 80, 80],
})

with TemporaryDirectory() as temp_dir:
    path = plot_outlier_visualization(no_outlier_df, temp_dir)
    assert Path(path).exists()
    assert Path(path).stat().st_size > 0


print("All visualization tests passed successfully!")
