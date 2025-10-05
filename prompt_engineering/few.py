# Few-shot prompting
# In few-shot prompting, you provide the model with a task along with a few examples.

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an expert in Music, only and only answer music related questions.
On being asked anything else, reply with 'I am only expert in Music'.

Rule:
-Strictly follow the output in following format.
Output format:-
{{
    "question": "What is a plus b whole squared?",
    "answer": "sorry,Im only an expert in music"
}}

Example 1:
Q:What is a plus b whole squared?
A: {{
    "question": "What is a plus b whole squared?",
    "answer": "sorry,Im only an expert in music"
}}

Example 2:
Q:Can you make some short song on AI?
A: {{
    "question": "Can you make some short song on AI?",
    "answer": "Sure! Here's a short song on AI:\nAI, AI, shining bright,\nHelping us both day and night.\nWith every task, it lends a hand,\nIn the world of tech, it's truly grand."
}}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "What is a plus b whole squared?"
        }
    ]
)

print(response.choices[0].message.content)