# BI PBL Mini Project 
# Topic: Youtube Channel Data Analytics
# Team Members:
# 1. Rudraksha M. J.
# 2. Soham Joshi
# 3. Akash Kamthe

from flask import Flask, request, send_file, jsonify, render_template
import pandas as pd
import io

import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for rendering plots
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the YouTube data from CSV
df = pd.read_csv('youtube_data.csv')  # Replace with your actual CSV file name

# Convert 'Video publish date' to datetime for plotting
df['Video publish date'] = pd.to_datetime(df['Video publish date'], format='%d-%m-%Y')

@app.route('/')
def index():
    return render_template('index.html')  # Make sure to have an index.html for the interface

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    # Get data from the request
    data = request.get_json()
    visualization_type = data['visualizationType']
    from_year = int(data['fromYear'])
    to_year = int(data['toYear'])
    graph_type = data['graphType']

    # Filter the dataframe based on the year range
    filtered_df = df[(df['Video publish date'].dt.year >= from_year) & (df['Video publish date'].dt.year <= to_year)]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        return jsonify({"error": "No data available for the selected year range. Please choose a different range."})

    # Add 'Year' column to the DataFrame
    filtered_df['Year'] = filtered_df['Video publish date'].dt.year

    # Initialize yearly_data for all cases
    yearly_data = None

    # Map visualization type to the correct column names and aggregate data
    if visualization_type == 'views':
        y_label = "Views"
        title = 'Views Over Time'
        yearly_data = filtered_df.groupby('Year')['Views'].sum()
    elif visualization_type == 'likes_vs_comments':
        y_label = "Likes vs Comments"
        title = 'Likes vs Comments Over Time'
        yearly_data_likes = filtered_df.groupby('Year')['likeCount'].sum()
        yearly_data_comments = filtered_df.groupby('Year')['commentCount'].sum()
    elif visualization_type == 'duration':
        y_label = "Duration (Seconds)"
        title = 'Video Duration Over Time'
        yearly_data = filtered_df.groupby('Year')['durationSecs'].mean()
    elif visualization_type == 'view_to_like_ratio':
        y_label = "View-to-Like Ratio"
        title = 'View-to-Like Ratio Over Time'
        yearly_data = filtered_df.groupby('Year')['View-to-Like Ratio'].mean()
    elif visualization_type == 'tag_count':
        y_label = "Tag Count"
        title = 'Tag Count Over Time'
        yearly_data = filtered_df.groupby('Year')['tagCount'].mean()
    elif visualization_type == 'words_in_title':
        y_label = "Number of Words in Title"
        title = 'Words in Title Over Time'
        yearly_data = filtered_df.groupby('Year')['noOfWordsInTitle'].mean()
    elif visualization_type == 'views_by_day':
        # New logic for views by day (workday vs weekend)
        y_label = "Views"
        title = 'Views by Day Type'
        # Read the new CSV file for day analysis
        day_df = pd.read_csv('day_analysis.csv')
        # Create a bar chart for Workday vs Weekend
        # Data is already in day_type (Workday, Weekend) and views columns
        day_df.set_index('dayType', inplace=True)
        yearly_data = day_df['Views']

    # Error handling for unsupported visualization type
    if yearly_data is None and visualization_type != 'likes_vs_comments':
        return jsonify({"error": "Invalid visualization type"}), 400

    # Create the plot
    plt.figure(figsize=(5, 5) if graph_type == 'pie' else (6.8, 3))

# Plot based on visualization type and graph type
    if visualization_type == 'views_by_day':
        # Generate a bar chart for the 'views_by_day' case
        plt.bar(yearly_data.index, yearly_data.values, color='skyblue')
    elif visualization_type == 'likes_vs_comments':
        if graph_type == 'bar':
            plt.bar(yearly_data_likes.index, yearly_data_likes, label="Likes", color='#59666F')
            plt.bar(yearly_data_comments.index, yearly_data_comments, label="Comments", bottom=yearly_data_likes, color='skyblue')
        else:  # default is line graph
            plt.plot(yearly_data_likes.index, yearly_data_likes, label="Likes", marker='o')
            plt.plot(yearly_data_comments.index, yearly_data_comments, label="Comments", marker='o')
    else:
        if graph_type == 'bar':
            plt.bar(yearly_data.index, yearly_data.values, color='skyblue')
        elif graph_type == 'pie':
            if len(yearly_data) > 10:
                yearly_data = yearly_data[:10]
            plt.pie(yearly_data.values, labels=yearly_data.index, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
        else:  # default is line graph
            plt.plot(yearly_data.index, yearly_data.values, marker='o')

        # Apply x-tick formatting **only if yearly_data is not None and the graph type is not a pie chart**
        if yearly_data is not None and graph_type != 'pie' and visualization_type != 'views_by_day':
            plt.xticks(ticks=yearly_data.index, labels=yearly_data.index.astype(int))


    # Common settings for all plots
    plt.title(title)
    plt.xlabel('Day Type' if visualization_type == 'views_by_day' else 'Year')
    plt.ylabel(y_label)
    plt.legend()


    plt.title(title)
    plt.xlabel('Day Type' if visualization_type == 'views_by_day' else 'Year')
    plt.ylabel(y_label)
    plt.legend()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Return the image as response
    return send_file(img, mimetype='image/png')

@app.route('/predict-chart', methods=['POST'])
def predict_chart():
    # Load predictive analysis data
    pred_df = pd.read_csv('youtube_predictions.csv')

    # Get data from the request
    data = request.get_json()
    visualization_type = data['visualizationType']
    graph_type = data['graphType']

    # Initialize y_data variable
    y_data = None

    # Map visualization type to correct row in predictive analysis data
    if visualization_type == 'views_prediction':
        y_data = pred_df.loc[pred_df['Metric'] == 'Views'].values.flatten()[1:]
        y_label = "Total Views (billions)"
        title = 'Views Prediction'
    elif visualization_type == 'like_count_prediction':
        y_data = pred_df.loc[pred_df['Metric'] == 'likeCount'].values.flatten()[1:]
        y_label = "Average Likes per Video (millions)"
        title = 'Like Count Prediction'
    elif visualization_type == 'comment_count_prediction':
        y_data = pred_df.loc[pred_df['Metric'] == 'commentCount'].values.flatten()[1:]
        y_label = "Comments per Video (thousands)"
        title = 'Comment Count Prediction'
    elif visualization_type == 'views_per_minute_prediction':
        y_data = pred_df.loc[pred_df['Metric'] == 'Views per Minute'].values.flatten()[1:]
        y_label = "Views per Minute"
        title = 'Views per Minute Prediction'
    
    # Error handling if y_data is not set or is empty
    if y_data is None or len(y_data) == 0:
        return jsonify({"error": "Invalid visualization type or missing data"}), 400

    # Year labels based on data
    years = ['2023', '2025', '2030']

    # Create the plot
    plt.figure(figsize=(5, 5) if graph_type == 'pie' else (6.8, 3))

    if graph_type == 'pie':
        plt.pie(y_data, labels=years, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
    else:
        if graph_type == 'bar':
            plt.bar(years, y_data, color='skyblue', label=y_label)
        else:  # default is line graph
            plt.plot(years, y_data, marker='o', label=y_label)

    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.legend()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Return the image as response
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
