# Description: קובץ זה מטפל בטעינת טקסט מקובץ PDF או Word והוספתו למסד הנתונים של ChromaDB

import os
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from docx import Document  # לטיפול ב-Word

# הגדרת Chroma
client = chromadb.PersistentClient(path="my_chroma_db")
collection = client.get_or_create_collection(name="my_collection")

# הגדרת Embedding (תעדכן פה למה שאתה באמת משתמש - לדוג' Instructor או SentenceTransformer)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# פונקציה לקרוא PDF
def load_pdf_text(file_path):
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return full_text

# פונקציה לקרוא Word
def load_word_text(file_path):
    doc = Document(file_path)
    full_text = ""
    for para in doc.paragraphs:
        full_text += para.text + "\n"
    return full_text

# טען את הטקסט לפי סוג הקובץ
file_path = "Module1.pdf"  # כאן תשנה לנתיב הקובץ שלך
if file_path.endswith(".pdf"):
    full_text = load_pdf_text(file_path)
elif file_path.endswith(".docx"):
    full_text = load_word_text(file_path)
else:
    raise ValueError("Unsupported file type. Please use PDF or Word (.docx)")

# פיצול הטקסט לחלקים קטנים
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
knowledge_texts = text_splitter.split_text(full_text)

# הוספת הטקסטים והוקטורים ל-ChromaDB
for idx, text in enumerate(knowledge_texts):
    embedding = embedding_func(text)  # מחזיר embedding רגיל
    if isinstance(embedding, list):  # אם קיבלנו רשימה (כדי לא להכניס רשימת רשימות)
        embedding = embedding[0]
    collection.add(
        documents=[text],
        ids=[str(idx)],
        embeddings=[embedding]  # רק וקטור אחד
    )

print("Successfully added texts to Chroma!")
