from view import view
from controller import controller, ControllerV2
from dbmodel import SqliteRepository
from ollamamodel import AIAdvisorRAG  # ה-AI החדש שלך

USE_NEW_CONTROLLER = True  # בחירה בין הישן לחדש

def main():
    ai = AIAdvisorRAG()  # זה ייטען רק פעם אחת
    screen = view(ai_advisor=ai)  # נעביר אותו ל-view
    screen.show()

# def main():
#     db = SqliteRepository()
#     ai = AIAdvisorRAG()  # AI החדש עם RAG

#     # שים לב: לא קובע סיכון, רק מגדיר את המנועים
#     if USE_NEW_CONTROLLER:
#         c = ControllerV2(risk_level=None, db_repo=db, ai_advisor=ai)  # risk_level=none כי view יגדיר
#     else:
#         c = controller(None)  # גם הישן

#     screen = view()
#     screen.show()  # שם מנהלים הכל

if __name__ == "__main__":
    main()








# def main():
#     screen= view()
#     screen.show()



# if __name__ == "__main__":
#     main()



# לא לשכוח לבצע את כל ההתקנות שנדרשות לפני הרצת הקוד
# pip install -r requirements.txt

# To generate the requirements.txt file, use the following command:
# pip freeze > requirements.txt