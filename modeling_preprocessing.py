# -*- coding: utf-8 -*-
"""modeling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tthfqbiTs-TK6xTKCkS6xucf2Kvj0PsQ

# **Modeling**

*   Preprocess the data (e.g., encoding categorical variables, scaling numerical features).
*   Split the data into training and testing sets.
*   Train at least two different machine learning models (e.g., Logistic Regression, Random Forest, XGBoost).
*   Evaluate the models using appropriate metrics (e.g., accuracy, precision, recall, F1-score, ROC-AUC).
*   Select the best-performing model and fine-tune its hyperparameters.
*   Save the final model using a serialization format (e.g., joblib, pickle).
"""


# -*- coding: utf-8 -*-
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

def modeling_pipeline(file_path='df_eda.csv'):
    # Load data
    data = pd.read_csv(file_path)

    # Categorical variables
    categorical_cols = ['Gender', 'Admission_Type', 'Diagnosis']  # 'A1C_Result' has been removed due to high missing values

    # OneHotEncoder
    onehot_encoder = OneHotEncoder(sparse_output=False, drop='first')
    encoded_features = onehot_encoder.fit_transform(data[categorical_cols])

    # Encode 'Readmitted' (Yes/No to 1/0)
    label_encoder = LabelEncoder()
    data['Readmitted'] = label_encoder.fit_transform(data['Readmitted'])

    # Prepare final dataset with both numerical and encoded categorical features
    numerical_cols = ['Age', 'Num_Lab_Procedures', 'Num_Medications',
                      'Num_Outpatient_Visits', 'Num_Inpatient_Visits',
                      'Num_Emergency_Visits', 'Num_Diagnoses']

    # Combine features
    X = pd.concat([data[numerical_cols],
                   pd.DataFrame(encoded_features, columns=onehot_encoder.get_feature_names_out())], axis=1)
    y = data['Readmitted']

    # Scale the numerical variables
    scaler = StandardScaler()
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save encoders and scaler
    joblib.dump(onehot_encoder, 'onehot_encoder.joblib')
    joblib.dump(scaler, 'scaler.joblib')

    # Evaluate models
    def evaluate_models(X_train, X_test, y_train, y_test):
        performance = {}

        # Random Forest Classifier
        rf_model = RandomForestClassifier(random_state=42)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        y_prob = rf_model.predict_proba(X_test)[:, 1]
        performance['Random Forest'] = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'ROC AUC': roc_auc_score(y_test, y_prob),
            'Classification Report': classification_report(y_test, y_pred, output_dict=True)
        }

        # XGBoost Classifier
        xgb_model = XGBClassifier(eval_metric='logloss', random_state=42)
        xgb_model.fit(X_train, y_train)
        y_pred = xgb_model.predict(X_test)
        y_prob = xgb_model.predict_proba(X_test)[:, 1]
        performance['XGBoost'] = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'ROC AUC': roc_auc_score(y_test, y_prob),
            'Classification Report': classification_report(y_test, y_pred, output_dict=True)
        }

        # Logistic Regression
        logistic_model = LogisticRegression(random_state=42, max_iter=1000)
        logistic_model.fit(X_train, y_train)
        y_pred = logistic_model.predict(X_test)
        y_prob = logistic_model.predict_proba(X_test)[:, 1]
        performance['Logistic Regression'] = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'ROC AUC': roc_auc_score(y_test, y_prob),
            'Classification Report': classification_report(y_test, y_pred, output_dict=True)
        }

        # Create performance dataframe
        performance_df = pd.DataFrame.from_dict(
            {model: {'Accuracy': metrics['Accuracy'], 'ROC AUC': metrics['ROC AUC']} for model, metrics in performance.items()},
            orient='index'
        ).round(3)

        # Create classification report dataframe
        report_df = pd.DataFrame()
        for model, metrics in performance.items():
            class_report = metrics['Classification Report']
            class_report_df = pd.DataFrame(class_report).T
            class_report_df = class_report_df.round(3)
            class_report_df['Model'] = model
            report_df = pd.concat([report_df, class_report_df], axis=0)

        return performance_df, report_df

    performance_table, classification_report_table = evaluate_models(X_train, X_test, y_train, y_test)

    # Fine-tune XGBoost
    xgb_model = XGBClassifier(eval_metric='logloss', random_state=42)

    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }

    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='roc_auc', cv=5, verbose=1, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    print("Best Parameters:", {k: round(v, 3) for k, v in best_params.items()})
    print("Best CV Score:", round(best_score, 3))

    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    print("Accuracy:", round(accuracy, 3))
    print("ROC AUC:", round(roc_auc, 3))

    classification_rep = classification_report(y_test, y_pred)
    print(classification_rep)

    joblib.dump(best_model, 'xgb_model.joblib')

    return performance_table, classification_report_table

# Example usage
performance_table, classification_report_table = modeling_pipeline()
print("Performance Table:")
print(performance_table)
print("\nClassification Report Table:")
print(classification_report_table)
