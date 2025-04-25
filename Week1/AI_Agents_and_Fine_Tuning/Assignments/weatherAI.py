from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import os

load_dotenv()

client = OpenAI()

def get_weather(city: str):
    print("Tool Called for", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    }
}
    
systemPrompt = """
    You are a helpful AI assistant who is specialize in resolving user query.
    You work on start, plan, action, observe mode.
    For the given query and avaialable tool, plan a step by step execution on the planning,
    Select relevant tool from the available tool and based on the tool selection you perform an action to call the tool
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of the function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city.

    Example:
    User Query: What is the weather of new york?
    Output: {{"step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{"step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{"step": "action", "function": "get_weather", "input": "new york"}}
    Output: {{"step": "observe", "output": "12 Degree Cel"}}
    Output: {{"step": "output", "content": "The weather for new yorks seems to be 12 degrees." }}
"""
query = input("> ")
messages = [{"role": "system", "content": systemPrompt}]
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model = 'gpt-4.1-nano',
        response_format={"type": "json_object"},
        messages = messages
    )
    
    content = response.choices[0].message.content
    parsed_content = json.loads(content)

    messages.append({"role": "assistant", "content": content})
    print(response.choices[0].message.content)

    if parsed_content.get("step") == "action":
        required_tool = parsed_content.get("function")
        required_input = parsed_content.get("input")

        if required_tool in available_tools:
            output = available_tools[required_tool].get("fn")(required_input)
            messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})

    if parsed_content.get("step") == "output":
        break