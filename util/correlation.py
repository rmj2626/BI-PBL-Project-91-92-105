import pandas as pd

# Load the dataset
df = pd.read_csv('youtube_data.csv')

print(df[['durationSecs', 'likeCount', 'commentCount', 'View-to-Like Ratio', 'Views', 'tagCount', 'noOfWordsInTitle', 'Comments per View', 'Views per Minute', 'Interaction Rate']].corr())

# Save the correlation matrix to a .txt file
correlation_matrix = df[['durationSecs', 'likeCount', 'commentCount', 'View-to-Like Ratio', 'Views', 'tagCount', 'noOfWordsInTitle', 'Comments per View', 'Views per Minute', 'Interaction Rate']].corr()
correlation_matrix.to_string('correlation_matrix.txt')

print("Correlation matrix saved to correlation_matrix.txt")