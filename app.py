from flask import Flask, request, jsonify
from sklearn.externals import joblib
import traceback
import pandas as pd
import sys

app = Flask(__name__)

def preprocess(model_data):
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    model_columns = joblib.load("model_columns.pkl")
    if model:
        query = pd.DataFrame(model_data, index=[0])
        query = pd.get_dummies(query)
        query = query.reindex(columns=model_columns, fill_value=0)
        query = scaler.transform(query)
        prediction = list(model.predict(query))
        if prediction[0] == 0:
            fraud = "Accepted"
        else:
           fraud = "Pending"
        return fraud
    else:
        return jsonify({
            "message": "No Trained Model Found"
        }), 403

@app.route('/predict', methods=['GET'])
claim=request.json.get("property_claim")
def predict():
    model_data = {
        'property_claim': 780,
        'policy_annual_premium': 1197.22,
        'incident_severity': 'Minor Damage',
        'insured_hobbies': 'reading',
        'vehicle_age': 12,
        'injury_claim': 780,
        'capital-gains': 0,
        'capital-loss': 0,
        'total_claim_amount': 5070,
        'months_as_customer': 228,
        'witnesses': 0,
        'vehicle_claim': 35100,
        'police_report_available': 0,
        'csl_per_person': 250,
        'csl_per_person': 500,
        'authorities_contacted': 'Police',
        'umbrella_limit': 5000000,
        'bodily_injuries': 0,
        'insured_relationship': 'other-relative',
        'auto_model': 'E400',
        'auto_make': 'Mercedes',
        'collision_en': 0,
        'policy_county': 'Nakuru',
        'age': '42',
        'policy_deductable': 2000,
        'insured_education_level': 'MD',
        'incident_county': 'Meru',
        'incident_city': 'Meru',
        'incident_period_of_the_day': 'morning',
        'property_damage': 0,
        'incident_type': 'Vehicle_Theft',
        'insured_occupation': 'machine-op-inspct',
        'number_of_vehicles_involved': 1

    }
    risk = preprocess(model_data)
    return jsonify({
        "prediction": risk
    }),200

if __name__ == '__main__':
    app.run(port=5000, debug=True)