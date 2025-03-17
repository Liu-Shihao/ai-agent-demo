from langchain_core.tools import tool
from pymilvus import MilvusClient

from agent.embedding_utils import get_embeddings

client = MilvusClient("data/milvus_demo.db")


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    result = a * b
    return result


@tool
def milvus_search(query: str) -> list[list[dict]]:
    """Search milvus for the query."""
    collection_name = 'collection_test'
    query_vector = get_embeddings(query)
    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=2,
        output_fields=["my_id", "my_content"],
        search_params={"metric_type": "COSINE"}
    )
    return res
