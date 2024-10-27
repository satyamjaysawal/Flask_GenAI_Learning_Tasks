# predict_price.py

import pandas as pd
import pickle

# Trained model ko load karna
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Prediction function define karna
def predict_price(age, mileage, brand, model_name):
    # Input data prepare karna
    input_data = pd.DataFrame([[age, mileage]], columns=['age', 'mileage'])
    
    # Dummy variables handle karna for brand aur model
    brands = [col for col in model.feature_names_in_ if 'brand_' in col]
    models = [col for col in model.feature_names_in_ if 'model_' in col]
    
    for b in brands:
        input_data[b] = 1 if f'brand_{brand}' == b else 0
    for m in models:
        input_data[m] = 1 if f'model_{model_name}' == m else 0

    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    # Prediction karna
    price_estimate = model.predict(input_data)[0]
    return price_estimate
