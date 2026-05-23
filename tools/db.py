import chromadb
from chromadb.utils import embedding_functions

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-large-en-v1.5"
)


client = chromadb.PersistentClient(path="../data/chromadb")

def create_collection(name):

    return client.create_collection(
        name,
        embedding_function=embedding_func)


def get_collection(name):
    return client.get_collection(name)

def push_data(collection, data):
    collection.add(data)


def query_collection(collection, query, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results