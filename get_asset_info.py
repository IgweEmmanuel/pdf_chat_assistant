import bagel
import os

client = bagel.Client()

# Set environment variable
os.environ['BAGEL_API_KEY']

asset_id = 'f501e8fd-73c8-4b97-9b51-d934814ff987'

asset_info = client.get_asset_info(asset_id)
print(asset_info)
