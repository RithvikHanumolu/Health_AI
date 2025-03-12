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
    "thyroid_cancer": joblib.load("NEW_thyroid_cancer_model.pkl"),
    "Heart_Disease": joblib.load("heart_disease_model.pkl"),
}

# Expected features for each disease
expected_features = {
    "thyroid_cancer": ["Age", "Gender", "Smoking", "Hx Smoking", "Hx Radiotherapy", 
                         "Physical Examination", "Adenopathy", "Pathology", "Focality", 
                         "T", "N", "M", "Stage", "Response"],
    "lung_cancer": ["GENDER", "AGE", "SMOKING", "YELLOW_FINGERS", "ANXIETY", "PEER_PRESSURE", "CHRONIC DISEASE", "FATIGUE ", "ALLERGY ", "WHEEZING", "ALCOHOL CONSUMING", "COUGHING", "SHORTNESS OF BREATH", "SWALLOWING DIFFICULTY", "CHEST PAIN"],
    "diabetes": ["HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"],
    "Heart_Disease": ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
}

# Preprocessing functions for each disease
def preprocess_thyroid_cancer(data):

# Initialize a dictionary with the expected features
    processed_data = {feature: None for feature in expected_features}

    # Map frontend answers to model's expected features
    processed_data["Age"] = data.get("How old are you?", None)

    cancer_age = data.get("What is your gender?", None)
    if cancer_age == "Male":
        processed_data["Gender"] = "1"
    elif cancer_age == "Female":
        processed_data["Gender"] = "0"

    cancer_Smoke = data.get("Do you currently smoke?", None)
    if cancer_Smoke == "Yes":
        processed_data["Smoking"] = "1"
    elif cancer_Smoke == "No":
        processed_data["Smoking"] = "0"

    cancer_HxSmoke = data.get("Do you currently smoke?", None)
    if cancer_HxSmoke == "Yes":
        processed_data["Hx Smoking"] = "1"
    elif cancer_HxSmoke == "No":
        processed_data["Hx Smoking"] = "0"

    cancer_HxRadiotherapy = data.get("Have you ever smoked?", None)
    if cancer_HxRadiotherapy == "Yes":
        processed_data["Hx Radiotherapy"] = "1"
    elif cancer_HxRadiotherapy == "No":
        processed_data["Hx Radiotherapy"] = "0"

    cancer_exam = data.get("What are the results of your physical examination?", None)
    if cancer_exam == "Normal":
        processed_data["Physical Examination"] = "0"
    elif cancer_exam == "Diffuse goiter":
        processed_data["Physical Examination"] = "1"
    elif cancer_exam == "Single nodular goiter-left":
        processed_data["Physical Examination"] = "2"
    elif cancer_exam == "Single nodular goiter-right":
        processed_data["Physical Examination"] = "3"
    elif cancer_exam == "Multinodular goiter":
        processed_data["Physical Examination"] = "4"

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

    cancer_path = data.get("What is the pathology results of your thyroid biopsy?", None)
    if cancer_path == "Micropapillary":
        processed_data["Pathology"] = "0"
    elif cancer_path == "Papillary":
        processed_data["Pathology"] = "1"
    elif cancer_path == "Follicular":
        processed_data["Pathology"] = "2"
    elif cancer_path == "Hurthle cell":
        processed_data["Pathology"] = "3"



    # Additional Features
    cancer_Focality = data.get("Is your thyroid cancer unifocal or multifocal?", None)
    if cancer_Focality == "Multi-Focal":
        processed_data["Focality"] = "1"
    elif cancer_Focality == "Uni-Focal":
        processed_data["Focality"] = "0"

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

    cancer_stage = data.get("Has your cancer spread to distant organs?", None)
    if cancer_stage == "No":
        processed_data["M"] = "0"
    elif cancer_stage == "Yes":
        processed_data["M"] = "1"

    cancer_stage = data.get("What is your stage of cancer?", None)
    if cancer_stage == "I":
        processed_data["Stage"] = "0"
    elif cancer_stage == "II":
        processed_data["Stage"] = "1"
    elif cancer_stage == "III":
        processed_data["Stage"] = "2"
    elif cancer_stage == "IVA":
        processed_data["Stage"] = "3"
    elif cancer_stage == "IVB":
        processed_data["Stage"] = "4"
    
    cancer_stage = data.get("How did your cancer respond to treatment?", None)
    if cancer_stage == "Excellent":
        processed_data["Response"] = "0"
    elif cancer_stage == "Indeterminate":
        processed_data["Response"] = "1"
    elif cancer_stage == "Biochemical Incomplete":
        processed_data["Response"] = "2"
    elif cancer_stage == "Structural Incomplete":
        processed_data["Response"] = "3"

    # Return the data in the same order as the expected features
    return [processed_data[feature] for feature in expected_features["thyroid_cancer"]]

