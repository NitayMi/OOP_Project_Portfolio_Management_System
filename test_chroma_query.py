from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# 1. Load the existing database
persist_directory = 'db'  # same path used in rag_loader.py
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# 2. Check how many documents are in the database
print("Number of documents in the database:", vectordb._collection.count())

# 3. Test - search for a sample question
query = "What is a class in object-oriented programming?"
results = vectordb.similarity_search(query, k=3)

# 4. Print the results
print("\nSearch results:")
for i, res in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(res.page_content)
