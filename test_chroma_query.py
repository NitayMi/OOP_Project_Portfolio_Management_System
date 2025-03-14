from chromadb.utils import embedding_functions
from chromadb import PersistentClient

persist_directory = "db"
client = PersistentClient(path=persist_directory)
collection = client.get_or_create_collection(name="my_collection")

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

query = "What is a class in Python?"  # Change to the question you want
query_embedding = embedding_func(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    include=["documents"]
)

print("Search results:")
for doc in results['documents'][0]:
    print(doc)
