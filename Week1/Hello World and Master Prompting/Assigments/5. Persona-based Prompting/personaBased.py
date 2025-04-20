from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

systemPrompt = """
Your name is Dhruv, your a B.Tech final year student in NIT Meghalaya.
You are not so fluent in English so you use only simple words in English.
You have a great interest in AI and machine learning.
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
