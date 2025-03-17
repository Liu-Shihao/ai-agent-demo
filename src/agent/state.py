from __future__ import annotations

from typing_extensions import TypedDict

from dataclasses import dataclass
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated


@dataclass
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]