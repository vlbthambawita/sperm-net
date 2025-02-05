import json
import os

# Define file paths
input_file_path = "/global/D1/homes/vajira/data/sperm/visem_tracking/video_metadata/metadata.jsonl"
output_dir = "/global/D1/homes/vajira/data/sperm/visem_tracking/videos_only/per_video_json_files"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the input file and split into individual JSON files
with open(input_file_path, "r") as infile:
    for line in infile:
        entry = json.loads(line.strip())
        file_name = entry.get("file_name")
        file_name = file_name.split(".")[0] if file_name else None
        
        if file_name:
            output_file_path = os.path.join(output_dir, f"{file_name}.json")
            with open(output_file_path, "w") as outfile:
                json.dump(entry, outfile, indent=4)
        else:
            print("Warning: 'file_name' field is missing in the entry.")