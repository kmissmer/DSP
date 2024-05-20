import os
import sys
import matplotlib.pyplot as plt

def plot_file_size_histogram(directory):
    json_files = []
    html_files = []
    txt_files = []

    # Iterate over files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)

            # Categorize files based on extension
            if file.endswith('.json'):
                json_files.append(file_size)
            elif file.endswith('.htm') or file.endswith('.html'):
                html_files.append(file_size)
            elif file.endswith('.txt'):
                txt_files.append(file_size)

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(json_files, bins=20, alpha=0.5, label='JSON')
    plt.hist(html_files, bins=20, alpha=0.5, label='HTML')
    plt.hist(txt_files, bins=20, alpha=0.5, label='TXT')
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Frequency')
    plt.title('File Size Histogram')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Histogram.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    plot_file_size_histogram(directory_path)
