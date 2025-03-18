from sentence_transformers import SentenceTransformer

# פונקציה ליצירת embedding
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # זה בסדר שישאר כי זה רק הפונקציה

def embed_text(text):
    return embedding_model.encode([text])[0].tolist()

def query(question: str, collection, top_k: int = 3):
    """
    Query the RAG knowledge base and return the most relevant document.

    :param collection: The Chroma collection to search.
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
