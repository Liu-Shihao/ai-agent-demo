import uuid

from pymilvus import MilvusClient

from milvus.ollama_embedding import get_embeddings

client = MilvusClient("./data/milvus_demo.db")


def generate_unique_id():
    """生成唯一ID的几种方式"""
    # 方式1：使用时间戳（毫秒）
    # timestamp_id = int(time.time() * 1000)

    # 方式2：使用UUID的整数表示
    uuid_int = uuid.uuid4().int & (1 << 63) - 1  # 确保ID在64位范围内

    # 方式3：使用递增ID（需要自己维护计数器，比如使用Redis或数据库）
    # counter = get_next_counter()  # 实现获取下一个计数器的逻辑

    return uuid_int  # 这里使用时间戳方式


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


def read_file_content(file_path: str) -> str:
    """读取整个文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == "__main__":
    # print(generate_unique_id())
    collection_name = 'collection_test'
    file_path = './data/example.txt'
    # content = read_file_content(file_path)
    # print(content)
    # insert_data(generate_unique_id(), content, collection_name)

    query_vector = get_embeddings("what's the Oscar Zoom?")
    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=2,
        output_fields=["my_id", "my_content"],
        search_params={"metric_type": "COSINE"}
    )
    for hits in res:
        for hit in hits:
            print(hit)
