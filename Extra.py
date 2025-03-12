from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to call backend API

# Load trained models
models = {
    "lung_cancer": joblib.load("lung_cancer_model.pkl"),
    "diabetes": joblib.load("diabetes_model.pkl"),
    "thyroid_cancer": joblib.load("thyroid_cancer_model.pkl"),
    "Heart_Disease": joblib.load("heart_disease_model.pkl"),
}

# Expected features for each disease
expected_features = {
    "thyroid_cancer": ["Response", "Adenopathy", "N", "T"],
    "lung_cancer": ['AGE', 'ALCOHOL CONSUMING', 'ALLERGY ', 'PEER_PRESSURE'],
    "diabetes": ['BMI', 'Age', 'GenHlth', 'Income'],
    "Heart_Disease": ['ca', 'cp', 'oldpeak', 'thalach']
}

# Preprocessing functions for each disease
def preprocess_thyroid_cancer(data):
    print(models["thyroid_cancer"].feature_names_in_)
# Initialize a dictionary with the expected features
    processed_data = {feature: None for feature in expected_features}


    cancer_stage = data.get("How did your cancer respond to treatment?", None)
    if cancer_stage == "Excellent":
        processed_data["Response"] = "0"
    elif cancer_stage == "Indeterminate":
        processed_data["Response"] = "1"
    elif cancer_stage == "Biochemical Incomplete":
        processed_data["Response"] = "2"
    elif cancer_stage == "Structural":
        processed_data["Response"] = "3"

    cancer_aden = data.get("Do you have enlarged lymph nodes in your neck?", None)
    if cancer_aden == "No":
        processed_data["Adenopathy"] = "0"
    elif cancer_aden == "Right":
        processed_data["Adenopathy"] = "1"
    elif cancer_aden == "Left":
        processed_data["Adenopathy"] = "1"
    elif cancer_aden == "Posterior":
        processed_data["Adenopathy"] = "2"
    elif cancer_aden == "Bilateral":
        processed_data["Adenopathy"] = "3"
    elif cancer_aden == "Extensive":
        processed_data["Adenopathy"] = "4"

    cancer_Tumor = data.get("What is your tumor classification?", None)
    if cancer_Tumor == "T1a":
        processed_data["T"] = "0"
    elif cancer_Tumor == "T1b":
        processed_data["T"] = "1"
    elif cancer_Tumor == "T2":
        processed_data["T"] = "2"
    elif cancer_Tumor == "T3a":
        processed_data["T"] = "3"
    elif cancer_Tumor == "T3b":
        processed_data["T"] = "4"
    elif cancer_Tumor == "T4a":
        processed_data["T"] = "5"
    elif cancer_Tumor == "T4b":
        processed_data["T"] = "6"
        
    cancer_spread = data.get("What is your lymph node classification based on cancer staging?", None)
    if cancer_spread == "N0":
        processed_data["N"] = "0"
    elif cancer_spread == "N1a":
        processed_data["N"] = "1"
    elif cancer_spread == "N1b":
        processed_data["N"] = "2"

    # Return the data in the same order as the expected features
    return [processed_data[feature] for feature in expected_features["thyroid_cancer"]]

def preprocess_lung_cancer(data):
    
    print(f"Input data: {data}")

    processed_data = {feature: None for feature in expected_features}

    processed_data["AGE"] = data.get("How old are you?", None)


    lung_cancer_peer = data.get("Do you have peer pressure?", None)
    if lung_cancer_peer == "Yes":
        processed_data["PEER_PRESSURE"] = "2"
    elif lung_cancer_peer == "No":
        processed_data["PEER_PRESSURE"] = "1"

    lung_cancer_allergy = data.get("Do you have allergies?", None)
    if lung_cancer_allergy == "Yes":
        processed_data["ALLERGY "] = "2"
    elif lung_cancer_allergy == "No":
        processed_data["ALLERGY "] = "1"


    lung_cancer_wheeze = data.get("Do you drink alcohol?", None)
    if lung_cancer_wheeze == "Yes":
        processed_data["ALCOHOL CONSUMING"] = "2"
    elif lung_cancer_wheeze == "No":
        processed_data["ALCOHOL CONSUMING"] = "1"
    

    return [processed_data[feature] for feature in expected_features["lung_cancer"]]

def preprocess_diabetes(data):

    print(f"Input data: {data}")

    processed_data = {feature: None for feature in expected_features}

    
    processed_data["BMI"] = data.get("What is your BMI?", None)
    processed_data["GenHlth"] = data.get("How would you rank your general health (1 is the best, 5 is the worst)", None)
    processed_data["Age"] = data.get("What is your age?", None)
    processed_data["Income"] = data.get("Rank your income: \n1 = less than $10k \n5 = less than 35k \n8 = more than 75k", None)

    
    return [processed_data[feature] for feature in expected_features["diabetes"]]

def preprocess_Heart_Disease(data):

    processed_data = {feature: None for feature in expected_features}

    
    Heart_cp = data.get("What type of chestpain do you experience?", None)
    if Heart_cp == "Asymptomatic":
        processed_data["cp"] = "0"
    elif Heart_cp == "Typical Angina":
        processed_data["cp"] = "1"
    elif Heart_cp == "Atypical Angina":
        processed_data["cp"] = "2"
    elif Heart_cp == "Non-Anginal Pain":
        processed_data["cp"] = "3"


    processed_data["thalach"] = data.get("What is your maximum heart rate?", None)

    processed_data["ca"] = data.get("What is the number of major vessels colored by flourosopy?", None)

    processed_data["oldpeak"] = data.get("What is your ST depression induced by exercise relative to rest?", None)

    return [processed_data[feature] for feature in expected_features["Heart_Disease"]]

# Mapping diseases to their preprocessing functions
preprocessing_functions = {
    "thyroid_cancer": preprocess_thyroid_cancer,
    "lung_cancer": preprocess_lung_cancer,
    "diabetes": preprocess_diabetes,
    "Heart_Disease": preprocess_Heart_Disease
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Receive JSON data
        disease = data.get("disease")
        answers = data.get("answers")

        if disease not in models:
            return jsonify({"error": "Invalid disease type"}), 400

        # Preprocess the input based on the selected disease
        input_data = preprocessing_functions[disease](answers)

        # Create DataFrame with the correct columns
        input_df = pd.DataFrame([input_data], columns=expected_features[disease])

        # Make the prediction
        prediction = models[disease].predict(input_df)[0]
        result = "Positive" if prediction == 1 else "Negative"

        return jsonify({"disease": disease, "prediction": result})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
