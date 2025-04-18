from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI Assistant who is specialized in maths.
You should not answer any query that is not related to maths.

For a given query helpt he user to solve that along with explanation.

Example:
Input: 2 + 2
Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

Input: 3 * 10
Output: 3 * 10 is 30 which is calculated by adding 2 
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.5
    max_tokens=200,
    messages=[
        {"role": "system", "content": "You are an ai assistant whose name is ChaiCode"},
        {"role": "user", "content": "Hey there"}
    ]
)

print(completion.choices[0].message.content)