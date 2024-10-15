# __init__.py

"""
Hospital Readmission Package

This package contains tools for analyzing hospital readmission data, 
including data preprocessing, feature engineering, and model training.

Modules:
- data_preprocessing: Functions for cleaning and preparing data.
- feature_engineering: Tools for creating features from raw data.
- model_training: Functions for training and evaluating machine learning models.
"""

# Importing relevant functions or classes for easier access
from .EDA import (
    perform_eda
)


from .model_training import (
    modeling_pipeline
)
