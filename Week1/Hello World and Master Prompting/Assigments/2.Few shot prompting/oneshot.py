from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

systemPrompt = """
Example: 
Input: "Why sky is blue?"
Output: "When sunlight collides with air molecules and small particles in atmosphere, light scatters in all direction. Due to shorter wavelength it is scattered teh modst and sky appears blue"
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
