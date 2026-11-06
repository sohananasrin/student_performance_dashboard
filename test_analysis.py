
import math

from analysis import (
    validate_score,
    validate_study_hours,
    calculate_average,
    get_grade,
    load_student_data,
    add_performance_metrics,
    analyze_performance,
)


# 1. Test score validation
assert validate_score(0)
assert validate_score(100)
assert validate_score(75.5)
assert not validate_score(-1)
assert not validate_score(101)
assert not validate_score("abc")
assert not validate_score(float("nan"))
assert not validate_score(True)


# 2. Test study-hour validation
assert validate_study_hours(0)
assert validate_study_hours(8.5)
assert validate_study_hours(24)
assert not validate_study_hours(-1)
assert not validate_study_hours(25)
assert not validate_study_hours(float("nan"))


# 3. Test average calculation
assert calculate_average([70, 80, 90]) == 80

try:
    calculate_average([])
except ValueError:
    pass
else:
    raise AssertionError("Empty score list should be rejected.")

try:
    calculate_average([70, 105])
except ValueError:
    pass
else:
    raise AssertionError("Invalid score should be rejected.")


# 4. Test grade boundaries
assert get_grade(95) == "A+"
assert get_grade(80) == "A"
assert get_grade(70) == "B"
assert get_grade(60) == "C"
assert get_grade(50) == "D"
assert get_grade(49.99) == "F"

try:
    get_grade(101)
except ValueError:
    pass
else:
    raise AssertionError("Invalid average should be rejected.")


# 5. Test CSV loading and calculated metrics
df = load_student_data()
assert len(df) == 20

result = add_performance_metrics(df)
assert "average_score" in result.columns
assert "grade" in result.columns
assert len(result) == 20

# Confirm the original DataFrame was not modified.
assert "average_score" not in df.columns

# Check the first student: (48 + 45 + 52) / 3
assert math.isclose(
    result.loc[0, "average_score"],
    145 / 3,
)

assert result.loc[0, "grade"] == "F"


# 6. Test the performance summary
report = analyze_performance(df)

assert report["student_count"] == 20
assert math.isclose(report["average_study_hours"], 4.325)
assert len(report["top_students"]) >= 1
assert sum(report["grade_distribution"].values()) == 20

print("All Step 3 tests passed successfully!")
