from dotenv import load_dotenv
from typing import Any as AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
    temperature=0,
)

# Define the state structure
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

# Define node functions
def chatbot(state: MessagesState):
    response = llm.invoke(state.get("messages", []))
    return { 
                "messages": [response],
                "llm_calls": state.get("llm_calls", 0) + 1,
            }

def sampleNode(state: MessagesState):
    print("\n\n\n Inside Sample Node", state)
    return { "messages": ["Sample Message Appended!"] }

# Build the state graph
graph_builder = StateGraph(MessagesState)

# Add nodes
graph_builder.add_node("nodeA" , chatbot)
graph_builder.add_node("nodeB" , sampleNode)

# Add edges to connect nodes
graph_builder.add_edge(START, "nodeA")
graph_builder.add_edge("nodeA", "nodeB")
graph_builder.add_edge("nodeB", END)

# Compile the graph
graph = graph_builder.compile()

# Invoke the graph with an initial state
updated_state = graph.invoke({ "messages": ["Hi, do you know my name?"], "llm_calls": 0 })
print("Final State:", updated_state)

