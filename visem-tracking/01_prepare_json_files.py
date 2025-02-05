# %%
import os
import json
import glob
from PIL import Image

# %%
# Define paths
yolo_annotations_folder = "/global/D1/homes/vajira/data/sperm/visem_tracking/yolo_BB_with_feid"  # Update this path
image_folder = "/global/D1/homes/vajira/data/sperm/visem_tracking/extracted_frames_with_BB"  # Update this path
output_jsonl = "/global/D1/homes/vajira/data/sperm/visem_tracking/metadata/metadata.jsonl"

# %%
# Function to convert YOLO bbox to COCO format
def yolo_to_coco(x_center, y_center, width, height, img_width, img_height):
    x_min = (x_center - width / 2) * img_width
    y_min = (y_center - height / 2) * img_height
    w = width * img_width
    h = height * img_height
    return [x_min, y_min, w, h]

# %%
# Process each YOLO annotation file
metadata = []
for txt_file in glob.glob(os.path.join(yolo_annotations_folder, "*.txt")):
    # Extract frame details from filename
    file_name = os.path.basename(txt_file).replace("_with_ftid.txt", ".jpg")
    image_path = os.path.join(image_folder, file_name)

    # Skip if image does not exist
    if not os.path.exists(image_path):
        print(f"Skipping {file_name}, image not found.")
        continue

    # Get image dimensions
    with Image.open(image_path) as img:
        img_width, img_height = img.size

    objects = {"yolo_bbox": [], "coco_bbox": [], "categories": [], "feature_ids": []}

    # Read YOLO annotation file
    with open(txt_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue  # Skip invalid lines

            feature_id, class_id, x_center, y_center, width, height = parts
            x_center, y_center, width, height = map(float, [x_center, y_center, width, height])
            
            # Convert to COCO format
            coco_bbox = yolo_to_coco(x_center, y_center, width, height, img_width, img_height)
            
            # Store in objects dictionary
            objects["yolo_bbox"].append([x_center, y_center, width, height])  # YOLO format
            objects["coco_bbox"].append(coco_bbox)  # COCO format
            objects["categories"].append(int(class_id))
            objects["feature_ids"].append(feature_id)

    # Construct metadata entry
    entry = {
        "file_name": file_name,
        "image_width": img_width,
        "image_height": img_height,
        "objects": objects,
    }
    metadata.append(entry)

# Write to JSONL file
with open(output_jsonl, "w") as jsonl_file:
    for entry in metadata:
        jsonl_file.write(json.dumps(entry) + "\n")

print(f"Metadata saved to {output_jsonl}")

# %%



