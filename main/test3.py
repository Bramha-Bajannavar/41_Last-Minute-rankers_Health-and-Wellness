import pickle
import numpy as np
import os

# Define the complete path to the .pkl files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, '/Users/bramhabajannavar/Desktop/Parkinsons/Parkinsons/main/models/parkinsons_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, '/Users/bramhabajannavar/Desktop/Parkinsons/Parkinsons/main/models/scaler.pkl')

# Load the model and scaler from pickle files
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

with open(SCALER_PATH, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)


def predict(input_features):
    """
    Predict the likelihood of Parkinson's disease based on input features.

    Args:
        input_features (list): List of 22 numeric input features.

    Returns:
        float: The predicted probability of Parkinson's disease.
    """
    # Ensure the input is in the correct format (2D array)
    input_features = np.array(input_features).reshape(1, -1)

    # Scale the input features using the scaler
    scaled_features = scaler.transform(input_features)

    # Make the prediction using the model
    prediction_prob = model.predict_proba(scaled_features)
    return prediction_prob[0][1]
