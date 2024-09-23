import bagel
import os

client = bagel.Client()

# Set environment variable
os.environ['BAGEL_API_KEY']

finetuned_model_id = '9fbc2581-6a92-46fa-acb5-003b9efebac6'
response = client.download_model(finetuned_model_id)
print(response)
