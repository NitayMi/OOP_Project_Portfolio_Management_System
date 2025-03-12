
# import sqlite3
# import matplotlib.pyplot as plt


# class dbmodel():
    
#  def __init__(self):
#     print("DB connect")
#     self.conn = sqlite3.connect('investments.db')
#     self.cursor = self.conn.cursor()
#     self.cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='investments';''')
#     if not self.cursor.fetchone():
#         self.cursor.execute('''
#             CREATE TABLE investments (
#                 id INTEGER PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 basevalue REAL NOT NULL,
#                 ammont REAL NOT NULL
#             )
#         ''')
#         self.conn.commit()
     
#  def insert(self,whatsecurity,ammout):   
     
#     #צריך לבדוק האם אחרי קניית המניה רמת הסיכון בתיק מתחת לסף
#     # פה נכנסת לפעולה הלוגיקה במודל הסיכונים
#     #בשלב ראשון הייתי מוסיף חוקים פשוטים יחסית ורק אחרי שהכל עובד טכנית
#     #מוודא שהחוקים כתובים נכון 
#     #סדרה של IF's ...
#     self.cursor.execute('''
#         INSERT INTO investments (name, basevalue, ammont)
#         VALUES (?, ?, ?)
#     ''', ("tesla", 360, 640))
#     self.conn.commit()
#     print("Inserting...")      



#  def getdata(self):
#     self.cursor.execute('SELECT * FROM investments')
#     rows = self.cursor.fetchall()
#     columns = [column[0] for column in self.cursor.description]
#     dictanswer = {row[0]: dict(zip(columns, row)) for row in rows}
   
#     return dictanswer


# קוד חדש שלי
import sqlite3
import matplotlib.pyplot as plt

class dbmodel():
    
    def __init__(self):
        print("DB connect")
        self.conn = sqlite3.connect('investments.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='investments';''')
        if not self.cursor.fetchone():
            self.cursor.execute('''
                CREATE TABLE investments (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    basevalue REAL NOT NULL,
                    ammont REAL NOT NULL
                )
            ''')
            self.conn.commit()
     
    def insert(self, whatsecurity, ammount, basevalue=360):  # נוסיף basevalue כברירת מחדל, אבל ניתן לשנות
        # במקום להכניס תמיד "tesla", מכניסים מה שבאמת רוצים
        self.cursor.execute('''
            INSERT INTO investments (name, basevalue, ammont)
            VALUES (?, ?, ?)
        ''', (whatsecurity, basevalue, ammount))
        self.conn.commit()
        print(f"Inserting {whatsecurity} with amount {ammount} and base value {basevalue}...")      

    def delete(self, name):  # פונקציה למחיקה לפי שם
        self.cursor.execute('DELETE FROM investments WHERE name = ?', (name,))
        self.conn.commit()
        print(f"Deleted {name} from investments.")

    def getdata(self):
        self.cursor.execute('SELECT * FROM investments')
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        dictanswer = {row[0]: dict(zip(columns, row)) for row in rows}
        return dictanswer

    def get_available_securities(self):
        self.cursor.execute('SELECT * FROM available_securities')
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return result
