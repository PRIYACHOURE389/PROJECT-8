from flask import Flask, render_template, request, send_file
import pandas as pd

# Initialize Flask application
app = Flask(__name__, template_folder='templates')

# Load your CSV data into a DataFrame
df = pd.read_csv('task6_data.csv')

# Route to handle job recommendations
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        title = request.form['title']
        recommended_jobs = process_recommendations(title)
        return render_template('recommendations.html', title=title, recommended_jobs=recommended_jobs)
    else:
        return render_template('index.html')

# Function to process recommendations based on title
def process_recommendations(title):
    # Example logic to filter recommendations based on title
    # Replace this with your actual logic to filter from the DataFrame
    filtered_jobs = df[df['title'].str.contains(title, case=False)]
    recommended_jobs = filtered_jobs.to_dict('records')
    return recommended_jobs

# Route to serve task6_data.csv file
@app.route('/download_csv')
def download_csv():
    csv_filename = 'task6_data.csv'
    return send_file(csv_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
