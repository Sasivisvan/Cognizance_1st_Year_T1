# Import necessary libraries
from sklearn.datasets import load_diabetes
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np


# Step 1: Load the Dataset and Convert to DataFrame
data = load_diabetes()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['progression'] = data.target
df.to_csv("diabetes.csv", index=False)  # Save to CSV for completeness

# Step 2: Preprocess the Data
# Load the data from CSV
df = pd.read_csv("diabetes.csv")

# Check for missing values
print("Missing values in dataset:\n", df.isnull().sum())

# Standardize the features
X = df.drop('progression', axis=1)  # Features
y = df['progression']  # Target variable

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Model Selection
# Initialize models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=5)
}

# Step 4: Train and Evaluate Each Model on the Test Set
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=5)

# Train and evaluate each model
test_results = {}

for name, model in models.items():
    # Train the model on the training set
    model.fit(X_train, y_train)
    # Predict on the test set
    y_pred = model.predict(X_test)
    # Evaluate Mean Squared Error
    test_mse = mean_squared_error(y_test, y_pred)
    test_results[name] = test_mse
    print(f"{name} - Test set Mean Squared Error: {test_mse}")

# Select the best model based on test set performance
best_model_name = min(test_results, key=test_results.get)
best_model = models[best_model_name]
print(f"\nBest model based on test set: {best_model_name}")
