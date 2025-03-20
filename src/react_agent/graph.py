import os
from datetime import datetime, timezone
from typing import Dict, List, Literal, cast

from langchain_community.chat_models import ChatTongyi

from react_agent.configuration import Configuration
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from react_agent.state import State, InputState
from react_agent.tools import TOOLS

os.environ["DASHSCOPE_API_KEY"] = "..."
"""
pip install --upgrade --quiet  dashscope
"""


async def call_model(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our "react_agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)

    # model = ChatDeepSeek(
    #     model=configuration.model,
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    # ).bind_tools(TOOLS)

    model = ChatTongyi().bind_tools(TOOLS)

    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}


graph_builder = StateGraph(State, input=InputState, config_schema=Configuration)

graph_builder.add_node("call_model", call_model)
graph_builder.add_node("tools", ToolNode(TOOLS))

graph_builder.add_edge("__start__", "call_model")


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """Determine the next node based on the model's output.

    This function checks if the model's last message contains tool calls.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: The name of the next node to call ("__end__" or "tools").
    """
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # If there is no tool call, then we finish
    if not last_message.tool_calls:
        return "__end__"
    # Otherwise we execute the requested actions
    return "tools"


graph_builder.add_conditional_edges(
    "call_model",
    route_model_output,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "call_model")

# memory = MemorySaver()

# Compile the builder into an executable graph
# You can customize this by adding interrupt points for state updates
graph = graph_builder.compile(
    # interrupt_before=[],  # Add node names here to update state before they're called
    # interrupt_after=[],  # Add node names here to update state after they're called
    # checkpointer=memory,
)

graph.name = "New Graph"  # This defines the custom name in LangSmith
