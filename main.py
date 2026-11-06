
"""Main entry point for the Student Performance Dashboard."""

from analysis import (
    load_student_data,
    add_performance_metrics,
    analyze_performance,
    create_advanced_analysis,
)
from visualizations import create_all_visualizations


def main():
    """Run the complete student performance analysis pipeline."""

    print("=" * 55)
    print("       STUDENT PERFORMANCE DASHBOARD")
    print("=" * 55)

    # 1. Load the dataset.
    print("\n[1/5] Loading and validating student data...")
    students = load_student_data()
    print(f"Successfully loaded {len(students)} student records.")

    # 2. Calculate individual student metrics.
    print("\n[2/5] Calculating student performance metrics...")
    scored_students = add_performance_metrics(students)
    print("Average scores and grades calculated.")

    # 3. Display the class summary.
    print("\n[3/5] Generating class performance summary...")
    summary = analyze_performance(scored_students)

    print("\nCLASS SUMMARY")
    print("-" * 40)
    print(f"Number of students: {summary['student_count']}")
    print(f"Class average: {summary['class_average']:.2f}")
    print(f"Highest average: {summary['highest_average']:.2f}")
    print(f"Lowest average: {summary['lowest_average']:.2f}")
    print(
        f"Average study hours/day: "
        f"{summary['average_study_hours']:.2f}"
    )
    print(f"Average attendance: {summary['average_attendance']:.2f}%")

    print("\nSUBJECT AVERAGES")
    for subject, average in summary["subject_averages"].items():
        print(f"{subject}: {average:.2f}")

    print("\nGRADE DISTRIBUTION")
    for grade, count in summary["grade_distribution"].items():
        print(f"Grade {grade}: {count} student(s)")

    print("\nTOP-PERFORMING STUDENT(S)")
    for student in summary["top_students"]:
        print(
            f"{student['student_id']}: "
            f"{student['average_score']:.2f} "
            f"(Grade {student['grade']})"
        )

    correlation = summary["study_hours_score_correlation"]
    print("\nSTUDY HOURS AND AVERAGE SCORE")
    if correlation is None:
        print("Correlation cannot be calculated for these data.")
    else:
        print(f"Pearson correlation coefficient: {correlation:.3f}")
        print("Note: Correlation does not prove causation.")

    # 4. Run advanced statistical analysis.
    print("\n[4/5] Running advanced analysis...")
    advanced = create_advanced_analysis(scored_students)

    print("\nADVANCED SCORE STATISTICS")
    stats = advanced["average_score_statistics"]
    print(f"Median average score: {stats['median']:.2f}")
    print(f"Population standard deviation: {stats['std_dev']:.2f}")
    print(f"First quartile (Q1): {stats['q1']:.2f}")
    print(f"Third quartile (Q3): {stats['q3']:.2f}")

    print("\nSUBJECT COMPARISON")
    print(advanced["subject_comparison"].round(2).to_string(index=False))

    print("\nPOTENTIAL OUTLIERS")
    outliers = advanced["outliers"]
    if outliers.empty:
        print("No potential outliers detected.")
    else:
        print(outliers.round(2).to_string(index=False))

    # 5. Generate and save visualizations and analysis files.
    print("\n[5/5] Generating charts and saving output files...")
    chart_paths = create_all_visualizations(scored_students)

    # Import output locations from the analysis and visualization modules.
    from analysis import DATA_FILE
    from visualizations import OUTPUT_DIR

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    processed_csv = OUTPUT_DIR / "student_performance_results.csv"
    subject_csv = OUTPUT_DIR / "subject_comparison.csv"
    outlier_csv = OUTPUT_DIR / "potential_outliers.csv"
    summary_txt = OUTPUT_DIR / "class_summary.txt"

    scored_students.to_csv(processed_csv, index=False)
    advanced["subject_comparison"].to_csv(subject_csv, index=False)
    outliers.to_csv(outlier_csv, index=False)

    with open(summary_txt, "w", encoding="utf-8") as file:
        file.write("STUDENT PERFORMANCE SUMMARY\n")
        file.write("=" * 40 + "\n")
        file.write(f"Students: {summary['student_count']}\n")
        file.write(f"Class average: {summary['class_average']:.2f}\n")
        file.write(f"Highest average: {summary['highest_average']:.2f}\n")
        file.write(f"Lowest average: {summary['lowest_average']:.2f}\n")
        file.write(
            f"Average study hours: "
            f"{summary['average_study_hours']:.2f}\n"
        )
        file.write(
            f"Average attendance: "
            f"{summary['average_attendance']:.2f}%\n"
        )
        file.write(
            f"Study-hours/score correlation: {correlation}\n"
        )
        file.write("\nGrade distribution:\n")
        for grade, count in summary["grade_distribution"].items():
            file.write(f"{grade}: {count}\n")

    print("\nPROJECT OUTPUTS")
    print("-" * 40)
    for path in chart_paths:
        print(f"Chart: {path}")

    print(f"Processed student data: {processed_csv}")
    print(f"Subject comparison: {subject_csv}")
    print(f"Potential outliers: {outlier_csv}")
    print(f"Class summary report: {summary_txt}")

    print("\nDashboard analysis completed successfully.")
    print("=" * 55)


if __name__ == "__main__":
    main()
