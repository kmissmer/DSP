import json
import os
import sys
from bs4 import BeautifulSoup

def extract_year_from_docket_id(docket_id):
    if not docket_id:
        return None
    try:
        return int(docket_id.split('-')[1])  # Extract the year part from the docket_id
    except (IndexError, ValueError):
        return None

def process_json_file(file_path, docket_id):
    try:
        with open(file_path, 'r') as json_file:
            comments = json.load(json_file)
            if isinstance(comments, int):
                return {"docket_id": docket_id, "comments": comments}
            elif isinstance(comments, list) or isinstance(comments, dict):
                comments_count = len(comments)
                return {"docket_id": docket_id, "comments": comments_count}
            else:
                print(f"Invalid JSON format in file: {file_path}")
                return None
    except Exception as e:
        print(f"An error occurred while processing JSON file {file_path}: {e}")
        return None

def process_txt_file(file_path, docket_id):
    try:
        with open(file_path, 'r') as txt_file:
            lines = txt_file.readlines()
            comments_count = len(lines)
            return {"docket_id": docket_id, "comments": comments_count}
    except Exception as e:
        print(f"An error occurred while processing TXT file {file_path}: {e}")
        return None

def process_htm_file(file_path, docket_id):
    try:
        with open(file_path, 'r') as htm_file:
            soup = BeautifulSoup(htm_file, 'html.parser')
            rows = soup.find_all('tr')
            comments_count = len(rows) - 1  # Assuming the first row is the header
            return {"docket_id": docket_id, "comments": comments_count}
    except Exception as e:
        print(f"An error occurred while processing HTML file {file_path}: {e}")
        return None

def process_file(file_path):
    path_components = file_path.split(os.sep)
    if len(path_components) >= 4:
        docket_id = path_components[3]
        if file_path.endswith(".json"):
            return process_json_file(file_path, docket_id)
        elif file_path.endswith(".txt"):
            return process_txt_file(file_path, docket_id)
        elif file_path.endswith(".htm") or file_path.endswith(".html"):
            return process_htm_file(file_path, docket_id)
        else:
            print(f"Unsupported file type: {file_path}")
            return None
    else:
        print(f"Invalid file path format: {file_path}")
        return None

def process_dockets(directory_path):
    all_dockets = []

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            docket_info = process_file(file_path)
            if docket_info:
                all_dockets.append(docket_info)
    
    # Filter dockets from 2024
    dockets_2024 = [docket for docket in all_dockets if extract_year_from_docket_id(docket['docket_id']) == 2024]
    
    # Sort dockets by the number of comments in descending order
    sorted_dockets = sorted(dockets_2024, key=lambda x: x['comments'], reverse=True)
    
    # Get the top 50 dockets
    top_50_dockets = sorted_dockets[:50]
    
    # Print the top 50 dockets
    for i, docket in enumerate(top_50_dockets, start=1):
        print(f"{i}. Docket ID: {docket['docket_id']}, Comments: {docket['comments']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 NumCommentsPDocket.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        process_dockets(directory_path)
