import pandas as pd
import json
import os
import sys

def json_to_csv(json_file_path, csv_file_path=None):
    try:
        # Load the JSON data from the file
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Convert JSON data to pandas DataFrame
        df = pd.json_normalize(json_data)
        
        # Determine output CSV file path
        if csv_file_path is None:
            # If csv_file_path is not provided, generate it based on json_file_path
            base_name = os.path.splitext(os.path.basename(json_file_path))[0]
            csv_file_path = os.path.join(os.path.dirname(json_file_path), f"{base_name}.csv")
        
        # Save DataFrame to CSV
        df.to_csv(csv_file_path, index=False)
        
        print(f"JSON data successfully converted to CSV and saved to {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_csv.py <json_file_path>")
    else:
        json_file_path = sys.argv[1]
        json_to_csv(json_file_path)
