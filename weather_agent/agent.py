# Chain Of Thought Prompting
# This prompt is designed to encourage the model to reason through problems step-by-step.

import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, Field
from typing import Optional

import json

load_dotenv()

client = OpenAI()

def run_command(command: str):
    result = os.system(command)
    return result

def get_weather(city :str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Sorry, I couldn't fetch the weather information right now."

available_tools = {
    "get_weather" : get_weather,
    "run_command" : run_command
}

SYSTEM_PROMPT = """
You're an expert AI assistant in resolving user-query using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done, The PLAN can be of multiple steps.
Once you think enough PLAN has been done finally you can give an OUTPUT.
You can also call a TOOL if required from the list of tools available.
For every tool call, wait for the oberve step to get the output of the tool.

Rules:
- Strictly follow the given json output format.
- Only run one step at a time.
- The sequence of steps is 
  START(where user gives an input), 
  PLAN(you plan what needs to be done, that can be multiple times), 
  OUTPUT(you give final answer,going to be displayed to the user).

  Output JSON format:-
  {step:"START" | "PLAN" | "OUTPUT" | "TOOL", content:"string", tool:"string", input:"string", output:"string"}

  Available TOOLS:
    1. get_weather(city :str) : Gives you the current weather of the city.
         Usage: {step:"TOOL", content:"get_weather('city_name')"}
         Note: You can call this tool only once in a single chain of thought.
    2. run_command(command :str) : Takes a system command as input and executes the command in user's system and returns the output from that command,or performs the action.
    


  Example 1:
  START: Hey, Can u solve 2+3*5/10 
  PLAN: {step:"PLAN", content:"Seems like user is asking for a mathematical calculation."}
  PLAN: {step:"PLAN", content:"According to BODMAS, I need to first do multiplication and division from left to right, then addition."}
  PLAN: {step:"PLAN", content:"Yes, BODMAS is the correct thing to be done here."}
  PLAN: {step:"PLAN", content:"first we must multiply 3*5=15"}
  PLAN: {step:"PLAN", content:"Now the new equation is 2+15/10"}
  PLAN: {step:"PLAN", content:"We must perform division now, so 15/10=1.5"}
  PLAN: {step:"PLAN", content:"Now the new equation is 2+1.5"}
  PLAN: {step:"PLAN", content:"Now we perform addition, so 2+1.5=3.5"}
  PLAN: {step:"PLAN", content:"Great, we have solved and finally left with 3.5 as answer"}
  OUTPUT: {step:"OUTPUT", content:"3.5"} 

  Example 2:
  START: What's the weather like in New York?
  PLAN: {step:"PLAN", content:"Seems like User is asking for the weather information."}
  PLAN: {step:"PLAN", content:"Lets see if we have any available tools from the list of available tools."}
  PLAN: {step:"PLAN", content:"Great, we have get_weather tool available for this query!"}
  PLAN: {step:"PLAN", content:"Calling the tool with the city name New York as argument."}
  PLAN: {step:"TOOL", "tool":"get_weather", "input":"New York"}
  PLAN: {step:"OBSERVE", "tool":"get_weather", "output":"The weather in New York is Partly cloudy +22°C"}
  PLAN: {step:"PLAN", content:"The tool has given the weather information, now I can provide the final answer to the user."}
  OUTPUT: {step:"OUTPUT", content:"The current weather in New York is Partly cloudy +22°C"}
"""

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: START, PLAN, OUTPUT, TOOL")
    content: Optional[str] = Field(None, description="The content of the step.")
    tool: Optional[str] = Field(None, description="The tool being used.")
    input: Optional[str] = Field(None, description="The input to the tool.")
    output: Optional[str] = Field(None, description="The output from the tool.")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👉 ")
    message_history.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.parse(
            model="gpt-4o-mini",
            response_format=MyOutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({ "role": "assistant", "content": raw_result })

        parsed_result = response.choices[0].message.parsed 

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🔧: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🔧: {tool_to_call} ({tool_input}) = {tool_response}")

            message_history.append({ "role": "developer", "content": json.dumps({
                "step": "OBSERVE",
                "tool": tool_to_call,
                "input": tool_input,
                "output": tool_response
            }) })
            continue

        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("✅", parsed_result.content)
            break

print("\n\n\n")