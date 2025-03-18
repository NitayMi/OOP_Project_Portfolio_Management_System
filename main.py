from view import view

def main():
    screen = view()
    screen.show()

if __name__ == "__main__":
    main()



# לא לשכוח לבצע את כל ההתקנות שנדרשות לפני הרצת הקוד
# pip install -r requirements.txt

# To generate the requirements.txt file, use the following command:
# pip freeze > requirements.txt














# בדיקות מהירות לפני הרצת הקוד
# import time
# import sys
# import os

# # התחלת מדידת זמן
# start_time = time.time()

# print("🔍 Starting main.py...")

# def log_time(section):
#     """ מדפיס את זמן ההרצה של כל שלב ב-main """
#     print(f"✅ {section} loaded in {time.time() - start_time:.2f} seconds")

# # טעינת מודולים חשובים
# log_time("Initializing")

# try:
#     sys.path.append(os.path.dirname(__file__))  # הוספת נתיב התיקייה הראשית
#     import advisor_ai  # ודא שזהו שם הקובץ הנכון!
#     log_time("advisor_ai imported")
# except ImportError as e:
#     print(f"❌ Failed to import advisor_ai: {e}")


# try:
#     import dbmodel
#     log_time("dbmodel imported")
# except ImportError:
#     print("❌ Failed to import dbmodel")

# try:
#     import controller
#     log_time("controller imported")
# except ImportError:
#     print("❌ Failed to import controller")

# try:
#     import view
#     log_time("view imported")
# except ImportError:
#     print("❌ Failed to import view")

# try:
#     import rag_loader
#     log_time("rag_loader imported")
# except ImportError:
#     print("❌ Failed to import rag_loader")

# try:
#     import rag_engine
#     log_time("rag_engine imported")
# except ImportError:
#     print("❌ Failed to import rag_engine")

# # טעינת AI רק אם נדרש
# AI_ENABLED = False  # טוען את ה-AI רק בעת קריאה מפורשת
# ai_instance = None

# def load_ai():
#     global ai_instance, AI_ENABLED
#     if not AI_ENABLED:
#         print("⏳ Initializing AI...")
#         ai_instance = ai_advisor.AIAdvisorRAG()
#         AI_ENABLED = True
#         log_time("AI Initialized")

# # פונקציה להרצת הממשק הראשי
# def main():
#     screen = view.view()
#     screen.show()
# if __name__ == "__main__":
#     main()
#     print("📋 Running main application...")
#     log_time("Main application started")
#     screen = view.view()
#     screen.show()
#     print("✅ Main.py fully loaded.")
    