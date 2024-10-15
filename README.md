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
- [Contributing](#contributing)
- [License](#license)

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


