%%writefile app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import logging
import pandas as pd
import numpy as np

# Set up logging
logging.basicConfig(
    filename='app.log',  # Log file
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Load the model, one-hot encoder, and scaler
model = joblib.load("xgb_model.joblib")
onehot_encoder = joblib.load("onehot_encoder.joblib")
scaler = joblib.load("scaler.joblib")

class ReadmissionInput(BaseModel):
    Age: int
    Gender: str
    Admission_Type: str
    Diagnosis: str
    Num_Lab_Procedures: int
    Num_Medications: int
    Num_Outpatient_Visits: int
    Num_Inpatient_Visits: int
    Num_Emergency_Visits: int
    Num_Diagnoses: int

app = FastAPI()

@app.get("/health")
def health_check():
    """Health check endpoint."""
    logging.info("Health check endpoint called.")
    return {"status": "OK"}

@app.post("/predict")
def predict_readmission(input_data: ReadmissionInput):
    """Predict hospital readmission based on input features."""
    logging.info("Prediction request received with input: %s", input_data.dict())

    try:
        # Convert input data to DataFrame
        data = pd.DataFrame([input_data.dict()])

        categorical_cols = ['Gender', 'Admission_Type', 'Diagnosis']
        numerical_cols = ['Age', 'Num_Lab_Procedures', 'Num_Medications',
                          'Num_Outpatient_Visits', 'Num_Inpatient_Visits',
                          'Num_Emergency_Visits', 'Num_Diagnoses']

        # Preprocessing
        encoded_features = onehot_encoder.transform(data[categorical_cols])
        scaled_numerical = scaler.transform(data[numerical_cols])
        processed_data = pd.DataFrame(
            data=np.hstack((scaled_numerical, encoded_features)),
            columns=numerical_cols + list(onehot_encoder.get_feature_names_out(categorical_cols))
        )

        # Make predictions
        prediction = model.predict(processed_data)
        probability = model.predict_proba(processed_data)[:, 1]

        logging.info("Prediction successful: %d with probability: %.3f", int(prediction[0]), float(probability[0]))

        return {
            "prediction": int(prediction[0]),
            "probability": float(probability[0])
        }
    except Exception as e:
        logging.error("Error occurred while making prediction: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Only run the app if the script is called directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

# Function to check for existing tunnels
def check_existing_tunnels():
    try:
        tunnels = ngrok.get_tunnels()
        return tunnels is not None and len(tunnels) > 0
    except Exception as e:
        logging.error("Error checking existing tunnels: %s", str(e))
        return False

# Set up ngrok and check for existing tunnels
ngrok.set_auth_token("2nRc8cyZBQoLeTme7zYGSktUfrH_3d3QoHP267PTaECDCzyS9")

if check_existing_tunnels():
    print("Existing tunnels found. Closing them.")
    ngrok.kill()  # This will terminate all existing tunnels

# Create a new tunnel
public_url = ngrok.connect(8080)
print("Public URL:", public_url)

# Run the app
app = create_app()
import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8080)
