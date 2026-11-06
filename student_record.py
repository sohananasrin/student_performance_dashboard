
"""StudentRecord class for the Student Performance Dashboard."""

from analysis import (
    calculate_average,
    get_grade,
    validate_score,
    validate_study_hours,
)


class StudentRecord:
    """Represent and manage one student's academic record."""

    def __init__(
        self,
        student_id,
        study_hours,
        python_score,
        dsa_score,
        math_score,
        attendance_pct,
    ):
        """Initialize a student record with validated values."""

        student_id = str(student_id).strip()

        if not student_id:
            raise ValueError("Student ID cannot be empty.")

        self._student_id = student_id
        self.study_hours = study_hours
        self.python_score = python_score
        self.dsa_score = dsa_score
        self.math_score = math_score
        self.attendance_pct = attendance_pct

    @property
    def student_id(self):
        """Return the student's identifier."""
        return self._student_id

    @property
    def study_hours(self):
        return self._study_hours

    @study_hours.setter
    def study_hours(self, value):
        if not validate_study_hours(value):
            raise ValueError(
                "Study hours must be between 0 and 24."
            )
        self._study_hours = float(value)

    @property
    def python_score(self):
        return self._python_score

    @python_score.setter
    def python_score(self, value):
        if not validate_score(value):
            raise ValueError(
                "Python score must be between 0 and 100."
            )
        self._python_score = float(value)

    @property
    def dsa_score(self):
        return self._dsa_score

    @dsa_score.setter
    def dsa_score(self, value):
        if not validate_score(value):
            raise ValueError(
                "DSA score must be between 0 and 100."
            )
        self._dsa_score = float(value)

    @property
    def math_score(self):
        return self._math_score

    @math_score.setter
    def math_score(self, value):
        if not validate_score(value):
            raise ValueError(
                "Mathematics score must be between 0 and 100."
            )
        self._math_score = float(value)

    @property
    def attendance_pct(self):
        return self._attendance_pct

    @attendance_pct.setter
    def attendance_pct(self, value):
        if not validate_score(value):
            raise ValueError(
                "Attendance must be between 0 and 100."
            )
        self._attendance_pct = float(value)

    def calculate_average(self):
        """Return the average across the three subjects."""
        scores = [
            self.python_score,
            self.dsa_score,
            self.math_score,
        ]
        return calculate_average(scores)

    def get_grade(self):
        """Return the grade based on the average score."""
        return get_grade(self.calculate_average())

    def get_performance_summary(self):
        """Return a readable summary of this student's performance."""
        return {
            "student_id": self.student_id,
            "study_hours": self.study_hours,
            "python_score": self.python_score,
            "dsa_score": self.dsa_score,
            "math_score": self.math_score,
            "attendance_pct": self.attendance_pct,
            "average_score": self.calculate_average(),
            "grade": self.get_grade(),
        }

    def to_dict(self):
        """Convert the record into a dictionary."""
        return self.get_performance_summary()

    def __str__(self):
        """Return a user-friendly string representation."""
        return (
            f"Student {self.student_id} | "
            f"Average: {self.calculate_average():.2f} | "
            f"Grade: {self.get_grade()}"
        )


if __name__ == "__main__":
    # Demonstration using the first fictional student.
    student = StudentRecord(
        student_id="S001",
        study_hours=2.0,
        python_score=48,
        dsa_score=45,
        math_score=52,
        attendance_pct=68,
    )

    print(student)
    print("\nPerformance summary:")
    print(student.get_performance_summary())
