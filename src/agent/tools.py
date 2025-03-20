import json
from typing import List, Callable, Any

from langchain_core.tools import tool
from langgraph.types import Command, interrupt
from pymilvus import MilvusClient
from agent.embedding_utils import get_embeddings

client = MilvusClient("data/milvus_demo.db")


async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    result = a * b
    return result


async def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]


async def milvus_search(query: str) -> str:
    """
    Search milvus for a query
    :param query: query for milvus search
    :return: milvus search result
    """
    collection_name = 'collection_test'
    query_vector = get_embeddings(query)
    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=2,
        output_fields=["my_id", "my_content"],
        search_params={"metric_type": "COSINE"}
    )
    return json.dumps(res, ensure_ascii=False)


TOOLS: List[Callable[..., Any]] = [multiply, milvus_search]
