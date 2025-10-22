from dotenv import load_dotenv
from typing import Any as AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver 
from langchain_core.messages import HumanMessage

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
    temperature=0,
)

# Define the state structure
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# Define node functions
def chatbot(state: MessagesState):
    response = llm.invoke(state.get("messages", []))
    return { "messages": [response] }

# Build the state graph
graph_builder = StateGraph(MessagesState)

# Add nodes
graph_builder.add_node("nodeA" , chatbot)

# Add edges to connect nodes
graph_builder.add_edge(START, "nodeA")
graph_builder.add_edge("nodeA", END)

# Compile the graph
graph = graph_builder.compile()

# Compile the graph with MongoDB checkpointer
def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

# Invoke the graph with an initial state

DB_URI = "mongodb://admin:admin@localhost:27017"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer: 
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config ={
                "configurable": {
                    "thread_id": "ansh" # user ID (different users can have different threads)
                }
            }

    for chunk in graph_with_checkpointer.stream(
        MessagesState({ "messages": [HumanMessage(content="what is my name")] }), 
        config,
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
