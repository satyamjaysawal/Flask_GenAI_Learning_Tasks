# model_training.py

# Required libraries import karte hain
import pandas as pd   # data manipulation aur analysis ke liye pandas
import numpy as np    # mathematical calculations ke liye numpy
from sklearn.model_selection import train_test_split  # data ko train aur test mein split karne ke liye
from sklearn.linear_model import LinearRegression     # Linear Regression model import kar rahe hain
from sklearn.metrics import mean_squared_error, r2_score  # model evaluation ke liye metrics import kar rahe hain
import pickle    # trained model ko save aur load karne ke liye pickle use karenge

# Data load karna
data = pd.read_csv('data/car_data.csv')  # car_data.csv file se data load kar rahe hain

# Data clean aur encode karna
data = data.dropna()  # missing values ko drop kar rahe hain
data = pd.get_dummies(data, columns=['brand', 'model'], drop_first=True)  # categorical variables ko encode kar rahe hain

# Features aur target variable define karna
X = data.drop('price', axis=1)  # X mein price ke alawa saare features store karenge
y = data['price']               # y mein price ko store karenge jo hamara target variable hai

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  
# data ko 80-20 ke ratio mein split karte hain (80% train aur 20% test data)

# Model create aur train karna
model = LinearRegression()  # Linear Regression model ka instance banate hain
model.fit(X_train, y_train)  # model ko training data par fit karte hain

# Model evaluate karna
y_pred = model.predict(X_test)  # test data par predictions generate karte hain
mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error calculate karte hain
r2 = r2_score(y_test, y_pred)  # R^2 Score calculate karte hain

print(f"Mean Squared Error: {mse}")  # Mean Squared Error ko print karte hain
print(f"R^2 Score: {r2}")  # R^2 Score ko print karte hain

# Trained model ko save karna using pickle
with open('model.pkl', 'wb') as file:  # model ko model.pkl file mein save karenge
    pickle.dump(model, file)  # pickle ke through model ko dump karte hain
print("Model trained and saved as 'model.pkl'")  # success message display karte hain
