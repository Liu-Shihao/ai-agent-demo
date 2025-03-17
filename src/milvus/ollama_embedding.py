from langchain_ollama import OllamaEmbeddings

"""
pip install -qU langchain-ollama
"""


def get_embeddings(text: str):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return (embeddings.embed_query(text))


if __name__ == "__main__":
    embeddings = get_embeddings("Hello, world!")
    print(embeddings)
    print(len(embeddings))
    # 768
