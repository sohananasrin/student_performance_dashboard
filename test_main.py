
"""Integration test for the complete dashboard."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from main import main
from visualizations import OUTPUT_DIR


# Run the complete project and capture its console output.
captured_output = StringIO()

with redirect_stdout(captured_output):
    main()

output = captured_output.getvalue()

# Verify that the main program reports successful completion.
assert "STUDENT PERFORMANCE DASHBOARD" in output
assert "Dashboard analysis completed successfully." in output
assert "Successfully loaded 20 student records." in output

# Verify that the expected charts and reports were generated.
expected_files = [
    "study_hours_vs_average_score.png",
    "subject_comparison.png",
    "average_score_histogram.png",
    "grade_distribution.png",
    "outlier_visualization.png",
    "student_performance_results.csv",
    "subject_comparison.csv",
    "potential_outliers.csv",
    "class_summary.txt",
]

for filename in expected_files:
    file_path = OUTPUT_DIR / filename
    assert file_path.exists(), f"Missing output file: {filename}"
    assert file_path.stat().st_size > 0, f"Empty output file: {filename}"

print("All main program integration tests passed successfully!")
