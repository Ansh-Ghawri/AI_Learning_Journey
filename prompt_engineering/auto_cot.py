# Auto-CoT (Chain of Thought) Prompting Example
# This script demonstrates how to implement an Auto-CoT prompting strategy using OpenAI's API.

# example usage: Q-hey,can u write a code in js that can take n number of arguments and add all the numbers as fast as possible with caching.

from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You're an expert AI assistant in resolving user-query using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done, The PLAN can be of multiple steps.
Once you think enough PLAN has been done finally you can give an OUTPUT.

Rules:
- Strictly follow the given json output format.
- Only run one step at a time.
- The sequence of steps is 
  START(where user gives an input), 
  PLAN(you plan what needs to be done, that can be multiple times), 
  OUTPUT(you give final answer,going to be displayed to the user).

  Output JSON format:-
  {step:"START" | "PLAN" | "OUTPUT", content:"string"}

  Example:
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
"""

print("\n\n\n")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

user_query = input("👉 ")
message_history.append({ "role": "user", "content": user_query })

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({ "role": "assistant", "content": raw_result })

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue
    if parsed_result.get("step") == "OUTPUT":
        print("✅", parsed_result.get("content"))
        break

print("\n\n\n")