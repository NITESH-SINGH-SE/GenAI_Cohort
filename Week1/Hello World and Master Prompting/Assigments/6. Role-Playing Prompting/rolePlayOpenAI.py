from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

systemPrompt = """
You are a person from 9th century, you dont believe in science.
You perform sacred rituals and live in tribal community.
You have never crossed the seas.
All your education is based on your ancestors and forest.
"""

while True:
    query = input("> ")
    if query == "exit":
        break
    
    response = client.chat.completions.create(
        model = 'gpt-4.1-mini',
        messages = [
            {
                "role": "system",
                "content": systemPrompt
            },
            {
                "role": "user",
                "content": query
            },
        ]
    )

    print(response.choices[0].message.content)
