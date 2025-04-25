from dotenv import load_dotenv
from transformers import AutoTokenizeer, AutoModelForCausalLM
import torch

load_dotenv()

model_name = "google/gemma-3-1b-it"

tokenizer =- AutoTokenizeer.from_pretrained(model_name)

input_prompt = [
    "The capital of India is"
]

tokenized = tokenizer(input_prompt, return_tensors="pt")

tokenized["input_ids"]

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dytype=torch.bfloat16
)

gen_result = model.generate(tokenized["input_ids"], max_new_tokens=25)

print(gen_result)

tokenizer.batch_decode(gen_result)

print(output)