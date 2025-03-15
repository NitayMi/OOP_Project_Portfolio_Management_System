import sqlite3

# חיבור למסד הנתונים
conn = sqlite3.connect('investments.db')
cursor = conn.cursor()

# מחיקת הטבלה אם קיימת כדי שלא יהיו כפילויות
cursor.execute('DROP TABLE IF EXISTS available_securities;')

# יצירת הטבלה לפי המודל שסיכמנו
cursor.execute('''
CREATE TABLE IF NOT EXISTS available_securities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sector TEXT NOT NULL,
    variance TEXT NOT NULL,
    type TEXT NOT NULL,      -- stock / bond
    subtype TEXT NOT NULL,  -- common / preferred / government / corporate
    basevalue REAL NOT NULL  -- מחיר בסיס
)
''')

# הכנסת 10 ניירות ערך לדוגמה עם מחיר
securities = [
    ('Apple', 'Technology', 'High', 'stock', 'common', 360),
    ('Google', 'Technology', 'High', 'stock', 'preferred', 280),
    ('Teva', 'Health', 'Low', 'stock', 'common', 100),
    ('BankLeumi', 'Finance', 'Low', 'stock', 'preferred', 85),
    ('AzrieliGroup', 'Real Estate', 'Low', 'stock', 'common', 200),
    ('GovBond', 'Industry', 'Low', 'bond', 'government', 150),
    ('CorpBondRealty', 'Real Estate', 'High', 'bond', 'corporate', 110),
    ('CorpBondTech', 'Technology', 'High', 'bond', 'corporate', 130),
    ('GovBondEnergy', 'Energy', 'Low', 'bond', 'government', 180),
    ('CorpBondFinance', 'Finance', 'High', 'bond', 'corporate', 95)
]

# הכנסת הנתונים לטבלה
cursor.executemany('''
INSERT INTO available_securities (name, sector, variance, type, subtype, basevalue)
VALUES (?, ?, ?, ?, ?, ?)
''', securities)

# סגירת החיבור עם הודעה
conn.commit()
print("✅ Table 'available_securities' created and 10 securities inserted successfully!")
conn.close()
