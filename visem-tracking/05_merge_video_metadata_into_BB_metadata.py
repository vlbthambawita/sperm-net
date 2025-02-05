import json
import os
import csv
from collections import defaultdict

# Define file paths
metadata_file_path = "/global/D1/homes/vajira/data/sperm/visem_tracking/image_metadata/metadata.jsonl"  # Update with actual path
metadata_csv_path = "/global/D1/homes/vajira/data/sperm/visem/visem-dataset/metadata_CSV/metadata.csv"  # Path to CSV file
output_file_path = "/global/D1/homes/vajira/data/sperm/visem_tracking/video_metadata/metadata_merged.jsonl"  # Output JSONL

# Dictionary to store consolidated data per video
video_data = defaultdict(lambda: {"file_name": "", "video_id": "", "frames": [], "features": {}})

# Step 1: Read metadata.jsonl (group frames per video)
with open(metadata_file_path, "r") as file:
    for line in file:
        entry = json.loads(line.strip())

        # Extract video ID from frame file name (assuming format "videoID_frame_xxx.jpg")
        frame_file_name = entry["file_name"]
        video_id = frame_file_name.split("_frame_")[0]  # Extract video ID
        frame_id = frame_file_name.split("_frame_")[-1].split(".")[0]  # Extract frame number

        # Initialize video entry if not already done
        if not video_data[video_id]["file_name"]:
            video_data[video_id]["file_name"] = f"{video_id}.mp4"
            video_data[video_id]["video_id"] = video_id

        # Structure the frame data
        frame_data = {
            "frame_id": frame_id,
            "image_width": entry["image_width"],
            "image_height": entry["image_height"],
            "objects": entry["objects"],
        }

        # Append frame data to corresponding video
        video_data[video_id]["frames"].append(frame_data)

# Step 2: Read metadata.csv and add additional video-level features
with open(metadata_csv_path, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)  # Read CSV as a dictionary

    for row in csv_reader:
        video_file_name = row["file_name"]  # Get the file_name from CSV
        video_id = os.path.splitext(video_file_name)[0]  # Extract video ID (remove .avi, .mp4, etc.)

        # If the video exists in our JSON data, add its features
        if video_id in video_data:
            video_data[video_id]["features"] = {key: value for key, value in row.items() if key != "file_name"}

# Step 3: Write the merged data to a new JSONL file
with open(output_file_path, "w") as jsonl_file:
    for video_entry in video_data.values():
        jsonl_file.write(json.dumps(video_entry) + "\n")

print(f"Merged metadata saved to {output_file_path}")