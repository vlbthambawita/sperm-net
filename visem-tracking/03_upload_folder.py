import os
from huggingface_hub import HfApi

# --- Configuration ---
REPO_ID = "sperm-net/VISEM-Tracking"  # Existing Hugging Face dataset repo
FOLDER_PATH = "/global/D1/homes/vajira/data/sperm/visem_tracking/extracted_frames_with_BB"  # Update with your actual folder path
TARGET_PATH = "data/extracted_frames_with_BB"  # Destination folder inside the repo
#HF_TOKEN = "your_huggingface_token"  # Use your Hugging Face token or login via CLI

# Initialize API
api = HfApi()

# Upload the entire folder
api.upload_folder(
    folder_path=FOLDER_PATH,   # Local folder to upload
    repo_id=REPO_ID,           # Hugging Face dataset repo
    repo_type="dataset",       # Uploading to a dataset
    path_in_repo=TARGET_PATH,  # Target folder inside repo          
    # Authentication token
)

print("✅ Folder uploaded successfully to Hugging Face!")