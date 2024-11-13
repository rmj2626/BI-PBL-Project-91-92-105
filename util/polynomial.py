import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score

# Try Polynomial Regression with degree 2 or 3
degree = 2  # Start with 2; can increase to 3 if necessary

# Load the dataset
df = pd.read_csv('youtube_data.csv')

# Select features and target variables (example: predict Views)
features = ['durationSecs', 'likeCount', 'commentCount', 'Views per Minute']
X = df[features]  # Independent variables
y = df['Views']   # Dependent variable (target)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline that applies Polynomial Features then Linear Regression
poly_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
poly_model.fit(X_train, y_train)

# Make predictions and evaluate
y_poly_pred = poly_model.predict(X_test)

# Calculate evaluation metrics
mse_poly = mean_squared_error(y_test, y_poly_pred)
r2_poly = r2_score(y_test, y_poly_pred)
mape_poly = mean_absolute_percentage_error(y_test, y_poly_pred)

print(f"Polynomial Regression (Degree {degree})")
print(f"Mean Squared Error (MSE): {mse_poly}")
print(f"R² Score: {r2_poly}")
print(f"Mean Absolute Percentage Error (MAPE): {mape_poly * 100:.2f}%")

from sklearn.preprocessing import StandardScaler

# Create a pipeline with scaling, polynomial features, and linear regression
poly_model = make_pipeline(StandardScaler(), PolynomialFeatures(2), LinearRegression())
poly_model.fit(X_train, y_train)

# Evaluate again
y_poly_pred = poly_model.predict(X_test)
mse_poly = mean_squared_error(y_test, y_poly_pred)
r2_poly = r2_score(y_test, y_poly_pred)
mape_poly = mean_absolute_percentage_error(y_test, y_poly_pred)

print(f"After Standardizing Features - Polynomial Regression (Degree 2)")
print(f"Mean Squared Error (MSE): {mse_poly}")
print(f"R² Score: {r2_poly}")
print(f"Mean Absolute Percentage Error (MAPE): {mape_poly * 100:.2f}%")
