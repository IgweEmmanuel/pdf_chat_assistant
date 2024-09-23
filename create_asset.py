import bagel
import os

client = bagel.Client()


# Set environment variable
os.environ['BAGEL_API_KEY']


def create_asset(client):
    title = "creamcheese_dataset_chatbot_test" #@param
    description = "Cream Cheese dataset_test" #@param
    user_id = '136444225'
    payload = {
                "title": title,
                "dataset_type": "RAW",
                "tags": [
                    "AI", "TEST"
                ],
                "category": "AI",
                "details": description,
                "user_id": user_id
            }

    dataset = client.create_asset(
        payload=payload
    )
    return dataset

asset_id = create_asset(client)
print(asset_id)
