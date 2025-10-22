from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    embedding=embedding_model,
    collection_name="learning_AI_agents",
)
print("Connection to vector database established...")

# Take User input
user_query = input("Ask something: ")

# Relevant chunks from the vector database
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join(f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results)

SYSTEM_PROMPT = """
You are an helpful AI assistant that answers user query based on the context provided retrieved from a PDF file along with page_contents and page_number.

You should only answer the user based on the following context and navigate the user to open the right page number to know more.

Context: {context}
"""

response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {"role": "user", "content": user_query},
    ],
)

print(f"🤖: {response.choices[0].message.content}")