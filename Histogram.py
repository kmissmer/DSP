import os
import sys
import matplotlib.pyplot as plt

def plot_file_size_histogram(directory):
    file_sizes = []

    # Iterate over files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_sizes.append(file_size)

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(file_sizes, bins=20, alpha=0.5)
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Frequency')
    plt.title('File Size Histogram')
    plt.grid(True)
    plt.show()  # Display histogram in the terminal

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Histogram.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    plot_file_size_histogram(directory_path)
