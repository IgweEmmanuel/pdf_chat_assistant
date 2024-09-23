import bagel
import os

client = bagel.Client()

# Set environment variable
os.environ['BAGEL_API_KEY']

user_id = '136444225'

llama3_model_id = "3323b6c4-06ef-4949-b239-1a2b220e211d" #This is LLama3-8b model
response = client.buy_asset(
                    asset_id=llama3_model_id,
                    user_id=user_id
                )
print(response)
