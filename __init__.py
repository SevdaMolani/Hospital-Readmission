# __init__.py

"""
Hospital Readmission Package

This package contains tools for analyzing hospital readmission data, 
including data preprocessing, feature engineering, and model training.

"""

# Importing relevant functions or classes for easier access
from .eda import perform_eda
from .modeling_preprocessing import modeling_pipeline


perform_eda('/content/hospital_readmissions.csv')
performance_table, classification_report_table = modeling_pipeline()
print("Performance Table:")
print(performance_table)
print("\nClassification Report Table:")
print(classification_report_table)

