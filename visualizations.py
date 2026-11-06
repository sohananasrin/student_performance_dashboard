
"""Matplotlib visualizations for the Student Performance Dashboard."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save plots without opening GUI windows.

import matplotlib.pyplot as plt
import numpy as np

from analysis import (
    SCORE_COLUMNS,
    add_performance_metrics,
    compare_subjects,
    detect_score_outliers,
)


# Save all charts inside the project's output folder.
OUTPUT_DIR = Path(__file__).parent / "output"

SUBJECT_LABELS = {
    "python_score": "Python",
    "dsa_score": "DSA",
    "math_score": "Mathematics",
}


def _prepare_output_dir(output_dir):
    """Create the output directory if it does not exist."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def plot_study_hours_vs_average_score(df, output_dir=OUTPUT_DIR):
    """Create a scatter plot of daily study hours versus average score."""
    output_dir = _prepare_output_dir(output_dir)
    scored_df = add_performance_metrics(df)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(
        scored_df["study_hours"],
        scored_df["average_score"],
        alpha=0.8,
        edgecolors="black",
    )

    ax.set_title("Study Hours vs Average Score")
    ax.set_xlabel("Study Hours per Day")
    ax.set_ylabel("Average Score")
    ax.set_ylim(0, 105)
    ax.grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()
    path = output_dir / "study_hours_vs_average_score.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def plot_subject_comparison(df, output_dir=OUTPUT_DIR):
    """Create a bar chart comparing mean scores across subjects."""
    output_dir = _prepare_output_dir(output_dir)
    comparison = compare_subjects(df)

    labels = [
        SUBJECT_LABELS.get(subject, subject)
        for subject in comparison["subject"]
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(labels, comparison["mean"])

    ax.set_title("Average Score by Subject")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Mean Score")
    ax.set_ylim(0, 105)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    ax.bar_label(bars, fmt="%.1f", padding=3)

    fig.tight_layout()
    path = output_dir / "subject_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def plot_average_score_histogram(df, output_dir=OUTPUT_DIR):
    """Show how students' average scores are distributed."""
    output_dir = _prepare_output_dir(output_dir)
    scored_df = add_performance_metrics(df)

    scores = scored_df["average_score"].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        scores,
        bins=np.arange(0, 111, 10),
        edgecolor="black",
        alpha=0.8,
    )

    ax.set_title("Distribution of Student Average Scores")
    ax.set_xlabel("Average Score Range")
    ax.set_ylabel("Number of Students")
    ax.set_xlim(0, 100)
    ax.set_xticks(np.arange(0, 101, 10))
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    path = output_dir / "average_score_histogram.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def plot_grade_distribution(df, output_dir=OUTPUT_DIR):
    """Create a bar chart showing the number of students in each grade."""
    output_dir = _prepare_output_dir(output_dir)
    scored_df = add_performance_metrics(df)

    grade_order = ["A+", "A", "B", "C", "D", "F"]
    grade_counts = (
        scored_df["grade"]
        .value_counts()
        .reindex(grade_order, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(grade_counts.index, grade_counts.values)

    ax.set_title("Student Grade Distribution")
    ax.set_xlabel("Grade")
    ax.set_ylabel("Number of Students")
    ax.set_ylim(0, max(1, int(grade_counts.max()) + 2))
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    ax.bar_label(bars, padding=3)

    fig.tight_layout()
    path = output_dir / "grade_distribution.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def plot_outlier_visualization(df, output_dir=OUTPUT_DIR):
    """
    Visualize potential subject-score outliers detected by the IQR rule.

    This chart displays only flagged scores. If no outliers are found,
    it displays an explanatory message rather than failing.
    """
    output_dir = _prepare_output_dir(output_dir)
    outliers = detect_score_outliers(df)

    fig, ax = plt.subplots(figsize=(9, 5))

    if outliers.empty:
        ax.text(
            0.5,
            0.5,
            "No potential outliers detected",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=12,
        )
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        subject_order = list(SCORE_COLUMNS)
        subject_positions = {
            subject: position
            for position, subject in enumerate(subject_order)
        }

        x_positions = [
            subject_positions[subject]
            for subject in outliers["subject"]
        ]

        ax.scatter(
            x_positions,
            outliers["score"],
            s=90,
            marker="x",
            linewidths=2,
            label="Potential outlier",
        )

        # Label each flagged point with its student ID.
        for x, (_, row) in zip(x_positions, outliers.iterrows()):
            ax.annotate(
                str(row["student_id"]),
                (x, row["score"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
            )

        ax.set_xticks(range(len(subject_order)))
        ax.set_xticklabels(
            [SUBJECT_LABELS.get(subject, subject)
             for subject in subject_order]
        )
        ax.set_ylabel("Subject Score")
        ax.set_ylim(0, 105)
        ax.legend()

    ax.set_title("Potential Subject-Score Outliers")
    ax.set_xlabel("Subject")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout()
    path = output_dir / "outlier_visualization.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return path


def create_all_visualizations(df, output_dir=OUTPUT_DIR):
    """Generate all five charts and return their saved file paths."""
    functions = [
        plot_study_hours_vs_average_score,
        plot_subject_comparison,
        plot_average_score_histogram,
        plot_grade_distribution,
        plot_outlier_visualization,
    ]

    return [
        function(df, output_dir)
        for function in functions
    ]


if __name__ == "__main__":
    from analysis import load_student_data

    students = load_student_data()
    saved_paths = create_all_visualizations(students)

    print("VISUALIZATIONS CREATED")
    print("=" * 40)

    for path in saved_paths:
        print(f"Saved: {path}")
