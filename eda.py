# -*- coding: utf-8 -*-
"""EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tthfqbiTs-TK6xTKCkS6xucf2Kvj0PsQ

# **Exploratory Data Analysis (EDA)**

*   Load the hospital_readmissions.csv dataset and perform initial data exploration.
*   Summarize the dataset with descriptive statistics.
*   Visualize the data to identify patterns, trends, and potential outliers.
*   Handle missing values and perform data cleaning as necessary.
*   Generate a report summarizing your findings.
"""

# !pip install pandas-profiling

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### Load the hospital_readmissions.csv dataset and perform initial data exploration.
file_path = '/content/hospital_readmissions.csv'
data = pd.read_csv(file_path)
data_head = data.head()
data_info = data.info()

# Summarize the dataset with descriptive statistics.
data_description = data.describe(include='all')
missing_values = data.isnull().sum()


print(data_head)
print(data_info)
print(data_description)
print("Missing values:\n", missing_values)

# only numeric columns for correlation, excluding 'Patient_ID'
numeric_data = data.select_dtypes(include=['number']).drop(columns=['Patient_ID'], errors='ignore')

plt.figure(figsize=(10, 8))
sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

numerical_cols = ['Age', 'Num_Lab_Procedures', 'Num_Medications',
                  'Num_Outpatient_Visits', 'Num_Inpatient_Visits',
                  'Num_Emergency_Visits', 'Num_Diagnoses']

n_cols = 3
n_rows = (len(numerical_cols) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(numerical_cols):
    sns.histplot(data[col], bins=20, kde=True, ax=axes[i])
    axes[i].set_title(f'Distribution of {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Frequency')

for i in range(len(numerical_cols), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.show()

numerical_cols = ['Age', 'Num_Lab_Procedures', 'Num_Medications',
                  'Num_Outpatient_Visits', 'Num_Inpatient_Visits',
                  'Num_Emergency_Visits', 'Num_Diagnoses']

n_cols = 3
n_rows = (len(numerical_cols) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(numerical_cols):
    sns.boxplot(data[col], ax=axes[i])
    axes[i].set_title(f'Boxplot of {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Value')

for i in range(len(numerical_cols), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.show()

categorical_cols = ['Gender', 'Admission_Type', 'Diagnosis', 'A1C_Result']

n_cols = 2
n_rows = (len(categorical_cols) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 8))
axes = axes.flatten()

for i, col in enumerate(categorical_cols):
    sns.countplot(x=data[col], ax=axes[i])
    axes[i].set_title(f'Count Plot of {col}')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Count')
    axes[i].tick_params(axis='x', rotation=45)

for i in range(len(categorical_cols), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.show()

# Check for missing values percentage
missing_percentage = data.isnull().mean() * 100
print("Missing percentage for each column:\n", missing_percentage)

# Remove the columns with missing percentage > than 20%
columns_to_drop = missing_percentage[missing_percentage > 20].index.tolist()
data.drop(columns=columns_to_drop, inplace=True)

print(f"Columns dropped due to >20% missing values: {columns_to_drop}")
print(f"Shape of the dataset after dropping columns: {data.shape}")

# Outliers
def impute_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_condition = (df[column] < lower_bound) | (df[column] > upper_bound)
    median_value = df[column].median()
    df.loc[outlier_condition, column] = median_value
    return median_value

# Numerical Variables / Impute the missing values or outliers using median
numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
for col in numerical_cols:
    outlier_median = impute_outliers_iqr(data, col)
    print(f"Outliers in '{col}' were replaced with the median: {outlier_median}")

    data[col].fillna(data[col].median(), inplace=True)
    print(f"Missing values in '{col}' were filled with the median: {data[col].median()}")

# Categorical Variables / Impute the missing values using mode
categorical_cols = data.select_dtypes(include=['object']).columns
for col in categorical_cols:
    mode_value = data[col].mode()[0]
    data[col].fillna(mode_value, inplace=True)
    print(f"Missing values in '{col}' were filled with the mode: {mode_value}")

missing_values_after = data.isnull().sum()
print("Missing values after cleaning:\n", missing_values_after[missing_values_after > 0])

data.to_pickle('data_EDA.pkl')