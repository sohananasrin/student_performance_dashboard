
from analysis import load_student_data, create_advanced_analysis

df = load_student_data()
results = create_advanced_analysis(df)

print("\nSUBJECT COMPARISON")
print(results["subject_comparison"].round(2).to_string(index=False))

print("\nAVERAGE SCORE STATISTICS")
for name, value in results["average_score_statistics"].items():
    print(f"{name}: {value:.2f}" if isinstance(value, float)
          else f"{name}: {value}")

print("\nAVERAGE SCORE DISTRIBUTION")
for interval, count in results["average_score_distribution"].items():
    print(f"{interval}: {count}")

print("\nPOTENTIAL SUBJECT-SCORE OUTLIERS")
if results["outliers"].empty:
    print("No outliers detected.")
else:
    print(results["outliers"].round(2).to_string(index=False))
