from dbmodel import dbmodel, SecurityData, IDataRepository
from ollamamodel import IAIAdvisor, ollamamodel
from securitiesmodel import Stock, Bond, Portfolio
from enum import Enum

# class SecurityType(Enum):
#     STOCK = 'stock'
#     BOND = 'bond'

# class controller:
#     def __init__(self, risk_level: str):
#         self.dbmodel = dbmodel()  # Database model
#         self.portfolio = Portfolio(self.dbmodel)  # Portfolio instance linked to DB
#         self.ollamamodel = ollamamodel()  # AI Advisor
#         self.risk_level = risk_level  # Risk preference

#     def get_available_securities(self):
#         return self.dbmodel.get_available_securities()

#     def buy(self, name, sector, variance, security_type, subtype, amount, basevalue):
#         # מבצע קניית נייר ערך, כולל בדיקת סיכון והתאמה לרמת הסיכון של התיק.

#         # יצירת אובייקט SecurityData
#         security_data = SecurityData(
#             id=None,
#             name=name,
#             basevalue=basevalue,
#             ammont=amount,
#             sector=sector,
#             variance=variance,
#             security_type=security_type,
#             subtype=subtype
#         )

#         # חישוב סיכון נוכחי
#         current_risk = self.portfolio.calculate_total_risk()
#         # חישוב סיכון חזוי כולל הנייר החדש
#         projected_risk = self.portfolio.calculate_projected_risk_with_new_security(security_data, amount)

#         # ✅ הצגת סיכון למשתמש
#         print(f"\n🧮 Current portfolio risk: {current_risk:.2f}")
#         print(f"📈 Projected portfolio risk after purchase: {projected_risk:.2f}")

#         # חישוב טווח רמת סיכון
#         min_risk, max_risk = self._get_risk_range_for_level()

#         # ✅ לוגיקה נכונה:
#         # 1. אם התיק חורג כבר מהמקסימום — נאפשר רק קנייה שמקטינה או לא מחמירה.
#         if current_risk > max_risk:
#             if projected_risk > current_risk:
#                 return False, f"⚠️ Cannot buy '{name}'. Portfolio already exceeds risk limit ({current_risk:.2f}), and this purchase would increase it to {projected_risk:.2f}."
#             # אחרת (מוריד סיכון) - נאשר
#         else:
#             # 2. אם התיק עומד בדרישות — נאפשר קנייה אם היא נשארת בטווח.
#             if not (min_risk <= projected_risk <= max_risk):
#                 return False, f"⚠️ Cannot buy '{name}'. Total projected risk {projected_risk:.2f} exceeds acceptable range for '{self.risk_level}' risk level."

#         # ✅ הכנסת הקנייה למסד הנתונים
#         self.dbmodel.insert_or_update(name, sector, variance, security_type, subtype, basevalue, amount)

#         return True, f"✅ '{name}' bought successfully! Total portfolio risk: {projected_risk:.2f}"

#     def sell(self, name, security_type, sector, subtype, amount):
#         # מבצע מכירת נייר ערך, כולל בדיקת כמות קיימת.

#         # שליפת התיק הקיים
#         portfolio = self.dbmodel.get_portfolio_data()

#         # חיפוש נייר הערך לפי פרמטרים
#         security = next(
#             (s for s in portfolio if s.name == name and s.security_type == security_type and s.sector == sector and s.subtype == subtype),
#             None
#         )

#         if not security:
#             return False, f"❌ Security '{name}' not found in portfolio."

#         # בדיקת כמות מספקת למכירה
#         if security.ammont < amount:
#             return False, f"❌ Not enough units to sell. You own {security.ammont} units."

#         # ביצוע המכירה
#         self.dbmodel.sell(name, amount)

#         # חישוב סיכון לאחר מכירה
#         updated_risk = self.portfolio.calculate_total_risk()

#         # החזרת הודעת הצלחה
#         return True, f"✅ '{name}' sold successfully! Total portfolio risk after sale: {updated_risk:.2f}"


#     def get_portfolio_data(self):
#         return self.dbmodel.get_portfolio_data()

