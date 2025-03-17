import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# הגדרת מודל Embedding (המרת טקסט למספרים)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # מודל מהיר, מתאים למחשב שלך

# יצירת מאגר Chroma
persist_directory = "db"  # לוודא שזה תואם למה שיש ב-loader
client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_or_create_collection(name="my_collection")


# פונקציה ליצירת embedding
def embed_text(text):
    return embedding_model.encode([text])[0].tolist()

def query(question, top_k=3):
    """
    Query the RAG knowledge base and return the most relevant document.

    :param question: The user's question.
    :param top_k: Number of top results to retrieve.
    :return: The most relevant document text or a default message if no result found.
    """
    results = collection.query(query_texts=[question], n_results=top_k)

    # בדיקה אם קיימות תוצאות אמיתיות
    if results and 'documents' in results and results['documents']:
        first_doc_list = results['documents'][0]  # לוקח את הרשימה הראשונה של התשובות
        if first_doc_list:  # אם הרשימה לא ריקה
            return first_doc_list[0]  # מחזיר את התוצאה הראשונה
    # אם אין תוצאה רלוונטית
    return "No relevant background knowledge found."
