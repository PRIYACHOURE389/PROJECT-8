import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load CSV data
file_path = r'C:\Users\admin\OneDrive\Desktop\job-recommend\task6_data.csv'
df = pd.read_csv(file_path)

# Print columns to debug
print("Columns in the DataFrame:", df.columns.tolist())

# Clean column names by stripping leading/trailing spaces
df.columns = df.columns.str.strip()

# Convert date column to datetime and set as index
df['published_date'] = pd.to_datetime(df['published_date'])
df.set_index('published_date', inplace=True)

# Initialize the Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("Job Market Trends Dashboard"),
    html.Label("Select Metric:"),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Number of Job Postings', 'value': 'title'},
            {'label': 'Average Hourly Rate', 'value': 'average_hourly_rate'},
            {'label': 'Total Budget', 'value': 'budget'}
        ],
        value='title'
    ),
    dcc.Graph(id='job-market-trends')
])

# Callback function to update graph
@app.callback(
    Output('job-market-trends', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_graph(metric):
    try:
        if metric == 'title':
            # Count the number of job postings per month
            monthly_data = df.resample('ME').size()
            y_label = 'Number of Job Postings'
            fig = px.line(monthly_data, x=monthly_data.index, y=monthly_data, 
                          title=f'{y_label} Over Months', labels={'y': y_label})
        else:
            if metric not in df.columns:
                raise ValueError(f"Column '{metric}' does not exist in the data")
            
            # Aggregate other metrics by mean
            monthly_data = df.resample('ME').agg({
                metric: 'mean'
            })
            y_label = metric.replace('_', ' ').capitalize()
            fig = px.line(monthly_data, x=monthly_data.index, y=metric, 
                          title=f'{y_label} Over Months', labels={metric: y_label})

        return fig

    except Exception as e:
        print(f"Error in callback: {e}")
        return px.line(title="Error: Unable to update graph. Check metric selection and data availability.")

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
