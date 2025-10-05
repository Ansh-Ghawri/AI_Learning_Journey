# Chain Of Thought Prompting
# This prompt is designed to encourage the model to reason through problems step-by-step.

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

response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": "Hey,write a code to add n numbers in js." },
        
        # Manually, keep adding messages to History as the conversation progresses
        { "role": "assistant", "content": json.dumps({ "step": "START", "content": "User is requesting a JavaScript code snippet to add n numbers." }) },
        { "role": "assistant", "content": json.dumps({"step": "PLAN", "content": "First, I need to determine how to take input from the user for n numbers."}) },
        { "role": "assistant", "content": json.dumps({"step": "PLAN", "content": "Next, I will need to create a function that allows for summing those n numbers."}) },
        { "role": "assistant", "content": json.dumps({"step": "PLAN", "content": "I should consider using an array to store the n numbers and then iterating through the array to calculate the sum."}) },
        { "role": "assistant", "content": json.dumps({"step": "PLAN", "content": "I must ensure to return the sum at the end of the function."}) },
        { "role": "assistant", "content": json.dumps({"step": "PLAN", "content": "Finally, I will write the complete code that demonstrates this approach."}) },

        # Finally the OUTPUT step:
        # {"step": "OUTPUT", "content": "Here's a JavaScript code snippet to add n numbers:\n\n```javascript\nfunction addNumbers(numbers) {\n    let sum = 0;\n    for (let num of numbers) {\n        sum += num;\n    }\n    return sum;\n}\n\n// Example usage:\nconst n = [1, 2, 3, 4, 5]; // You can change this array to add different numbers\nconsole.log(addNumbers(n)); // Output will be the sum of numbers in the array\n```"}
    ]
)

print(response.choices[0].message.content)