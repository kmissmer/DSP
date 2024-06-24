import os
import sys

def count_files_per_docket(directory_path):
    file_counts = {}

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            docket_id = os.path.basename(root)
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.json', '.txt', '.htm', '.html']:
                if docket_id not in file_counts:
                    file_counts[docket_id] = 0
                file_counts[docket_id] += 1
    
    # Sort dockets by the number of files in descending order
    sorted_dockets = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)

    # Get the top 50 dockets
    top_50_dockets = sorted_dockets[:50]

    return top_50_dockets

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 NumFilesPerDocket.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        top_50_dockets = count_files_per_docket(directory_path)

        # Display the top 50 dockets with their file counts
        for i, (docket_id, count) in enumerate(top_50_dockets, start=1):
            print(f"{i}. Docket - {docket_id}: {count} files")
