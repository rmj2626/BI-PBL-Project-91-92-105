import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor

# Load the dataset
df = pd.read_csv('youtube_data.csv')

# Select relevant features and target variable
features = ['durationSecs', 'likeCount', 'commentCount', 'Views per Minute']
X = df[features]  # Independent variables
y = df['Views']   # Dependent variable (target)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Initialize and train the Gradient Boosting model
gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gb_model.fit(X_train, y_train)

# Make predictions and evaluate
y_gb_pred = gb_model.predict(X_test)

# Calculate evaluation metrics
mse_gb = mean_squared_error(y_test, y_gb_pred)
r2_gb = r2_score(y_test, y_gb_pred)
mape_gb = mean_absolute_percentage_error(y_test, y_gb_pred)

print("\nGradient Boosting Regressor Results")
print(f"Mean Squared Error (MSE): {mse_gb}")
print(f"R² Score: {r2_gb}")
print(f"Mean Absolute Percentage Error (MAPE): {mape_gb * 100:.2f}%")
