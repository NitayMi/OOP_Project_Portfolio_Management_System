# Description: קובץ זה מטפל בטעינת טקסט מקובץ PDF או Word והוספתו למסד הנתונים של ChromaDB
import os
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from docx import Document  # לטיפול ב-Word
import logging

logging.getLogger("chromadb.segment.impl.vector.local_persistent_hnsw").setLevel(logging.ERROR)

# _persist_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
_persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "db"))
_client = chromadb.PersistentClient(path=_persist_directory)
_collection = _client.get_or_create_collection(name="my_collection")  # נטען רק פעם אחת!

def add_texts_to_chromadb(texts):
    """
    הוספת טקסטים למאגר ChromaDB, רק אם הם עדיין לא קיימים
    """
    existing_ids = set(_collection.get()["ids"])  # שליפת ה-IDs שכבר קיימים

    new_data = []
    for idx, text in enumerate(texts):
        text_id = str(idx)  # מזהה ייחודי לכל טקסט

        if text_id not in existing_ids:  # בדיקה אם כבר קיים
            new_data.append({"id": text_id, "text": text})

    if new_data:
        _collection.add(
            ids=[item["id"] for item in new_data],
            documents=[item["text"] for item in new_data]
        )
        print(f"✅ Added {len(new_data)} new texts to ChromaDB.")
    else:
        print("🔍 No new texts to add. Skipping insert.")


def get_collection():
    print("✅ Fetching ChromaDB Collection (No reload expected)")
    return _collection  # מחזיר את אותה Collection כל הזמן!


















# persist_directory = "db"  # שים לב! צריך להיות תואם למה שאתה משתמש בקובץ הבדיקה
# client = chromadb.PersistentClient(path=persist_directory)
# collection = client.get_or_create_collection(name="my_collection")

# def get_collection():
#     return collection





# # בדיקה האם כבר קיימים נתונים במאגר
# if len(collection.get()['ids']) > 0:
#     print("✅ Knowledge base already loaded. Skipping reload.")
#     exit()  # יציאה מהסקריפט כדי לא להעמיס כפול

# # הגדרת Embedding (תעדכן לפי הצורך)
# embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# # פונקציה לקרוא PDF
# def load_pdf_text(file_path):
#     reader = PdfReader(file_path)
#     full_text = ""
#     for page in reader.pages:
#         text = page.extract_text()
#         if text:
#             full_text += text + "\n"
#     return full_text

# # פונקציה לקרוא Word
# def load_word_text(file_path):
#     doc = Document(file_path)
#     full_text = ""
#     for para in doc.paragraphs:
#         full_text += para.text + "\n"
#     return full_text

# # טען את הטקסט לפי סוג הקובץ
# file_path = "Module1.pdf"  # כאן תשנה לנתיב הקובץ שלך
# if file_path.endswith(".pdf"):
#     full_text = load_pdf_text(file_path)
# elif file_path.endswith(".docx"):
#     full_text = load_word_text(file_path)
# else:
#     raise ValueError("Unsupported file type. Please use PDF or Word (.docx)")

# # פיצול הטקסט לחלקים קטנים
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len
# )
# knowledge_texts = text_splitter.split_text(full_text)

# print(f"Number of chunks created: {len(knowledge_texts)}")  # בדיקה

# # הוספת הטקסטים והוקטורים ל-ChromaDB
# for idx, text in enumerate(knowledge_texts):
#     embedding = embedding_func(text)  # מחזיר embedding רגיל
#     if isinstance(embedding, list):  # אם קיבלנו רשימה (כדי לא להכניס רשימת רשימות)
#         embedding = embedding[0]
#     collection.add(
#         documents=[text],
#         ids=[str(idx)],
#         embeddings=[embedding]  # רק וקטור אחד
#     )

# print("Successfully added texts to Chroma!")
# print("You can now use the ChromaDB for similarity search.")

