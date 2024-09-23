import zipfile
import os

# Path to the zip file
zip_file_path = '9fbc2581-6a92-46fa-acb5-003b9efebac6.zip'

# Destination directory to extract to
destination_dir = './adapter_model'

# Ensure destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(destination_dir)

print(f"Unzipped to {destination_dir}")

