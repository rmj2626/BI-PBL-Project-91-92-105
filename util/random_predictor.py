import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Load the dataset
df = pd.read_csv('youtube_data.csv')

# Select relevant features and target variable
features = ['durationSecs', 'likeCount', 'commentCount', 'Views per Minute']
X = df[features]
y = df['Views']

# Train the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Prepare input data for predictions for the years 2023, 2025, and 2030
# You may need to adjust these values based on trends or historical averages
future_data = pd.DataFrame({
    'durationSecs': [np.mean(df['durationSecs'])] * 3,
    'likeCount': [np.mean(df['likeCount']) * 1.05, np.mean(df['likeCount']) * 1.10, np.mean(df['likeCount']) * 1.20],
    'commentCount': [np.mean(df['commentCount']) * 1.05, np.mean(df['commentCount']) * 1.10, np.mean(df['commentCount']) * 1.20],
    'Views per Minute': [np.mean(df['Views per Minute']) * 1.05, np.mean(df['Views per Minute']) * 1.10, np.mean(df['Views per Minute']) * 1.20]
}, index=[2023, 2025, 2030])

# Predict views for future years
predicted_views = rf_model.predict(future_data)

# Create the youtube_predictions.csv DataFrame
predictions_df = pd.DataFrame({
    'Metric': ['Views', 'likeCount', 'commentCount', 'Views per Minute'],
    '2023': [predicted_views[0], future_data.loc[2023, 'likeCount'], future_data.loc[2023, 'commentCount'], future_data.loc[2023, 'Views per Minute']],
    '2025': [predicted_views[1], future_data.loc[2025, 'likeCount'], future_data.loc[2025, 'commentCount'], future_data.loc[2025, 'Views per Minute']],
    '2030': [predicted_views[2], future_data.loc[2030, 'likeCount'], future_data.loc[2030, 'commentCount'], future_data.loc[2030, 'Views per Minute']]
})

# Save predictions to youtube_predictions.csv
predictions_df.to_csv('youtube_predictions.csv', index=False)

print("Predictions have been saved to youtube_predictions.csv")
