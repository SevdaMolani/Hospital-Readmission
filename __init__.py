# __init__.py

"""
Hospital Readmission Package

This package contains tools for analyzing hospital readmission data, 
including data preprocessing, feature engineering, and model training.

"""

# Importing relevant functions or classes for easier access
from .eda import perform_eda
from .modeling_preprocessing import modeling_pipeline
import app.py

perform_eda('/content/hospital_readmissions.csv')
performance_table, classification_report_table = modeling_pipeline()
print("Performance Table:")
print(performance_table)
print("\nClassification Report Table:")
print(classification_report_table)

# Example CURL commands to test the API (commented out in production)
!curl -X POST "http://localhost:8080/predict" -H "Content-Type: application/json" -d '{"Age": 50, "Gender": "Male", "Admission_Type": "Emergency", "Diagnosis": "Diabetes", "Num_Lab_Procedures": 5, "Num_Medications": 2, "Num_Outpatient_Visits": 1, "Num_Inpatient_Visits": 0, "Num_Emergency_Visits": 1, "Num_Diagnoses": 2}'
!curl http://localhost:8080/health
