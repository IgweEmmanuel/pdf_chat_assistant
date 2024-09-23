
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig


# Adapter model path
adapter_path = "adapter_model"

# Load only the adapter config initially
peft_config = PeftConfig.from_pretrained(adapter_path)
base_model_name = "bagelnet/Llama-3-8B"

# Function to load the model with minimal GPU memory usage
def load_model():
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0,
        llm_int8_has_fp16_weight=False,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=quantization_config,
        device_map="auto",
        trust_remote_code=True
    )

    model = PeftModel.from_pretrained(base_model, adapter_path)
    return model

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

# This function will load the model only when needed
model = None

if model is None:
    print("Loading model... This may take a moment.")
    model = load_model()
    print("Model loaded successfully.")

def generate_response(conversation_history, max_length=200):
    # Prepare the prompt
    prompt = f"You are a helpful AI assistant. Provide a concise and relevant answer to the user's question. Only reply to the question\n\n{conversation_history}"
    # prompt += conversation_history
    # prompt += "Assistant: "

    # Encode the input prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)

    # Generate a response
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=input_ids.shape[1] + max_length,
            num_return_sequences=1,
            # no_repeat_ngram_size=2,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode and return the response
    response = tokenizer.decode(output[0][input_ids.shape[1]:], skip_special_tokens=True)
    return response.strip()
