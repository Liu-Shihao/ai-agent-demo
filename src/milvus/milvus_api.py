import sys
import os
import atexit
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pymilvus import MilvusClient, DataType

from src.milvus.ollama_embedding import get_embeddings

client = MilvusClient("./data/milvus_demo.db")

# Register cleanup function
def cleanup():
    try:
        client.close()
    except Exception as e:
        print(f"Error during cleanup: {e}")

atexit.register(cleanup)


def collection_list():
    res = client.list_collections()
    print(res)


def create_collection_test(collection_name: str):
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )

    schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=768)
    schema.add_field(field_name="my_content", datatype=DataType.VARCHAR, max_length=65535)

    index_params = client.prepare_index_params()

    index_params.add_index(
        field_name="my_vector",
        index_type="AUTOINDEX",
        metric_type="COSINE"
    )

    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params
    )

    res = client.get_load_state(
        collection_name=collection_name
    )

    print(res)


def drop_collection(collection_name: str):
    client.drop_collection(
        collection_name=collection_name
    )


def insert_data(id: int, data: str, collection_name: str):
    vector = get_embeddings(data)
    data = [
        {
            'my_id': id,
            'my_vector': vector,
            'my_content': data
        }
    ]
    res = client.insert(
        collection_name=collection_name,
        data=data
    )
    print(res)


def search_data(query: str, collection_name: str):
    query_vector = get_embeddings(query)
    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=2,
        output_fields=["my_id", "my_content"],
        search_params={"metric_type": "COSINE"}
    )
    print(f"search: {res}")


if __name__ == "__main__":
    try:
        # collection_list()
        collection_name = 'collection_test'
        # create_collection_test(collection_name)
        # collection_list()
        print(client.has_collection(collection_name))
        # print(client.describe_collection(collection_name))
        
        # insert_data(2, 'hello', collection_name)
        search_data('hi', collection_name)
    finally:
        cleanup()
        atexit.unregister(cleanup)
