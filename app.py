
"""Interactive Streamlit dashboard for student performance."""

from pathlib import Path

import pandas as pd
import streamlit as st

from analysis import (
    DATA_FILE,
    SCORE_COLUMNS,
    add_performance_metrics,
    load_student_data,
    analyze_performance,
    compare_subjects,
    detect_score_outliers,
)
from visualizations import (
    OUTPUT_DIR,
    create_all_visualizations,
)


# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Student Performance Dashboard")
st.caption(
    "Explore study hours, academic scores, attendance, and grade patterns."
)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

@st.cache_data
def get_student_data():
    """Load and cache the source dataset."""
    return load_student_data(DATA_FILE)


try:
    raw_df = get_student_data()
    students = add_performance_metrics(raw_df)
except Exception as error:
    st.error(f"Could not load student data: {error}")
    st.stop()


# ------------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------------

st.sidebar.header("Filter Students")

available_grades = ["A+", "A", "B", "C", "D", "F"]

selected_grades = st.sidebar.multiselect(
    "Select grades",
    options=available_grades,
    default=available_grades,
)

score_min = float(students["average_score"].min())
score_max = float(students["average_score"].max())

if score_min == score_max:
    selected_score_range = (score_min, score_max)
    st.sidebar.caption("All students have the same average score.")
else:
    selected_score_range = st.sidebar.slider(
        "Average score range",
        min_value=0.0,
        max_value=100.0,
        value=(
            max(0.0, score_min),
            min(100.0, score_max),
        ),
        step=1.0,
    )

min_attendance = st.sidebar.slider(
    "Minimum attendance (%)",
    min_value=0,
    max_value=100,
    value=0,
    step=5,
)

filtered_df = students[
    students["grade"].isin(selected_grades)
    & students["average_score"].between(
        selected_score_range[0],
        selected_score_range[1],
    )
    & (students["attendance_pct"] >= min_attendance)
].copy()

st.sidebar.divider()
st.sidebar.write(f"Matching students: **{len(filtered_df)}**")
st.sidebar.write(f"Total students: **{len(students)}**")


# ------------------------------------------------------------
# HANDLE EMPTY FILTER RESULTS
# ------------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No students match these filters. Change the selections "
        "in the sidebar to view results."
    )
    st.stop()


# ------------------------------------------------------------
# KEY PERFORMANCE INDICATORS
# ------------------------------------------------------------

summary = analyze_performance(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Students",
    summary["student_count"],
)

col2.metric(
    "Class Average",
    f"{summary['class_average']:.2f}/100",
)

col3.metric(
    "Avg. Study Hours",
    f"{summary['average_study_hours']:.2f} hrs/day",
)

col4.metric(
    "Avg. Attendance",
    f"{summary['average_attendance']:.1f}%",
)


# ------------------------------------------------------------
# TABS
# ------------------------------------------------------------

overview_tab, students_tab, subjects_tab, outliers_tab = st.tabs(
    [
        "Overview",
        "Student Records",
        "Subject Analysis",
        "Outlier Analysis",
    ]
)


# ------------------------------------------------------------
# OVERVIEW TAB
# ------------------------------------------------------------

with overview_tab:
    st.subheader("Performance Overview")

    correlation = summary["study_hours_score_correlation"]

    if correlation is not None:
        st.write(
            f"**Study-hours/average-score correlation:** "
            f"{correlation:.3f}"
        )
        st.caption(
            "Correlation describes an association; it does not establish "
            "that additional study hours cause higher scores."
        )

    st.subheader("Grade Distribution")

    grade_order = ["A+", "A", "B", "C", "D", "F"]

    grade_counts = (
        filtered_df["grade"]
        .value_counts()
        .reindex(grade_order, fill_value=0)
        .rename_axis("Grade")
        .reset_index(name="Number of Students")
    )

    st.bar_chart(
        grade_counts.set_index("Grade"),
        y="Number of Students",
    )

    st.subheader("Study Hours vs Average Score")

    scatter_data = filtered_df[
        ["student_id", "study_hours", "average_score"]
    ].set_index("student_id")

    st.scatter_chart(
        scatter_data,
        x="study_hours",
        y="average_score",
    )


# ------------------------------------------------------------
# STUDENT RECORDS TAB
# ------------------------------------------------------------

with students_tab:
    st.subheader("Student Records")

    search_id = st.text_input(
        "Search by Student ID",
        placeholder="For example, S001",
    ).strip().lower()

    display_df = filtered_df.copy()

    if search_id:
        display_df = display_df[
            display_df["student_id"]
            .astype(str)
            .str.lower()
            .str.contains(search_id, na=False)
        ]

    display_columns = [
        "student_id",
        "study_hours",
        "python_score",
        "dsa_score",
        "math_score",
        "attendance_pct",
        "average_score",
        "grade",
    ]

    st.dataframe(
        display_df[display_columns].round(2),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = display_df[display_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download displayed student records as CSV",
        data=csv_data,
        file_name="filtered_student_records.csv",
        mime="text/csv",
    )


# ------------------------------------------------------------
# SUBJECT ANALYSIS TAB
# ------------------------------------------------------------

with subjects_tab:
    st.subheader("Subject Performance Comparison")

    subject_comparison = compare_subjects(filtered_df)

    subject_labels = {
        "python_score": "Python",
        "dsa_score": "DSA",
        "math_score": "Mathematics",
    }

    chart_df = subject_comparison.copy()
    chart_df["subject"] = chart_df["subject"].map(subject_labels)

    st.bar_chart(
        chart_df.set_index("subject"),
        y="mean",
    )

    st.write("**Detailed subject statistics**")

    st.dataframe(
        chart_df.round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Standard deviation is population standard deviation for the "
        "students included in the selected dataset."
    )


# ------------------------------------------------------------
# OUTLIER ANALYSIS TAB
# ------------------------------------------------------------

with outliers_tab:
    st.subheader("Potential Subject-Score Outliers")

    outliers = detect_score_outliers(filtered_df)

    if outliers.empty:
        st.info(
            "No potential outliers were detected in the selected students."
        )
    else:
        st.warning(
            f"{len(outliers)} potential subject-score outlier(s) detected."
        )

        st.dataframe(
            outliers.round(2),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "The IQR rule flags unusual values for review. A flagged score "
        "is not automatically incorrect."
    )


# ------------------------------------------------------------
# OPTIONAL EXPORTS
# ------------------------------------------------------------

st.divider()
st.subheader("Export Reports")

report_col1, report_col2 = st.columns(2)

with report_col1:
    summary_lines = [
        "STUDENT PERFORMANCE DASHBOARD",
        "=" * 35,
        f"Students included: {summary['student_count']}",
        f"Class average: {summary['class_average']:.2f}",
        f"Average study hours: {summary['average_study_hours']:.2f}",
        f"Average attendance: {summary['average_attendance']:.2f}%",
        "",
        "Grade distribution:",
    ]

    for grade, count in summary["grade_distribution"].items():
        summary_lines.append(f"{grade}: {count}")

    summary_text = "\n".join(summary_lines)

    st.download_button(
        "Download class summary",
        data=summary_text,
        file_name="class_summary.txt",
        mime="text/plain",
    )

with report_col2:
    st.download_button(
        "Download subject statistics",
        data=subject_comparison.to_csv(index=False).encode("utf-8"),
        file_name="subject_comparison.csv",
        mime="text/csv",
    )

st.caption("Data source: data/students.csv")
