from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os

load_dotenv()

client = OpenAI()

def query_db(sql):
    pass

def run_command(command):
    result = os.system(command=command)
    return result

# print(run_command("dir"))


def get_weather(city: str):
    print("Tool Called for", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"Ther weather in {city} is {response.text}."

    return "Something went wrong"

# def add(x, y):
#     print("Tool Called: add", x, y)
#     return x + y

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output."
    }
}

systemPrompt = """
    You are a helpfull AI assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plain the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: "Takes a command as input to execute on system and returns output."
    # - add: Take two numbers x and y and returns sum of the given input that is x + y


    Example:
    User Query: What is the weather of new york?
    Output: {{"step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{"step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{"step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{"step": "observe", "output": "12 Degree Cel" }}
    Output: {{"step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""

while True:
    userQuery = input("> ")

    if userQuery == "bye":
        break

    messages = [{ "role": "system", "content": systemPrompt}]
    messages.append({"role": "user", "content": userQuery})


    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsedOutput = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsedOutput)})

        print(f"{parsedOutput.get('content')}")

        if parsedOutput.get("step") == "action":
            tool_name = parsedOutput.get("function")
            tool_input = parsedOutput.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({ "step": "observe", "output": output })})
                continue

        if parsedOutput.get("step") == "output":
            print(f"{parsedOutput.get("content")}")
            break
