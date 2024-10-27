from flask import Flask, request, jsonify, render_template
from predict_price import predict_price

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])  # Define route for POST requests
def predict():
    # JSON data ko retrieve karna, agar data nahi milta to force=True se empty dictionary milegi
    data = request.get_json(force=True)  

    # Input data ki validation
    required_keys = ['age', 'mileage', 'brand', 'model']  # Required keys define karo
    if not all(key in data for key in required_keys):  # Check karo ki sab keys present hain
        return jsonify({"error": "Missing required fields"}), 400  # Error message agar keys nahi hain

    # Input data ko variables mein assign karo
    age = data['age']
    mileage = data['mileage']
    brand = data['brand']
    model_name = data['model']

    # Price prediction karna
    predicted_price = predict_price(age, mileage, brand, model_name)

    return jsonify(price=predicted_price)  # Predicted price ko return karo as JSON

if __name__ == '__main__':
    app.run(debug=True)  # App ko debug mode mein run karo