def preprocess_lung_cancer(data):
    
    print(f"Input data: {data}")

    processed_data = {feature: None for feature in expected_features}

    lung_cancer_age = data.get("What is your gender?", None)
    if lung_cancer_age == "Male":
        processed_data["GENDER"] = "1"
    elif lung_cancer_age == "Female":
        processed_data["GENDER"] = "0"

    processed_data["AGE"] = data.get("How old are you?", None)

    lung_cancer_Smoke = data.get("Have you smoked over 100 cigarettes?", None)
    if lung_cancer_Smoke == "Yes":
        processed_data["SMOKING"] = "2"
    elif lung_cancer_Smoke == "No":
        processed_data["SMOKING"] = "1"

    lung_cancer_yellow = data.get("Do you have yellowish fingers?", None)
    if lung_cancer_yellow == "Yes":
        processed_data["YELLOW_FINGERS"] = "2"
    elif lung_cancer_yellow == "No":
        processed_data["YELLOW_FINGERS"] = "1"


    lung_cancer_anxiety = data.get("Do you have anxiety?", None)
    if lung_cancer_anxiety == "Yes":
        processed_data["ANXIETY"] = "2"
    elif lung_cancer_anxiety == "No":
        processed_data["ANXIETY"] = "1"

    lung_cancer_peer = data.get("Do you have peer pressure?", None)
    if lung_cancer_peer == "Yes":
        processed_data["PEER_PRESSURE"] = "2"
    elif lung_cancer_peer == "No":
        processed_data["PEER_PRESSURE"] = "1"

    lung_cancer_chronic = data.get("Do you have Chronic Diseases?", None)
    if lung_cancer_chronic == "Yes":
        processed_data["CHRONIC DISEASE"] = "2"
    elif lung_cancer_chronic == "No":
        processed_data["CHRONIC DISEASE"] = "1"
    
    lung_cancer_fatigue = data.get("Are you constantly fatigued?", None)
    if lung_cancer_fatigue == "Yes":
        processed_data["FATIGUE "] = "2"
    elif lung_cancer_fatigue == "No":
        processed_data["FATIGUE "] = "1"

    lung_cancer_allergy = data.get("Do you have allergies?", None)
    if lung_cancer_allergy == "Yes":
        processed_data["ALLERGY "] = "2"
    elif lung_cancer_allergy == "No":
        processed_data["ALLERGY "] = "1"

    lung_cancer_wheeze = data.get("Do you constantly wheeze?", None)
    if lung_cancer_wheeze == "Yes":
        processed_data["WHEEZING"] = "2"
    elif lung_cancer_wheeze == "No":
        processed_data["WHEEZING"] = "1"

    lung_cancer_wheeze = data.get("Do you drink alcohol?", None)
    if lung_cancer_wheeze == "Yes":
        processed_data["ALCOHOL CONSUMING"] = "2"
    elif lung_cancer_wheeze == "No":
        processed_data["ALCOHOL CONSUMING"] = "1"
    
    lung_cancer_cough = data.get("Do you constantly cough?", None)
    if lung_cancer_cough == "Yes":
        processed_data["COUGHING"] = "2"
    elif lung_cancer_cough == "No":
        processed_data["COUGHING"] = "1"

    lung_cancer_breath = data.get("Do you have shortness of breath?", None)
    if lung_cancer_breath == "Yes":
        processed_data["SHORTNESS OF BREATH"] = "2"
    elif lung_cancer_breath == "No":
        processed_data["SHORTNESS OF BREATH"] = "1"

    lung_cancer_swallow = data.get("Do you have difficulty swallowing?", None)
    if lung_cancer_swallow == "Yes":
        processed_data["SWALLOWING DIFFICULTY"] = "2"
    elif lung_cancer_swallow == "No":
        processed_data["SWALLOWING DIFFICULTY"] = "1"

    lung_cancer_chestpain = data.get("Do you have chest pain?", None)
    if lung_cancer_chestpain == "Yes":
        processed_data["CHEST PAIN"] = "2"
    elif lung_cancer_chestpain == "No":
        processed_data["CHEST PAIN"] = "1"

    #for feature, mapping in mappings.items():
        #value = data.get(f"What is your {feature.lower()}?", None)
        #if value:
            #processed_data[feature] = mapping.get(value, None)

    return [processed_data[feature] for feature in expected_features["lung_cancer"]]

