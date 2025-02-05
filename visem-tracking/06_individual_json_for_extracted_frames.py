import os
import json
import glob
from PIL import Image

# Define paths
image_folder = "/global/D1/homes/vajira/data/sperm/visem_tracking/extracted_frames_with_BB"  # Update this path
yolo_annotations_folder = "/global/D1/homes/vajira/data/sperm/visem_tracking/yolo_BB_with_feid"  # Update this path
output_json_folder = "/global/D1/homes/vajira/data/sperm/visem_tracking/extracted_json_per_image"  # Update this path

# Ensure output directory exists
os.makedirs(output_json_folder, exist_ok=True)

# Function to convert YOLO bbox to COCO format
def yolo_to_coco(x_center, y_center, width, height, img_width, img_height):
    x_min = (x_center - width / 2) * img_width
    y_min = (y_center - height / 2) * img_height
    w = width * img_width
    h = height * img_height
    return [x_min, y_min, w, h]

# Process each image in the image folder
for img_path in glob.glob(os.path.join(image_folder, "*.jpg")):
    file_name = os.path.basename(img_path)
    frame_id = os.path.splitext(file_name)[0]  # Extract frame ID without extension
    annotation_file = os.path.join(yolo_annotations_folder, f"{frame_id}_with_ftid.txt")
    
    # Get image dimensions
    with Image.open(img_path) as img:
        img_width, img_height = img.size

    objects = {"yolo_bbox": [], "coco_bbox": [], "categories": [], "feature_ids": []}

    # Check if YOLO annotation file exists
    if os.path.exists(annotation_file):
        with open(annotation_file, "r") as f:
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

    # Save as individual JSON file
    json_output_path = os.path.join(output_json_folder, f"{frame_id}.json")
    with open(json_output_path, "w") as json_file:
        json.dump(entry, json_file, indent=4)

print(f"Individual JSON files saved to {output_json_folder}")