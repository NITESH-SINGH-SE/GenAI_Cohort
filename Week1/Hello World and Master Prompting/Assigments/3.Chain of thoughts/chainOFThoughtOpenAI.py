from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

systemPrompt = """
You are an AI assitant and help person to solve Mathmatical Question
You solve a query in several step you think, you again think, an think again and validate the prediction and finally give the result.

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for the response.
3. Carefully read the query.

Output Format:
{{ step: "string", content: "string"}}

Example:
Input: What is 2 + 2?
Output: {{step: "think", content: "The user is asking me a mathematical question."}}
Output: {{step: "think", content: "The query is for simple arithmetic operation addition."}}
Output: {{step: "think", content: "There are two operands and one operation so it is binary additon."}}
Output: {{step: "think", content: "2 + 2 so I have to add 2 to 2 which will be 4."}}
Output: {{step: "predict", content: "4 should be the result."}}
Output: {{step: "validate", content: "Adding 2 more to 2 is 4"}}
Output: {{step: "result", content: "2 + 2 = 4"}}
"""

client = OpenAI()


msg = [{"role": "system", "content": systemPrompt}]
query = input("> ")
msg.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model = 'gpt-4.1-mini',
        response_format = {"type": "json_object"},
        messages = msg
    )
    parsed_response = json.loads(response.choices[0].message.content)
    newContent = parsed_response.get("content")
    print(newContent)
    msg.append({"role": "assistant", "content": response.choices[0].message.content})

    if parsed_response.get("step") == "result":
        break