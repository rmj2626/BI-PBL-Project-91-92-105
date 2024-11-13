import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv('youtube_data.csv')

# Select relevant features and target variable
features = ['durationSecs', 'likeCount', 'commentCount', 'Views per Minute']
X = df[features]  # Independent variables
y = df['Views']   # Dependent variable (target)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions and evaluate
y_rf_pred = rf_model.predict(X_test)

# Calculate evaluation metrics
mse_rf = mean_squared_error(y_test, y_rf_pred)
r2_rf = r2_score(y_test, y_rf_pred)
mape_rf = mean_absolute_percentage_error(y_test, y_rf_pred)

print("Random Forest Regressor Results")
print(f"Mean Squared Error (MSE): {mse_rf}")
print(f"R² Score: {r2_rf}")
print(f"Mean Absolute Percentage Error (MAPE): {mape_rf * 100:.2f}%")
