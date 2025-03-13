
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


# קוד חדש 12.03.25
import sqlite3

class dbmodel:
    def __init__(self):
        print("DB connect")
        self.conn = sqlite3.connect('investments.db')
        self.cursor = self.conn.cursor()
        self.create_table()


# למחוק אחרי זה ============================================
    def create_investments_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS investments;')  # מוחק טבלה ישנה (אם קיימת)
        self.cursor.execute('''
            CREATE TABLE investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                basevalue REAL NOT NULL,
                ammont REAL NOT NULL,
                sector TEXT NOT NULL,
                variance TEXT NOT NULL,
                type TEXT NOT NULL,
                subtype TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        print("✅ 'investments' table created successfully!")
# למחוק עד פה ============================================



    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            basevalue REAL NOT NULL,
            ammont INTEGER NOT NULL,
            sector TEXT NOT NULL,
            variance TEXT NOT NULL,
            type TEXT NOT NULL,
            subtype TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def insert(self, name, basevalue, ammont, sector, variance, type_, subtype):
        existing = self.find_security(name, type_, sector, subtype)
        if existing:
            self.cursor.execute('''
                UPDATE investments
                SET ammont = ammont + ?
                WHERE id = ?
            ''', (ammont, existing['id']))
        else:
            self.cursor.execute('''
                INSERT INTO investments (name, basevalue, ammont, sector, variance, type, subtype)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, basevalue, ammont, sector, variance, type_, subtype))
        self.conn.commit()

    def sell(self, name, amount):
        self.cursor.execute('SELECT * FROM investments WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        if row:
            if row[3] > amount:  # row[3] is 'ammont'
                self.cursor.execute('UPDATE investments SET ammont = ammont - ? WHERE name = ?', (amount, name))
            else:
                self.cursor.execute('DELETE FROM investments WHERE name = ?', (name,))
            self.conn.commit()

    def find_security(self, name, type_, sector, subtype):
        self.cursor.execute('''
        SELECT * FROM investments
        WHERE name=? AND type=? AND sector=? AND subtype=?
        ''', (name, type_, sector, subtype))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'basevalue': row[2],
                'ammont': row[3],
                'sector': row[4],
                'variance': row[5],
                'type': row[6],
                'subtype': row[7]
            }
        return None

    def getdata(self):
        self.cursor.execute('SELECT * FROM investments')
        rows = self.cursor.fetchall()
        data = {}
        for idx, row in enumerate(rows):
            data[idx] = {
                'id': row[0],
                'name': row[1],
                'basevalue': row[2],
                'ammont': row[3],
                'sector': row[4],
                'variance': row[5],
                'type': row[6],
                'subtype': row[7]
            }
        return data

    def clear_portfolio(self):
        self.cursor.execute('DELETE FROM investments')
        self.conn.commit()

    def get_available_securities(self):
        self.cursor.execute('SELECT * FROM available_securities')
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def insert_or_update(self, name, sector, variance, security_type, subtype, basevalue, amount):
        # קודם בודקים אם נייר הערך כבר קיים
        self.cursor.execute('''
            SELECT id, ammont FROM investments
            WHERE name = ? AND type = ? AND sector = ? AND subtype = ?
        ''', (name, security_type, sector, subtype))
        result = self.cursor.fetchone()

        if result:
            # אם קיים - מעדכנים כמות
            current_amount = result[1]
            new_amount = current_amount + amount
            self.cursor.execute('''
                UPDATE investments
                SET ammont = ?
                WHERE id = ?
            ''', (new_amount, result[0]))
            print(f"Updated {name}: New amount {new_amount}")
        else:
            # אם לא קיים - מכניסים חדש
            self.cursor.execute('''
                INSERT INTO investments (name, basevalue, ammont, sector, variance, type, subtype)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, basevalue, amount, sector, variance, security_type, subtype))
            print(f"Inserted new security: {name} with amount {amount}")

        # שמירה
        self.conn.commit()
