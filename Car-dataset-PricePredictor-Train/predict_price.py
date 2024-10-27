# predict_price.py

# Required libraries import karte hain
import pandas as pd   # data manipulation ke liye pandas
import pickle         # trained model ko load karne ke liye pickle

# Trained model ko load karna
with open('model.pkl', 'rb') as file:  # model.pkl file ko read mode mein open karte hain
    model = pickle.load(file)  # pickle ke through trained model ko load karte hain

# Prediction function define karna
def predict_price(age, mileage, brand, model_name):
    # Input data prepare karna
    input_data = pd.DataFrame([[age, mileage]], columns=['age', 'mileage'])  # input values ko dataframe mein convert karte hain
    
    # Dummy variables handle karna for brand aur model
    brands = [col for col in model.feature_names_in_ if 'brand_' in col]  # trained model ke brand columns find karte hain
    models = [col for col in model.feature_names_in_ if 'model_' in col]  # trained model ke model columns find karte hain
    
    # Brand ke dummy variables ko handle karna
    for b in brands:
        input_data[b] = 1 if f'brand_{brand}' == b else 0  # selected brand ke liye 1, baaki sab ke liye 0 set karte hain
    
    # Model ke dummy variables ko handle karna
    for m in models:
        input_data[m] = 1 if f'model_{model_name}' == m else 0  # selected model ke liye 1, baaki sab ke liye 0 set karte hain

    # Input data ko trained model ke columns ke hisaab se reindex karna
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)  # missing columns ko 0 se fill karte hain

    # Prediction karna
    price_estimate = model.predict(input_data)[0]  # input data ka price predict karte hain
    return price_estimate  # estimated price ko return karte hain
