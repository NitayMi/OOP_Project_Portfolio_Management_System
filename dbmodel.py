import os
import sqlite3
from abc import ABC, abstractmethod

class SecurityData:
    def __init__(self, id, name, basevalue, ammont, sector, variance, security_type, subtype='N/A'):
        self.id = id
        self.name = name
        self.basevalue = basevalue
        self.ammont = ammont
        self.sector = sector
        self.variance = variance
        self.security_type = security_type
        self.subtype = subtype

    def __str__(self):
        return f"{self.name} ({self.security_type}) - {self.ammont} units @ {self.basevalue}"

class IDataRepository(ABC):
    @abstractmethod
    def get_portfolio_data(self):
        pass

    @abstractmethod
    def get_available_securities(self):
        pass

    @abstractmethod
    def insert_or_update(self, name, sector, variance, security_type, subtype, basevalue, amount):
        pass

    @abstractmethod
    def sell(self, name, amount):
        pass

    @abstractmethod
    def clear_portfolio(self):
        pass

class dbmodel:
    _instance = None  # מחלקת Singleton להבטחת חיבור יחיד למסד הנתונים

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(dbmodel, cls).__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        print("DB connect")
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'investments.db')
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)  # מאפשר גישה ממספר תהליכים
        self.cursor = self.conn.cursor()
        self.create_table()

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
        return SecurityData(*row) if row else None

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
        self.cursor.execute("SELECT * FROM available_securities")
        rows = self.cursor.fetchall()
        return [
            SecurityData(
                row[0],  # id
                row[1],  # name
                row[6],  # basevalue (תמיד בעמודה 6)
                0,       # ammont (זמין לקנייה, לא בבעלות)
                row[2],  # sector
                row[3],  # variance
                row[4],  # security_type (type)
                row[5]   # subtype
            ) for row in rows
        ]

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

    def get_portfolio_data(self):
        """
        Retrieves the current portfolio from the database in a thread-safe manner.
        Uses the correct database path to avoid creating a duplicate DB file.
        """
        try:
            self.cursor.execute("SELECT * FROM investments")
            rows = self.cursor.fetchall()
            return [SecurityData(*row) for row in rows] if rows else []
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            return []


class SqliteRepository(IDataRepository):
    def __init__(self):
        self.db = dbmodel()

    def get_portfolio_data(self):
        return self.db.get_portfolio_data()

    def get_available_securities(self):
        return self.db.get_available_securities()

    def insert_or_update(self, name, sector, variance, security_type, subtype, basevalue, amount):
        return self.db.insert_or_update(name, sector, variance, security_type, subtype, basevalue, amount)

    def sell(self, name, amount):
        return self.db.sell(name, amount)

    def clear_portfolio(self):
        return self.db.clear_portfolio()
    