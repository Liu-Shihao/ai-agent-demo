import os
from typing import Annotated

from langchain_community.chat_models import ChatTongyi
from langchain_core.tools.base import InjectedToolCallId
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command


os.environ["DEEPSEEK_API_KEY"] = "..."
os.environ["DASHSCOPE_API_KEY"] = "..."


# model = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )


model = ChatTongyi(
    model="qwen-plus"
)

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b


def make_handoff_tool(*, agent_name: str):
    """Create a tool that can return handoff via a Command"""
    tool_name = f"transfer_to_{agent_name}"

    @tool(tool_name)
    def handoff_to_agent(
            # # optionally pass current graph state to the tool (will be ignored by the LLM)
            state: Annotated[dict, InjectedState],
            # optionally pass the current tool call ID (will be ignored by the LLM)
            tool_call_id: Annotated[str, InjectedToolCallId],
    ):
        """Ask another react_agent for help."""
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": tool_name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            # navigate to another react_agent node in the PARENT graph
            goto=agent_name,
            graph=Command.PARENT,
            # This is the state update that the react_agent `agent_name` will see when it is invoked.
            # We're passing react_agent's FULL internal message history AND adding a tool message to make sure
            # the resulting chat history is valid. See the paragraph above for more information.
            update={"messages": state["messages"] + [tool_message]},
        )

    return handoff_to_agent


addition_expert = create_react_agent(
    model,
    [add, make_handoff_tool(agent_name="multiplication_expert")],
    prompt="You are an addition expert, you can ask the multiplication expert for help with multiplication.",
)

multiplication_expert = create_react_agent(
    model,
    [multiply, make_handoff_tool(agent_name="addition_expert")],
    prompt="You are a multiplication expert, you can ask an addition expert for help with addition.",
)

builder = StateGraph(MessagesState)
builder.add_node("addition_expert", addition_expert)
builder.add_node("multiplication_expert", multiplication_expert)
builder.add_edge(START, "addition_expert")
graph = builder.compile()