
import math

from student_record import StudentRecord


def create_sample_student():
    return StudentRecord(
        student_id="S001",
        study_hours=2.0,
        python_score=48,
        dsa_score=45,
        math_score=52,
        attendance_pct=68,
    )


# Test 1: Object creation and attributes
student = create_sample_student()

assert student.student_id == "S001"
assert student.study_hours == 2.0
assert student.python_score == 48.0
assert student.dsa_score == 45.0
assert student.math_score == 52.0
assert student.attendance_pct == 68.0


# Test 2: Average calculation
assert math.isclose(
    student.calculate_average(),
    145 / 3,
)


# Test 3: Grade calculation
assert student.get_grade() == "F"

high_performer = StudentRecord(
    "S002", 5, 90, 92, 94, 95
)
assert high_performer.get_grade() == "A+"


# Test 4: Summary dictionary
summary = student.get_performance_summary()

assert summary["student_id"] == "S001"
assert math.isclose(summary["average_score"], 145 / 3)
assert summary["grade"] == "F"


# Test 5: String representation
assert "S001" in str(student)
assert "Grade: F" in str(student)


# Test 6: Invalid constructor values
invalid_records = [
    ("", 2, 50, 50, 50, 80),
    ("S003", -1, 50, 50, 50, 80),
    ("S003", 2, 101, 50, 50, 80),
    ("S003", 2, 50, -5, 50, 80),
    ("S003", 2, 50, 50, 101, 80),
    ("S003", 2, 50, 50, 50, 101),
]

for record in invalid_records:
    try:
        StudentRecord(*record)
    except ValueError:
        pass
    else:
        raise AssertionError(
            f"Invalid record was accepted: {record}"
        )


# Test 7: Invalid changes must be rejected
try:
    student.python_score = 150
except ValueError:
    pass
else:
    raise AssertionError("Invalid Python score was accepted.")

# The original score should remain unchanged.
assert student.python_score == 48.0


# Test 8: Valid changes should work
student.study_hours = 3.5
student.python_score = 70

assert student.study_hours == 3.5
assert student.python_score == 70.0


print("All StudentRecord tests passed successfully!")
