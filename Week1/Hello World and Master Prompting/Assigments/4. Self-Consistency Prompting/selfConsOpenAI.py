import re
import statistics
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def generateResult(query, requestedModel):
    completion = client.chat.completions.create(
        model = requestedModel,
        messages = [
            {"role": "user", "content": query}
        ]
    )

    return completion.choices[0].message.content

models = ['gpt-4.1-mini', 'gpt-4.1-nano', 'gpt-4o-mini']

query = """
A man standing on a road hold his umbrella at 30° with the vertical to keep the
rain away. He throws the umbrella and starts running at 10 km/hr. He finds that
raindrops are hitting his head vertically. What will be the speed of raindrops with respect to the
road?
Provide your answer in km/h, rounded to two decimal places.
"""

results = []

for i in range(len(models)):
    result = generateResult(query, models[i])
    results.append(result)
    print(f"Response {i+1}:\n{result}\n")

def extractAnswer(response):
    match = re.search(r'(\d+\.\d+)\s*km/h', response)
    if match:
        return float(match.group(1))
    return None

answers = [extractAnswer(result) for result in results]
validAnswers = [answer for answer in answers if answer is not None]
validAnswers

if validAnswers:
    finalAnswer = statistics.median(validAnswers)
    print(f"The most consistent answer is: {finalAnswer:.2f} km/h")
else:
    print(f"Unable to determine a consistent answer.")