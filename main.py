from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI() 

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an expert in Music, only and only answer music related questions.On being asked anything else, reply with 'I am only expert in Music'."
        },
        {
            "role": "user",
            "content": "Can you make some short song on AI?"
        }
    ]
)

print(response.choices[0].message.content)