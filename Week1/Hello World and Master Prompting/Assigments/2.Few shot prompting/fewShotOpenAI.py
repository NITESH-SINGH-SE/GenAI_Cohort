from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

systemPrompt = """
Example: 
Input: "Why is it raining today?"
Output: "The cloud had a breakup today, so he is crying."

Input: "Why was the flight delayed?"
Output: "There was huge traffic in the sky."

Input: "Why there is 7 colors in rainbow?"
Output: "Bro, 7 thala for a reason."

Input: "Is it safe to go out at night?"
Output: "Don't worry the garbage truck comes at morning."
"""

while True:
    userInput = input("> ")
    if userInput == "exit":
        break

    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
                { "role": "system", "content": systemPrompt },
                { "role": "user", "content": userInput}
            ]
    )

    print(response.choices[0].message.content)