#     def get_total_risk(self):
#         return self.portfolio.calculate_total_risk()
 
#     def _calculate_risk_with_new_security(self, security, amount):
#         current_risk = self.portfolio.calculate_total_risk()
#         current_amount = sum(sec['ammont'] for sec in self.dbmodel.getdata().values())
#         security_risk = security.calculate_risk()

#         total_risk = (current_risk * current_amount + security_risk * amount) / (current_amount + amount)
#         return total_risk

#     def is_risk_acceptable(self, total_risk):
#         """
#         בודקת האם הסיכון הכולל של התיק **לא חורג מהטווח העליון** של רמת הסיכון שנבחרה.
#         המשתמש יכול לקנות מניות/אג"ח בסיכון נמוך יותר ללא מגבלה כל עוד לא עובר את המקסימום.
#         """
#         _, max_risk = self._get_risk_range_for_level()  # קבלת הטווח העליון בלבד
#         return total_risk <= max_risk  # מותר כל עוד לא חורגים מהעליון

#     def _get_risk_range_for_level(self):
#         """
#         מחזירה את הטווח (min, max) של רמת הסיכון שנבחרה.
#         """
#         risk_ranges = {
#             'Low': (0.1, 2.5),
#             'Medium': (2.51, 4.5),
#             'High': (4.51, float('inf'))
#         }
#         return risk_ranges[self.risk_level]

#     def get_advice(self, question):
#         print("Getting AI advice...")
#         answer = self.ollamamodel.get_advice(question)
#         print("AI Advice:", answer)
#         return answer

#     def calculate_projected_risk(self, name, sector, variance, security_type, subtype, amount):
#         # יצירת אובייקט מניה או אג"ח
#         if security_type == 'stock':
#             security = Stock(name, sector, variance, subtype)
#         elif security_type == 'bond':
#             security = Bond(name, sector, variance, subtype)
#         else:
#             return self.portfolio.calculate_total_risk()  # מחזיר סיכון קיים אם לא זוהה

#         # חישוב הסיכון של הנייר החדש
#         security_risk = security.calculate_risk()

#         # שליפת כמות כוללת בתיק הנוכחי
#         current_data = self.dbmodel.getdata()
#         total_current_amount = sum(sec['ammont'] for sec in current_data.values())
#         current_total_risk = self.portfolio.calculate_total_risk()

#         # חישוב סיכון משוקלל חדש
#         total_risk = (current_total_risk * total_current_amount + security_risk * amount) / (total_current_amount + amount)

#         return total_risk
    
#     def get_individual_risk(self, security_obj):
#         # מחשב סיכון אישי של נייר ערך לפי הנתונים.
#         if security_obj.security_type == 'stock':
#             security = Stock(security_obj.name, security_obj.sector, security_obj.variance, security_obj.subtype)
#         elif security_obj.security_type == 'bond':
#             security = Bond(security_obj.name, security_obj.sector, security_obj.variance, security_obj.subtype)
#         else:
#             return 0  # לא חוקי
#         return security.calculate_risk()

#     def show_portfolio_graph(self):
#         self.portfolio.show_portfolio_graph()


# # ===================================
# # גרסה חדשה של controller, מקבל ממשקים


# class ControllerV2:
#     def __init__(self, risk_level: str, db_repo: IDataRepository, ai_advisor: IAIAdvisor):
#         self.db = db_repo
#         self.ai_advisor = ai_advisor
#         self.portfolio = Portfolio(self.db)
#         self.risk_level = risk_level

#     # (כאן ייכנס כל הקוד של קנייה/מכירה בדיוק כמו שכתבנו קודם)


















# כל המחלקות והייבואים הרגילים נשארים למעלה

# === המחלקה הקיימת (לא לגעת!) ===
class controller:
    def __init__(self, risk_level: str):
        self.dbmodel = dbmodel()
        self.portfolio = Portfolio(self.dbmodel)
        self.ollamamodel = ollamamodel()
        self.risk_level = risk_level

    # כל המתודות הקיימות שלך (כמו ששלחת)

