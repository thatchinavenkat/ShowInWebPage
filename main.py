import pandas as pd
from flask import Flask, render_template_string
import os
  
app = Flask(__name__)

def read_excel_file(file_path):
    """
    Read an Excel or CSV file and return the data as a DataFrame.
    Prints the data to console.
    
    Args:
        file_path (str): Path to the Excel or CSV file
    
    Returns:
        pandas.DataFrame: The data from the file
    """
    try:
        # Check if file exists(os)
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return None
        
        # Read based on file extension
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:  # CSV or other formats
            df = pd.read_csv(file_path)
        
        # Print to console
        print(f"\n{'='*80}")
        print(f"Data from: {file_path}")
        print(f"{'='*80}")
        print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
        print(df.to_string())
        print(f"{'='*80}\n")
        
        return df
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


@app.route('/')
def display_data():
    """
    Display the data as an HTML table on the web interface.
    """
    # Read the CSV file from the workspace
    file_path = "weather_data.csv"
    df = read_excel_file(file_path)
    
    if df is None:
        return "<h1>Error: No data to display</h1>"
    
    # Convert DataFrame to HTML table
    html_table = df.head(100).to_html(classes='table table-striped')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data Viewer</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
            }}
            .info {{
                background-color: #e3f2fd;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th {{
                background-color: #007bff;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Data Viewer</h1>
            <div class="info">
                <p><strong>File:</strong> {file_path}</p>
                <p><strong>Total Rows:</strong> {df.shape[0]} | <strong>Columns:</strong> {df.shape[1]}</p>
                <p><em>Showing first 100 rows</em></p>
            </div>
            {html_table}
        </div>
    </body>
    </html>
    """
    
    return html_content

if __name__ == '__main__':
    print("\n🚀 Starting Flask server on http://localhost:8080")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='localhost', port=8080)
