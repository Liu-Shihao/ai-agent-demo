
from typing import Any, Dict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langchain_deepseek import ChatDeepSeek
from agent.configuration import Configuration
from agent.state import State

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def call_model(state, config):
    response = model.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("call_model", call_model)

# Set the entrypoint as `call_model`
workflow.add_edge("__start__", "call_model")

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
