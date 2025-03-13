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
        "מניה היא נייר ערך שמייצג בעלות חלקית בחברה.",
        "אג\"ח הוא נייר ערך המהווה התחייבות חוב מצד המנפיק כלפי המחזיק.",
        "רמת סיכון גבוהה מתאימה למשקיעים שמוכנים לקחת סיכונים משמעותיים תמורת תשואות גבוהות.",
        "פיזור השקעות עוזר להקטין את הסיכון הכולל של התיק."
    ]
    load_data(knowledge)
    
    # בדיקה עם שאלה
    question = "מה זה מניה?"
    answer = query(question)
    print(f"\n❓ Question: {question}\n💡 Answer: {answer}")
