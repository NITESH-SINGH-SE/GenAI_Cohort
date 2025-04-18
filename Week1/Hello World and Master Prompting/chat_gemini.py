from google import genai
from google.genai import types

import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# print(client)
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='How Manish can get girlfriend?'
)
print(response.text)