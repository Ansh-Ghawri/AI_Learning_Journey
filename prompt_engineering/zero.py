# Zero-shot prompting
# In zero-shot prompting, you directly provide the model with a task without any examples.

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = "You are an expert in Music, only and only answer music related questions.On being asked anything else, reply with 'I am only expert in Music'."

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Can u help me solve a plus b whole squared?"
        }
    ]
)

print(response.choices[0].message.content)