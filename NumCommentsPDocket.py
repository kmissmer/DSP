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

def process_json_file(file_path):
    with open(file_path, 'r') as json_file:
        dockets = json.load(json_file)
        if isinstance(dockets, list):
            return dockets
        else:
            print(f"Invalid JSON format in file: {file_path}")
            return []

def process_txt_file(file_path):
    dockets = []
    with open(file_path, 'r') as txt_file:
        lines = txt_file.readlines()
        for line in lines:
            try:
                docket_id, comments = line.strip().split(',')
                comments = int(comments)
                dockets.append({"docket_id": docket_id, "comments": comments})
            except ValueError:
                print(f"Invalid line format in file: {file_path}")
    return dockets

def process_htm_file(file_path):
    dockets = []
    with open(file_path, 'r') as htm_file:
        soup = BeautifulSoup(htm_file, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                docket_id = cols[0].text.strip()
                try:
                    comments = int(cols[1].text.strip())
                    dockets.append({"docket_id": docket_id, "comments": comments})
                except ValueError:
                    print(f"Invalid comment number in file: {file_path}")
    return dockets

def process_dockets(directory_path):
    all_dockets = []

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".json"):
                try:
                    all_dockets.extend(process_json_file(file_path))
                except Exception as e:
                    print(f"An error occurred while processing JSON file {file_path}: {e}")
            elif file.endswith(".txt"):
                try:
                    all_dockets.extend(process_txt_file(file_path))
                except Exception as e:
                    print(f"An error occurred while processing TXT file {file_path}: {e}")
            elif file.endswith(".htm") or file.endswith(".html"):
                try:
                    all_dockets.extend(process_htm_file(file_path))
                except Exception as e:
                    print(f"An error occurred while processing HTML file {file_path}: {e}")
    
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
