import os
import shutil
import csv
from datetime import datetime

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the script directory
source_folder = os.path.join(script_directory, "problem1")
destination_folder = os.path.join(script_directory, "test")
report_file = os.path.join(destination_folder, "report.csv")
prefix_to_discard = "jdwjs-"

image_data = []

# Function to process the source folder and copy images to the destination folder
def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_folder, file.replace(prefix_to_discard, ""))
                shutil.copy(source_file_path, destination_file_path)
                
                file_info = os.stat(source_file_path)
                size = file_info.st_size / (1024 * 1024)  # Convert bytes to megabytes
                last_modified = datetime.fromtimestamp(file_info.st_mtime)
                
                image_data.append({
                    "image_name": file.replace(prefix_to_discard, ""),
                    "image_size": size,
                    "last_modified_date": last_modified
                })

# Main function to execute the script
def main():
    # Check if the destination folder already exists
    if os.path.exists(destination_folder):
        # Clear the contents of the destination folder
        for file in os.listdir(destination_folder):
            file_path = os.path.join(destination_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        # If the destination folder doesn't exist, create it
        os.makedirs(destination_folder)
    
    # Process the source folder
    process_folder(source_folder)
    
    # Write image data to a CSV report file
    with open(report_file, "w", newline="") as csvfile:
        fieldnames = ["image_name", "image_size_MB", "last_modified_date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in image_data:
            # Format the date as desired (e.g., "Sun July 26 2023 13:28:45")
            formatted_date = data["last_modified_date"].strftime("%a %B %d %Y %H:%M:%S")
            writer.writerow({
                "image_name": data["image_name"],
                "image_size_MB": "{:.2f} MB".format(data["image_size"]),
                "last_modified_date": formatted_date
            })

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
