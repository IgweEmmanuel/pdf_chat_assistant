import bagel
import os

client = bagel.Client()

# Set environment variable
os.environ['BAGEL_API_KEY']

asset_id = 'f501e8fd-73c8-4b97-9b51-d934814ff987'

file_path = 'generated_from_txt.parquet'

response = client.file_upload(
                            file_path=file_path,
                            asset_id=asset_id
                          )
print(response)
