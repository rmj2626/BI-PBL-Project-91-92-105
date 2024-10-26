# BI PBL Mini Project
# Topic: Youtube Channel Data Analytics
# Team Members:
# 1. Rudraksha M. J.
# 2. Soham Joshi
# 3. Akash Kamthe

# TODO: Improve the CSS, add predictive analysis

from flask import Flask, request, send_file, jsonify, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io

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
    filtered_df = df[(df['Video publish year'] >= from_year) & (df['Video publish year'] <= to_year)]

    # Map visualization type to the correct column names
    if visualization_type == 'views':
        y_data = filtered_df['Views']
        y_label = "Views"
        title = 'Views Over Time'
    elif visualization_type == 'likes_vs_comments':
        y_data_likes = filtered_df['likeCount']
        y_data_comments = filtered_df['commentCount']
        y_label = "Likes vs Comments"
        title = 'Likes vs Comments Over Time'
    elif visualization_type == 'engagement':
        y_data = filtered_df['Engagement']
        y_label = "Engagement Level"
        title = 'Engagement Over Time'
    elif visualization_type == 'duration':
        y_data = filtered_df['durationSecs']
        y_label = "Duration (Seconds)"
        title = 'Video Duration Over Time'

    # Aggregate data year-wise
    filtered_df['Year'] = filtered_df['Video publish date'].dt.year
    if visualization_type == 'likes_vs_comments':
        yearly_data_likes = filtered_df.groupby('Year')[y_data_likes.name].sum()
        yearly_data_comments = filtered_df.groupby('Year')[y_data_comments.name].sum()
    else:
        yearly_data = filtered_df.groupby('Year')[y_data.name].sum()

    # Create the plot
    if graph_type == 'pie':
        plt.figure(figsize=(10, 7))  # Larger figure size for pie charts
    else:
        plt.figure(figsize=(6.8, 3))  # 680px x 300px figure for other charts

    # Plot based on visualization type and graph type
    if visualization_type == 'likes_vs_comments':
        if graph_type == 'bar':
            plt.bar(yearly_data_likes.index, yearly_data_likes, label="Likes", color='#59666F')
            plt.bar(yearly_data_comments.index, yearly_data_comments, label="Comments", bottom=yearly_data_likes, color='skyblue')
        else:  # default is line graph
            plt.plot(yearly_data_likes.index, yearly_data_likes, label="Likes", marker='o')
            plt.plot(yearly_data_comments.index, yearly_data_comments, label="Comments", marker='o')
    else:
        if graph_type == 'bar':
            plt.bar(yearly_data.index, yearly_data, color='skyblue')
        elif graph_type == 'pie':
            plt.pie(yearly_data, labels=yearly_data.index, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')  # Equal aspect ratio for pie chart
        else:  # default is line graph
            plt.plot(yearly_data.index, yearly_data, marker='o')

    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.legend()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    # Return the image as response
    return send_file(img, mimetype='image/png')

@app.route('/predict-chart', methods=['POST'])
def predict_chart():
    # Load predictive analysis data
    pred_df = pd.read_csv('youtube_predictions.csv')  # Update with your file if different

    # Get data from the request
    data = request.get_json()
    visualization_type = data['visualizationType']
    graph_type = data['graphType']

    # Map visualization type to correct row in predictive analysis data
    if visualization_type == 'views_prediction':
        y_data = pred_df.loc[pred_df['Unnamed: 0'] == 'Views'].values.flatten()[1:]
        y_label = "Views"
        title = 'Views Prediction'
    elif visualization_type == 'like_count_prediction':
        y_data = pred_df.loc[pred_df['Unnamed: 0'] == 'likeCount'].values.flatten()[1:]
        y_label = "Like Count"
        title = 'Like Count Prediction'
    elif visualization_type == 'comment_count_prediction':
        y_data = pred_df.loc[pred_df['Unnamed: 0'] == 'commentCount'].values.flatten()[1:]
        y_label = "Comment Count"
        title = 'Comment Count Prediction'

    years = ['2023', '2025', '2030']  # Adjust as needed

    # Create the plot
    if graph_type == 'pie':
        plt.figure(figsize=(10, 7))
    else:
        plt.figure(figsize=(6.8, 3))

    # Plot based on graph type
    if graph_type == 'bar':
        plt.bar(years, y_data, color='skyblue', label=y_label)
    elif graph_type == 'pie':
        plt.pie(y_data, labels=years, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
    else:
        plt.plot(years, y_data, marker='o', label=y_label)

    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.legend()

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)

    # Return the image as response
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
