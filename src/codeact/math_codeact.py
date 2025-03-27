import os
import builtins
import contextlib
import io
from typing import Any

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph_codeact import create_codeact

from codeact.math_tools import multiply, add, divide, subtract, sin, cos, radians, exponentiation, sqrt, ceil

"""
pip install langgraph-codeact
https://github.com/langchain-ai/langgraph-codeact
"""

os.environ["DEEPSEEK_API_KEY"] = "..."

tools = [
    add,
    multiply,
    divide,
    subtract,
    sin,
    cos,
    radians,
    exponentiation,
    sqrt,
    ceil,
]


def eval(code: str, _locals: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    # Store original keys before execution
    original_keys = set(_locals.keys())

    try:
        with contextlib.redirect_stdout(io.StringIO()) as f:
            exec(code, builtins.__dict__, _locals)
        result = f.getvalue()
        if not result:
            result = "<code ran, no output printed to stdout>"
    except Exception as e:
        result = f"Error during execution: {repr(e)}"

    # Determine new variables created during execution
    new_keys = set(_locals.keys()) - original_keys
    new_vars = {key: _locals[key] for key in new_keys}
    return result, new_vars


model = init_chat_model("deepseek-chat", model_provider="deepseek")

code_act = create_codeact(model, tools, eval)
agent = code_act.compile(checkpointer=MemorySaver())

if __name__ == "__main__":

    messages = [
        {
            "role": "user",
            "content": "A batter hits a baseball at 45.847 m/s at an angle of 23.474° above the horizontal. "
                       "The outfielder, who starts facing the batter, picks up the baseball as it lands, "
                       "then throws it back towards the batter at 24.12 m/s at an angle of 39.12 degrees. "
                       "How far is the baseball from where the batter originally hit it? Assume zero air resistance.",
        }
    ]
    for typ, chunk in agent.stream(
        {"messages": messages},
        stream_mode=["values", "messages"],
        config={"configurable": {"thread_id": 1}},
    ):
        if typ == "messages":
            print(chunk[0].content, end="")
        elif typ == "values":
            print("\n\n---answer---\n\n", chunk)