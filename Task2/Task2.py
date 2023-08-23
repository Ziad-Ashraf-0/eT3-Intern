import sys
import json

if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

# Read the txt file and parse its contents
with open(input_file, 'r') as file:
    lines = file.readlines()

# Initialize the JSON structure
json_data = {
    "annotations": [
        {
            "result": []
        }
    ],
    "data": {
        "image": f"/data/upload/{input_file.split('.')[0]}.jpg"
    }
}

# Process each line of the txt file
for line in lines:
    parts = line.strip().split()
    x = float(parts[1]) * 100  # Scale the values
    y = float(parts[2]) * 100  # Scale the values
    width = float(parts[3]) * 100  # Scale the values
    height = float(parts[4]) * 100  # Scale the values

    annotation = {
        "image_rotation": 0,
        "value": {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "rotation": 0,
            "rectanglelabels": ["object"]
        }
    }

    json_data["annotations"][0]["result"].append(annotation)

# Convert the data to JSON format
json_string = json.dumps(json_data, indent=4)

# Write the JSON data to a file
output_file = f"{input_file.split('.')[0]}.json"
with open(output_file, 'w') as outfile:
    outfile.write(json_string)

print(f"Conversion completed. JSON saved to {output_file}")