def preprocess_diabetes(data):

    print(f"Input data: {data}")

    processed_data = {feature: None for feature in expected_features}

    diabetes_BP = data.get("Do you have high Blood Pressure?", None)
    if diabetes_BP == "Yes":
        processed_data["HighBP"] = "1"
    elif diabetes_BP == "No":
        processed_data["HighBP"] = "0"
    
    diabetes_chol = data.get("Do you have high Cholesterol?", None)
    if diabetes_chol == "Yes":
        processed_data["HighChol"] = "1"
    elif diabetes_chol == "No":
        processed_data["HighChol"] = "0"

    diabetes_check = data.get("Have you had a Cholesterol Check in the past 5 years?", None)
    if diabetes_check == "Yes":
        processed_data["CholCheck"] = "1"
    elif diabetes_check == "No":
        processed_data["CholCheck"] = "0"
    
    processed_data["BMI"] = data.get("What is your BMI?", None)

    diabetes_cig = data.get("Have you smoked over 100 cigaretes?", None)
    if diabetes_cig == "Yes":
        processed_data["Smoker"] = "1"
    elif diabetes_cig == "No":
        processed_data["Smoker"] = "0"

    diabetes_stroke = data.get("Have you had a stroke?", None)
    if diabetes_stroke == "Yes":
        processed_data["Stroke"] = "1"
    elif diabetes_stroke == "No":
        processed_data["Stroke"] = "0"

    diabetes_hd = data.get("Do you have a Coronary Heart Disease or Myocardial Infarction?", None)
    if diabetes_hd == "Yes":
        processed_data["HeartDiseaseorAttack"] = "1"
    elif diabetes_hd == "No":
        processed_data["HeartDiseaseorAttack"] = "0"

    diabetes_exc = data.get("Do you exercise frequently?", None)
    if diabetes_exc == "Yes":
        processed_data["PhysActivity"] = "1"
    elif diabetes_exc == "No":
        processed_data["PhysActivity"] = "0"

    diabetes_fruit = data.get("Do you eat a daily serving of fruits?", None)
    if diabetes_fruit == "Yes":
        processed_data["Fruits"] = "1"
    elif diabetes_fruit == "No":
        processed_data["Fruits"] = "0"

    diabetes_veg = data.get("Do you eat a daily serving of vegetables?", None)
    if diabetes_veg == "Yes":
        processed_data["Veggies"] = "1"
    elif diabetes_veg == "No":
        processed_data["Veggies"] = "0"

    diabetes_alc = data.get("Do you drink heavy alcohol?", None)
    if diabetes_alc == "Yes":
        processed_data["HvyAlcoholConsump"] = "1"
    elif diabetes_alc == "No":
        processed_data["HvyAlcoholConsump"] = "0"

    diabetes_hlth = data.get("Do you have any kind of healthcare coverage?", None)
    if diabetes_hlth == "Yes":
        processed_data["AnyHealthcare"] = "1"
    elif diabetes_hlth == "No":
        processed_data["AnyHealthcare"] = "0"

    diabetes_money = data.get("Was there a time in the past year when you needed to see a doctor but did not because of its cost?", None)
    if diabetes_money == "Yes":
        processed_data["NoDocbcCost"] = "1"
    elif diabetes_money == "No":
        processed_data["NoDocbcCost"] = "0"

    processed_data["GenHlth"] = data.get("How would you rank your general health (1 is the best, 5 is the worst)", None)
    processed_data["MentHlth"] = data.get("How many days for the past 30 days was your mental health not good", None)
    processed_data["PhysHlth"] = data.get("How many days for the past 30 days was your physical health not good", None)

    diabetes_walk = data.get("Do you have serious difficulty walking or climbing stairs?", None)
    if diabetes_walk == "Yes":
        processed_data["DiffWalk"] = "1"
    elif diabetes_walk == "No":
        processed_data["DiffWalk"] = "0"

    diabetes_gend = data.get("What is you gender?", None)
    if diabetes_gend == "Male":
        processed_data["Sex"] = "1"
    elif diabetes_gend == "Female":
        processed_data["Sex"] = "0"

    processed_data["Age"] = data.get("What is your age?", None)
    processed_data["Education"] = data.get("Rank your education: \n1 = Never attended school or only kindergarten \n2 = Grades 1-8 (Elementary) \n3 = Grades 9-11 (Some high school) \n4 = Grade 12 or GED (High school graduate)  \n5 = College 1-3 years (Some college or technical school)  \n6 = College 4 years+ (College graduate)", None)
    processed_data["Income"] = data.get("Rank your income: \n1 = less than $10k \n5 = less than 35k \n8 = more than 75k", None)

    
    return [processed_data[feature] for feature in expected_features["diabetes"]]

