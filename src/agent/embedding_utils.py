from langchain_ollama import OllamaEmbeddings

"""
pip install -qU langchain-ollama
"""


def get_embeddings(text: str):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings.embed_query(text)
