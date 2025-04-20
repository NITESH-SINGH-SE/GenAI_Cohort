from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

while True:
    userInput = input("> ")
    if userInput.lower() == "exit":
        break
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role" : "user", 
            "content" : userInput}
        ]
    )
    print(response.choices[0].message.content)