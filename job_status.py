import bagel
import os
import time


client = bagel.Client()


# Set environment variable
os.environ['BAGEL_API_KEY']

model_id = '9fbc2581-6a92-46fa-acb5-003b9efebac6'
# response = client.get_job_by_asset_id(model_id)
# print(response)


while True:
  response = client.get_job_by_asset_id(model_id)
  print(response[1]["job_status"])
  if response[1]["job_status"] == "JobState.JOB_STATE_SUCCEEDED":
    print("Model fine-tuned successfully")
    break
  if response[1]["job_status"] == "JobState.JOB_STATE_FAILED":
    print("Model fine-tuning failed")
    break
  time.sleep(10)
