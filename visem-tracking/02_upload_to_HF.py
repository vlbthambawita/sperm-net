import os
import glob
import time
from huggingface_hub import HfApi, HfFolder
from tqdm import tqdm

# --- Configuration ---
REPO_ID = "sperm-net/VISEM-Tracking"  # Existing Hugging Face dataset repo
IMAGE_FOLDER = "/global/D1/homes/vajira/data/sperm/visem_tracking/extracted_frames_with_BB"  # Update this with your local image folder
UPLOAD_PATH = "data/extracted_frames_with_BB"  # Target folder in repo
BATCH_SIZE = 50  # Adjust based on network speed
# HF_TOKEN = "your_huggingface_token"  # Use your Hugging Face token or login via CLI

# Initialize Hugging Face API
api = HfApi()

# Ensure authentication
#HfFolder.save_token(HF_TOKEN)

# Get list of image files
image_files = sorted(glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg")))

# Function to upload a batch
def upload_batch(batch_files, batch_num):
    for image_path in tqdm(batch_files, desc=f"Uploading Batch {batch_num}"):
        file_name = os.path.basename(image_path)
        repo_path = f"{UPLOAD_PATH}/{file_name}"  # Upload target path

        try:
            api.upload_file(
                path_or_fileobj=image_path,
                path_in_repo=repo_path,
                repo_id=REPO_ID,
                repo_type="dataset",
            )
        except Exception as e:
            print(f"❌ Error uploading {file_name}: {e}")

# Process images in batches
total_batches = len(image_files) // BATCH_SIZE + (1 if len(image_files) % BATCH_SIZE else 0)

for i in range(total_batches):
    start_idx = i * BATCH_SIZE
    end_idx = start_idx + BATCH_SIZE
    batch_files = image_files[start_idx:end_idx]

    print(f"🚀 Uploading batch {i+1}/{total_batches} ({len(batch_files)} images)...")
    upload_batch(batch_files, i + 1)

    # Optional delay to avoid rate limits
    time.sleep(2)

print("✅ All images uploaded successfully to Hugging Face!")