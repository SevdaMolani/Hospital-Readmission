# Hospital Readmission Prediction API

This project provides a FastAPI application for predicting hospital readmissions using machine learning. The model takes various patient attributes as input and returns a prediction indicating whether the patient is likely to be readmitted to the hospital, along with the probability of that prediction.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [Predict Readmission](#predict-readmission)
- [Testing](#testing)
- [Logging](#logging)

## Installation

To run this project, you need Python 3.7 or higher. Follow these steps to set up the environment:

1. Clone the repository:

   ```bash
   git clone https://github.com/SevdaMolani/hospital-readmission.git
   cd hospital-readmission
2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   pip install -r requirements.txt
4. To start the FastAPI application, run the following command:
   uvicorn app:app --host 0.0.0.0 --port 8080
   You can then access the API at http://127.0.0.1:8000.

## API Endpoints
Health Check
Endpoint: /health
Method: GET
Description: Checks the health of the API.
Response: {
  "status": "OK"
}

Predict Readmission
Endpoint: /predict
Method: POST
Request Body:
{
    "Age": 70,
    "Gender": "Male",
    "Admission_Type": "Emergency",
    "Diagnosis": "Heart Failure",
    "Num_Lab_Procedures": 5,
    "Num_Medications": 10,
    "Num_Outpatient_Visits": 2,
    "Num_Inpatient_Visits": 1,
    "Num_Emergency_Visits": 3,
    "Num_Diagnoses": 2
}
Response:
{
    "prediction": 1,
    "probability": 0.8
}

Testing
To run tests for the application, make sure you have pytest installed. You can run the tests using the following command:
pytest tests/

Logging
The application logs important events to a file named app.log. This includes health check requests, prediction requests, and any errors that may occur during processing.
