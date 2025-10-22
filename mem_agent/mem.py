from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "1.1",
    "embedder": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "text-embedding-3-small" } 
    },
    "llm": {
        "provider": "openai",
        "config": { "api_key": OPENAI_API_KEY, "model": "gpt-4.1" } 
    },
    "graph_store": {
        "provider": "neo4j",
        "config": { 
            "url": os.getenv("NEO_CONNECTION_URI"),
            "username": os.getenv("NEO_USERNAME"),
            "password": os.getenv("NEO_PASSWORD"),
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": { "host": "localhost", "port": 6333 }
    }
}
mem_client = Memory.from_config(config)

while True:

    user_query = input("> ")

    search_memory = mem_client.search(
        user_id="anshghawri",
        query=user_query,
    )

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]

    print("Found Memories ", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user: 
        {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content
    print("AI:", ai_response)

    mem_client.add(
        user_id="anshghawri",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("Conversation saved to memory...")