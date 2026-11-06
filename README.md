
# Student Performance and Study-Hours Dashboard

## 1. Project Overview

The Student Performance and Study-Hours Dashboard is a Python software
project that analyzes student academic performance using study hours,
subject scores, and attendance.

The project uses data analysis, object-oriented programming, statistical
methods, and data visualization to generate useful insights from student
records.

It includes a command-line analysis program and an interactive dashboard
built with Streamlit.

## 2. Objectives

- Analyze student performance across Python, DSA, and Mathematics.
- Calculate individual average scores and grade categories.
- Examine the relationship between study hours and academic performance.
- Summarize class-level performance and attendance.
- Compare average scores and variability across subjects.
- Identify potential score outliers using the interquartile range method.
- Generate visualizations and downloadable reports.
- Provide an interactive interface for filtering and exploring student data.

## 3. Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Streamlit
- CSV for data storage
- unittest-style assertion scripts for testing

## 4. Project Structure

```text
student_performance_dashboard/
├── data/
│   └── students.csv
├── output/
├── main.py
├── app.py
├── analysis.py
├── student_record.py
├── visualizations.py
├── test_setup.py
├── test_data.py
├── test_analysis.py
├── test_student_record.py
├── test_advanced_analysis.py
├── test_visualizations.py
├── test_main.py
├── requirements.txt
└── README.md
```

The `output/` directory is created or populated when the application runs.

## 5. Main Features

### Data Validation
Checks the required CSV columns, unique student IDs, numeric values,
score limits, attendance limits, and study-hour limits.

### Performance Analysis
Calculates student averages, grade categories, class averages, highest
and lowest averages, subject averages, and grade distributions.

### Object-Oriented Programming
The `StudentRecord` class represents an individual student and validates
the student's scores, attendance, and study hours.

### Advanced Statistical Analysis
Uses NumPy and Pandas to calculate:
- Mean and median
- Population standard deviation
- Minimum and maximum scores
- First and third quartiles
- Subject-wise comparisons
- Score distributions
- Potential outliers using the IQR rule

### Data Visualization
Matplotlib generates:
1. Study hours versus average score scatter plot
2. Subject comparison bar chart
3. Average score histogram
4. Grade distribution bar chart
5. Potential outlier visualization

### Interactive Dashboard
The Streamlit application provides:
- Class performance metrics
- Grade and score filters
- Attendance filtering
- Student ID search
- Subject analysis
- Outlier analysis
- CSV and text downloads

## 6. Installation Requirements

Install Python 3.10 or a compatible newer version, then open a terminal
inside the project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## 7. How to Run

### Run the command-line analysis

```powershell
python main.py
```

### Run the interactive dashboard

```powershell
python -m streamlit run app.py
```

### Run the visualization module independently

```powershell
python visualizations.py
```

## 8. Running the Tests

Run the test scripts individually:

```powershell
python test_setup.py
python test_data.py
python test_analysis.py
python test_student_record.py
python test_advanced_analysis.py
python test_visualizations.py
python test_main.py
```

The tests check dependencies, data loading, validation, calculations,
statistical analysis, chart generation, and integration.

## 9. Output Files

The application generates charts and reports in the `output/` directory.

Typical outputs include:

- `study_hours_vs_average_score.png`
- `subject_comparison.png`
- `average_score_histogram.png`
- `grade_distribution.png`
- `outlier_visualization.png`
- `student_performance_results.csv`
- `subject_comparison.csv`
- `potential_outliers.csv`
- `class_summary.txt`

## 10. Dataset

The project uses a CSV dataset containing fictional student records.
The records include student IDs, daily study hours, Python scores,
DSA scores, Mathematics scores, and attendance percentages.

The dataset is intended for educational demonstration and does not
represent real student records.

## 11. Limitations

- The supplied dataset is small and synthetic.
- Correlation does not establish causation.
- IQR-based outlier detection identifies unusual values, not necessarily
  errors.
- The current application reads data from a local CSV file.
- The grade thresholds are predefined and may need adjustment for
  different academic institutions.

## 12. Future Enhancements

Possible improvements include:
- Uploading custom student datasets through the dashboard
- Exporting PDF reports
- Comparing multiple semesters
- Adding predictive models for academic performance
- Improving accessibility and dashboard design
- Adding a database for persistent record management

## 13. Conclusion

The project demonstrates how Python can be used to validate data,
perform statistical analysis, apply object-oriented programming,
visualize results, and build an interactive data application.

It combines core Python programming with practical data analysis
techniques in a single software project.
