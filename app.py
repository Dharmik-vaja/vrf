# Import required libraries
from flask import Flask  # Flask to create the web server
import pandas as pd  # Pandas to handle CSV data

# Initialize Flask app
app = Flask(__name__)

# Load contractor data from CSV file
data_file = "contrator.csv"
df = pd.read_csv(data_file)  # Read the CSV file into a Pandas DataFrame

# Detect columns dynamically based on their names
experience_column = certifications_column = bid_amount_column = None
for col in df.columns:
    col_lower = col.lower()
    if "experience" in col_lower:
        experience_column = col  # Identify the 'Experience (Years)' column
    elif "certifications" in col_lower:
        certifications_column = col  # Identify the 'Certifications' column
    elif "bid amount" in col_lower:
        bid_amount_column = col  # Identify the 'Bid Amount' column

# Convert 'Experience' and 'Bid Amount' columns to numeric for filtering
if experience_column:
    df[experience_column] = pd.to_numeric(df[experience_column], errors="coerce")
if bid_amount_column:
    df[bid_amount_column] = pd.to_numeric(df[bid_amount_column], errors="coerce")

# Define the home route (HTML page)
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">  <!-- Responsive for mobile -->
        <title>Contractor Data</title>
        <style>
            /* Page Styling */
            body { font-family: Arial, sans-serif; text-align: center; margin: 20px; background-color: #f8f9fa; }
            h1 { color: #343a40; font-size: 22px; }

            /* Container for buttons */
            .button-container {
                display: flex; flex-direction: column; align-items: center; gap: 10px;
                margin-bottom: 20px;
            }

            /* Button Styles */
            button { 
                padding: 14px; font-size: 18px; cursor: pointer;
                border: none; background-color: #007bff; color: white; border-radius: 8px;
                transition: background 0.3s;
                width: 90%; max-width: 300px;  /* Ensures mobile-friendliness */
            }
            button:hover { background-color: #0056b3; }

            /* Data Table */
            #data-container { 
                margin-top: 20px; text-align: center; width: 100%;
                overflow-x: auto;  /* Makes the table scrollable on small screens */
            }

            table { width: 100%; border-collapse: collapse; background: white; min-width: 300px; }
            th, td { padding: 8px; border: 1px solid #dee2e6; text-align: left; font-size: 14px; }
            th { background-color: #007bff; color: white; }

            tr:nth-child(even) { background-color: #f2f2f2; } /* Alternating row colors */

            /* Mobile Styles */
            @media (max-width: 600px) {
                th, td { font-size: 12px; padding: 6px; }
                table { min-width: 100%; }
            }
        </style>

        <script>
            /* Function to fetch data from Flask backend */
            function loadData(endpoint) {
                fetch(endpoint)
                    .then(response => response.text())  // Convert response to text
                    .then(data => { document.getElementById("data-container").innerHTML = data; })  // Insert data into HTML
                    .catch(error => console.error("Error loading data:", error));
            }
        </script>
    </head>
    <body>
        <h1>Contractor Data</h1>
        <div class="button-container">
            <button onclick="loadData('/all_contractors')">Show All Contractors</button>  <!-- Loads full table -->
            <button onclick="loadData('/filtered_contractors')">Show Experienced Contractors</button>  <!-- Loads filtered table -->
        </div>
        <div id="data-container"></div>  <!-- Data will be displayed here -->
    </body>
    </html>
    '''

# Route to display all contractor data
@app.route('/all_contractors')
def all_contractors():
    return f'<div style="overflow-x:auto;">{df.to_html(classes="styled-table", index=False)}</div>'

# Route to display filtered contractors based on conditions
@app.route('/filtered_contractors')
def filtered_contractors():
    if experience_column and certifications_column and bid_amount_column:
        # Filtering logic: Experience >= 25, Certifications = "Complete", Bid Amount >= 20522848
        filtered_df = df[
            (df[experience_column] >= 25) &
            (df[certifications_column].str.lower() == "complete") &
            (df[bid_amount_column] >= 20522848)
        ]
    else:
        filtered_df = pd.DataFrame()  # Show empty table if columns are missing

    return f'<div style="overflow-x:auto;">{filtered_df.to_html(classes="styled-table", index=False)}</div>'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Runs on localhost with debugging enabled
