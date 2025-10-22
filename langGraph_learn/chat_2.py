from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    print('ChatBot node', state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")},
        ],
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def chatbot_gemini(state: State):
    print('chatbot_gemini node', state)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": state.get("user_query")},
        ],
    )

    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state: State) -> Literal["endNode", "chatbot_gemini"]:
    print('evaluate_response node', state)
    if False:
        return "endNode"
    
    return "chatbot_gemini"


def end_node(state: State):
    print('endnode Node', state)
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endNode", end_node)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)
graph_builder.add_edge("chatbot_gemini", "endNode")
graph_builder.add_edge("endNode", END)

graph = graph_builder.compile()

updated_state = graph.invoke({"user_query": "What is 2+2?"})
print("Final State:", updated_state)