def preprocess_Heart_Disease(data):

    processed_data = {feature: None for feature in expected_features}

    processed_data["age"] = data.get("What is your age", None)

    Heart_gender = data.get("What is your gender?", None)
    if Heart_gender == "Male":
        processed_data["sex"] = "1"
    elif Heart_gender == "Female":
        processed_data["sex"] = "0"
    
    Heart_cp = data.get("What type of chestpain do you experience?", None)
    if Heart_cp == "Asymptomatic":
        processed_data["cp"] = "0"
    elif Heart_cp == "Typical Angina":
        processed_data["cp"] = "1"
    elif Heart_cp == "Atypical Angina":
        processed_data["cp"] = "2"
    elif Heart_cp == "Non-Anginal Pain":
        processed_data["cp"] = "3"

    processed_data["trestbps"] = data.get("What is your resting blood pressure (mmHg)?", None)
    processed_data["chol"] = data.get("What is your cholesterol level (mg/dL)?", None)

    Heart_fbs = data.get("Is you fasting blood sugar more than 120 mg/dL?", None)
    if Heart_fbs == "Yes":
        processed_data["fbs"] = "1"
    elif Heart_fbs == "No":
        processed_data["fbs"] = "0"

    Heart_rest = data.get("What are your resting electrocardiographic results?", None)
    if Heart_rest == "Normal":
        processed_data["restecg"] = "0"
    elif Heart_rest == "ST-T wave abnormality":
        processed_data["restecg"] = "1"
    elif Heart_rest == "Left ventricular hypertrophy":
        processed_data["restecg"] = "2"

    processed_data["thalach"] = data.get("What is your maximum heart rate?", None)

    Heart_exa = data.get("Do you experience exercise induced angina?", None)
    if Heart_exa == "Yes":
        processed_data["exang"] = "1"
    elif Heart_exa == "No":
        processed_data["exang"] = "0"

    processed_data["oldpeak"] = data.get("What is your ST depression induced by exercise relative to rest?", None)

    Heart_slope = data.get("What is the slope of your peak exercise segment?", None)
    if Heart_slope == "Flat":
        processed_data["slope"] = "0"
    elif Heart_slope == "Upsloping":
        processed_data["slope"] = "1"
    elif Heart_slope == "Downsloping":
        processed_data["slope"] = "2"

    processed_data["ca"] = data.get("What is the number of major vessels colored by flourosopy?", None)

    Heart_thal = data.get("What is the thalassemia type?", None)
    if Heart_thal == "Normal":
        processed_data["thal"] = "0"
    elif Heart_thal == "Fixed Defect":
        processed_data["thal"] = "1"
    elif Heart_thal == "Reversable Defect":
        processed_data["thal"] = "2"

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
