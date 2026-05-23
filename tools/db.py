import chromadb,uuid
from chromadb.utils import embedding_functions
from config import DB_DIR

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2",
    device="cuda"
)


client = chromadb.PersistentClient(path=DB_DIR)

def create_collection(name):

    return client.create_collection(
        name,
        embedding_function=embedding_func)


def get_collection(name):
    return client.get_collection(name)

def push_data(collection, data):

    collection.add(
        ids=[str(uuid.uuid4()) for _ in data],
        documents=[doc.page_content for doc in data],
        metadatas=[doc.metadata for doc in data]
    )


def query_collection(collection, query, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def clear_data(collection):

    all_ids = collection.get()["ids"]
    if len(all_ids) == 0:
        return

    collection.delete(ids=all_ids)