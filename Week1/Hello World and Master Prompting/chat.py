from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "battery life of tesla 3"}
    ]
)

print(completion.choices[0].message.content)