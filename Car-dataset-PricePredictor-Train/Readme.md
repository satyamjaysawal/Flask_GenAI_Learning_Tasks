---


# Car Price Prediction App

Yeh app second-hand cars ke price ko predict karne ke liye machine learning model ka use karta hai. Ismein user-friendly web interface hai jahan users car ki details daal ke estimated price dekh sakte hain.

## Features
- Car ki age aur mileage ke basis par price prediction.
- Various brands aur models ke liye support.
- Simple aur intuitive user interface.

## Project Structure
```
car_price_prediction/
├── data/
│   └── car_data.csv               # CSV file with car sales data
├── templates/
│   └── index.html                 # HTML file for the UI
├── static/
│   └── style.css                  # CSS file for styling
├── app.py                         # Main Flask app for deployment
├── model_training.py              # Code to train and save the ML model
├── predict_price.py               # Code for prediction function
├── requirements.txt               # List of required libraries
└── README.md                      # Project documentation

```
---

## Setup Instructions

### 1. Clone the Repository
Pehle repository ko clone karo:
```bash
git clone <repository-url>
cd car_price_prediction
```

### 2. Install Required Libraries
Python ke liye required libraries install karo:
```bash
pip install -r requirements.txt
```

### 3. Data Preparation
Data ko load karne ke liye, ensure karo ki `data/car_data.csv` file sahi se configured hai.

### 4. Train the Model
Model ko train karne ke liye yeh command run karo:
```bash
python model_training.py
```

### 5. Run the Flask App
Flask app ko run karne ke liye:
```bash
python app.py
```
Phir web browser mein `http://127.0.0.1:5000/` open karo.

### 6. Using the App
- Car ki age aur mileage daalo.
- Brand aur model specify karo.
- "Predict Price" button par click karo.
- Estimated price screen par display hoga.

## API Endpoint
### `POST /predict`
- **Description**: Price prediction ke liye input deta hai.
- **Request Body**:
```json
{
    "age": 5,
    "mileage": 50000,
    "brand": "Toyota",
    "model": "Corolla"
}
```
- **Response**:
```json
{
    "price": 1234567.89
}
```

## Dependencies
- **Python**: 3.x
- **Libraries**:
  - pandas
  - numpy
  - scikit-learn
  - flask

---
---
