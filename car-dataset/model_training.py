# model_training.py

# Required libraries import karte hain
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# Data load karna
data = pd.read_csv('data/car_data.csv')

# Data clean aur encode karna
data = data.dropna()
data = pd.get_dummies(data, columns=['brand', 'model'], drop_first=True)

# Features aur target variable define karna
X = data.drop('price', axis=1)
y = data['price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model create aur train karna
model = LinearRegression()
model.fit(X_train, y_train)

# Model evaluate karna
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Trained model ko save karna using pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
print("Model trained and saved as 'model.pkl'")
