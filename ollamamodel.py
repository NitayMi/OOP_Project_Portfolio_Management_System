from abc import ABC, abstractmethod
import ollama
from rag_engine import query
from rag_loader import get_collection  # טעינת הקולקשן תתבצע רק כשצריך

# # ==== ממשק כללי לכל AI Advisor (חובה) ====
# class IAIAdvisor(ABC):
#     @abstractmethod
#     def get_advice(self, question: str, portfolio_data=None) -> str:
#         """
#         מתודה לקבלת ייעוץ AI. חובה לממש בכל מחלקה שמיישמת את הממשק.
#         """
#         pass

# # ==== מחלקה שמיישמת RAG AI עם שאילתות וניתוח תיק השקעות ====
# class AIAdvisorRAG(IAIAdvisor):
#     def __init__(self, model='deepseek-r1:7b', collection=None):
#         """
#         :param model: שם המודל לשימוש ב-ollama.
#         :param collection: חיבור ל-ChromaDB (מוזרק מ-main).
#         """
#         self.model = model
#         self.collection = collection  # עובר מבחוץ, לא נוצר פנימי!

#     def get_advice(self, question: str, portfolio_data=None) -> str:
#         """
#         מחזיר ייעוץ מבוסס AI בהתבסס על שאלה ותיק ההשקעות.
#         :param question: שאלת המשתמש.
#         :param portfolio_data: פרטי התיק של המשתמש.
#         :return: מחרוזת תשובה.
#         """
#         print("🔍 Getting AI advice with RAG and personalized portfolio context...")

#         # בניית קונטקסט של התיק
#         portfolio_context = ""
#         if portfolio_data:
#             portfolio_context = "\n".join([
#                 f"- {item.name}, {item.security_type}, Sector: {item.sector}, "
#                 f"Risk: {item.variance}, Amount: {item.ammont}"
#                 for item in portfolio_data
#             ])

#         # שליפת מידע תומך מה-RAG
#         if self.collection is None:
#             raise ValueError("Collection must be provided!")
#         rag_context = query(question=question, collection=self.collection, top_k=3)


#         # בניית השאלה המלאה עם הקשר
#         full_question = f"""
# You are a professional investment advisor AI.

# User's Risk Profile and Portfolio:
# {portfolio_context}

# Relevant Background Knowledge:
# {rag_context}

# Question:
# {question}

# Provide a professional and personalized investment recommendation.
# """

#         # שליחת השאלה למודל
#         response = ollama.generate(
#             model=self.model,
#             prompt=full_question
#         )
#         return response.get('response', '❌ No valid response')









class IAIAdvisor(ABC):
    @abstractmethod
    def get_advice(self, question: str, portfolio_data=None) -> str:
        pass

class AIAdvisorRAG(IAIAdvisor):
    def __init__(self, model='deepseek-r1:7b'):
        """
        :param model: שם המודל לשימוש ב-ollama.
        """
        self.model = model
        self.collection = None  # הקולקשן לא נטען עדיין!

    def ensure_collection_loaded(self):
        """ טוען את ChromaDB רק אם עדיין לא נטען """
        if not hasattr(self, "collection_loaded") or not self.collection_loaded:
            print("⏳ Loading AI Collection...")
            self.collection = get_collection()
            self.collection_loaded = True  # מבטיח טעינה פעם אחת בלבד
            print("✅ AI Collection Loaded!")


    def get_advice(self, question: str, portfolio_data=None) -> str:
        """ מחזיר ייעוץ מבוסס AI בהתבסס על שאלה ותיק ההשקעות """
        if not hasattr(self, "collection_loaded") or not self.collection_loaded:
            self.ensure_collection_loaded()
            self.collection_loaded = True  # מסמן שהקולקשן כבר נטען


        print("🔍 Getting AI advice with RAG and personalized portfolio context...")
        
        # יצירת קונטקסט תיק השקעות
        portfolio_context = ""
        if portfolio_data:
            portfolio_context = "\n".join([
                f"- {item.name}, {item.security_type}, Sector: {item.sector}, "
                f"Risk: {item.variance}, Amount: {item.ammont}"
                for item in portfolio_data
            ])

        # שליפת מידע תומך מה-RAG
        rag_context = query(question=question, collection=self.collection, top_k=3)

        # בניית השאלה המלאה עם ההקשר
        full_question = f"""
You are a professional investment advisor AI. 
Provide a short and actionable investment recommendation in **2-3 sentences** only. Avoid long explanations.

User's Risk Profile and Portfolio:
{portfolio_context}

Relevant Background Knowledge:
{rag_context}

Question:
{question}

Provide a professional and personalized investment recommendation.
"""

        response = ollama.generate(
            model=self.model,
            prompt=full_question
        )

        # בדיקה האם התשובה נחתכת
        full_response = response.get('response', '')
        if not full_response:
            return "❌ No valid response"

        print(f"🔍 Full AI Response: {full_response}")  # Debugging print
        return full_response


        # # שליחת השאלה למודל
        # response = ollama.generate(
        #     model=self.model,
        #     prompt=full_question
        # )
        # return response.get('response', '❌ No valid response')