# ===================================
# גרסה חדשה של controller, מקבל ממשקים

class ControllerV2:
    def __init__(self, risk_level: str, db_repo: IDataRepository, ai_advisor: IAIAdvisor):
        self.db = db_repo
        self.ai_advisor = ai_advisor
        self.portfolio = Portfolio(self.db)
        self.risk_level = risk_level

    def get_available_securities(self):
        return self.db.get_available_securities()

    def buy(self, name, sector, variance, security_type, subtype, amount, basevalue):
        security_data = SecurityData(None, name, basevalue, amount, sector, variance, security_type, subtype)
        current_risk = self.portfolio.calculate_total_risk()
        projected_risk = self.portfolio.calculate_projected_risk_with_new_security(security_data, amount)
        min_risk, max_risk = self._get_risk_range_for_level()

        print(f"\n🧮 Current portfolio risk: {current_risk:.2f}")
        print(f"📈 Projected portfolio risk after purchase: {projected_risk:.2f}")

        if current_risk > max_risk and projected_risk > current_risk:
            return False, f"⚠️ Cannot buy '{name}'. Portfolio already exceeds risk limit ({current_risk:.2f}), and this purchase would increase it to {projected_risk:.2f}."
        if not (min_risk <= projected_risk <= max_risk):
            return False, f"⚠️ Cannot buy '{name}'. Total projected risk {projected_risk:.2f} exceeds acceptable range for '{self.risk_level}' risk level."

        self.db.insert_or_update(name, sector, variance, security_type, subtype, basevalue, amount)
        return True, f"✅ '{name}' bought successfully! Total portfolio risk: {projected_risk:.2f}"

    def sell(self, name, security_type, sector, subtype, amount):
        portfolio = self.db.get_portfolio_data()
        security = next(
            (s for s in portfolio if s.name == name and s.security_type == security_type and s.sector == sector and s.subtype == subtype),
            None
        )
        if not security:
            return False, f"❌ Security '{name}' not found in portfolio."
        if security.ammont < amount:
            return False, f"❌ Not enough units to sell. You own {security.ammont} units."
        self.db.sell(name, amount)
        updated_risk = self.portfolio.calculate_total_risk()
        return True, f"✅ '{name}' sold successfully! Total portfolio risk after sale: {updated_risk:.2f}"

    def get_portfolio_data(self):
        return self.db.get_portfolio_data()

    def get_total_risk(self):
        return self.portfolio.calculate_total_risk()

    def is_risk_acceptable(self, total_risk):
        _, max_risk = self._get_risk_range_for_level()
        return total_risk <= max_risk

    def _get_risk_range_for_level(self):
        risk_ranges = {'Low': (0.1, 2.5), 'Medium': (2.51, 4.5), 'High': (4.51, float('inf'))}
        return risk_ranges[self.risk_level]

    def get_advice(self, question):
        print("Getting AI advice...")
        answer = self.ai_advisor.get_advice(question)
        print("AI Advice:", answer)
        return answer

    def calculate_projected_risk(self, name, sector, variance, security_type, subtype, amount):
        if security_type == 'stock':
            security = Stock(name, sector, variance, subtype)
        elif security_type == 'bond':
            security = Bond(name, sector, variance, subtype)
        else:
            return self.portfolio.calculate_total_risk()
        security_risk = security.calculate_risk()
        current_data = self.db.get_portfolio_data()
        total_current_amount = sum(sec.ammont for sec in current_data)
        current_total_risk = self.portfolio.calculate_total_risk()
        total_risk = (current_total_risk * total_current_amount + security_risk * amount) / (total_current_amount + amount)
        return total_risk

    def get_individual_risk(self, security_obj):
        if security_obj.security_type == 'stock':
            security = Stock(security_obj.name, security_obj.sector, security_obj.variance, security_obj.subtype)
        elif security_obj.security_type == 'bond':
            security = Bond(security_obj.name, security_obj.sector, security_obj.variance, security_obj.subtype)
        else:
            return 0
        return security.calculate_risk()

    def show_portfolio_graph(self):
        self.portfolio.show_portfolio_graph()
