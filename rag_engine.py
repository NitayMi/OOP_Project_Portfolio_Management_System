import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# הגדרת מודל Embedding (המרת טקסט למספרים)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # מודל מהיר, מתאים למחשב שלך

# יצירת מאגר Chroma
client = chromadb.Client()
collection = client.get_or_create_collection("investment_knowledge")

# פונקציה ליצירת embedding
def embed_text(text):
    return embedding_model.encode([text])[0].tolist()

# פונקציה לטעינת מידע לקולקציה (vector DB)
def load_data(text_list):
    for idx, text in enumerate(text_list):
        collection.add(
            documents=[text],
            ids=[str(idx)],
            embeddings=[embed_text(text)]
        )
    print("✅ Knowledge base loaded successfully.")

# פונקציה לחיפוש תשובה
def query(question, top_k=1):
    question_embedding = embed_text(question)
    results = collection.query(query_embeddings=[question_embedding], n_results=top_k)
    if results['documents']:
        return results['documents'][0][0]  # מחזיר את התוצאה הכי דומה
    return "❌ No relevant information found."

# דוגמה לשימוש (רק אם מריצים את הקובץ ישירות)
if __name__ == "__main__":
    # טעינת ידע ראשוני
    knowledge = [
        "A stock is a security that represents partial ownership in a company.",
        "A bond is a security that represents a debt obligation from the issuer to the holder.",
        "High risk is suitable for investors willing to take significant risks for higher returns.",
        "Diversifying investments helps reduce the overall portfolio risk."
    ]
    load_data(knowledge)

    # בדיקה עם שאלה
    question = "What is a stock?"
    answer = query(question)
    print(f"\n❓ Question: {question}\n💡 Answer: {answer}")
