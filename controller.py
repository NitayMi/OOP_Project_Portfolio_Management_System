# הקוד של יוסי
# from dbmodel import dbmodel
# from ollamamodel import ollamamodel

# class controller():
#     def __init__(self):
#         self.dbmodel = dbmodel()
#         self.ollamamodel = ollamamodel()       
        
#     def buy(self,whatsecurity,ammout):
#         print("Buying...")
#         self.dbmodel.insert(whatsecurity,ammout)

#     def sell(self):
#        print("Selling...")
#        self.dbmodel.delete()

#     def get_advice(self,question):
#        print("Getting advice...")
#        answer= self.ollamamodel.get_advice(question)
#        return answer


# קוד חדש 13.02
from dbmodel import dbmodel, SecurityData
from securitiesmodel import Stock, Bond
from ollamamodel import ollamamodel
from securitiesmodel import Stock, Bond, Portfolio

class controller:
    def __init__(self, risk_level: str):
        self.dbmodel = dbmodel()  # Database model
        self.portfolio = Portfolio(self.dbmodel)  # Portfolio instance linked to DB
        self.ollamamodel = ollamamodel()  # AI Advisor
        self.risk_level = risk_level  # Risk preference

    def get_available_securities(self):
        return self.dbmodel.get_available_securities()

    def buy(self, name, sector, variance, security_type, subtype, amount, basevalue):
        """
        מבצע קניית נייר ערך, כולל בדיקת סיכון והתאמה לרמת הסיכון של התיק.
        """
        # יצירת אובייקט נייר ערך בהתאם לסוג
        if security_type == 'stock':
            security = Stock(name, sector, variance, subtype)
        elif security_type == 'bond':
            security = Bond(name, sector, variance, subtype)
        else:
            return False, "Invalid security type."

        # חישוב סיכון נוכחי של התיק
        current_risk = self.portfolio.calculate_total_risk()
        # חישוב סיכון צפוי אחרי הקנייה
        projected_risk = self._calculate_risk_with_new_security(security, amount)

        # ✅ הצגת סיכון למשתמש
        print(f"\n🧮 Current portfolio risk: {current_risk:.2f}")
        print(f"📈 Projected portfolio risk after purchase: {projected_risk:.2f}")

        # ✅ לוגיקה נכונה:
        # 1. אם התיק כבר חורג מהסיכון, נאפשר קנייה שמקטינה או לא מחמירה את הסיכון.
        _, max_risk = self._get_risk_range_for_level()  # שליפת מקסימום רמת סיכון
        if current_risk > max_risk:
            if projected_risk > current_risk:
                return False, f"⚠️ Cannot buy '{name}'. Portfolio already exceeds risk limit ({current_risk:.2f}), and this purchase would increase it to {projected_risk:.2f}."
           
        # 2. אם התיק עומד בדרישות, לבדוק שהקנייה לא תגרום לחריגה.
        else:
            if not self.is_risk_acceptable(projected_risk):
                return False, f"⚠️ Cannot buy '{name}'. Total projected risk {projected_risk:.2f} exceeds acceptable range for '{self.risk_level}' risk level."

        # ✅ אם עובר את הבדיקות, ממשיכים לקנייה והכנסת/עדכון במסד הנתונים
        self.dbmodel.insert_or_update(name, sector, variance, security_type, subtype, basevalue, amount)

        # החזרת הודעת הצלחה
        return True, f"✅ '{name}' bought successfully! Total portfolio risk: {projected_risk:.2f}"

    def sell(self, name, amount):
        """
        מוכר נייר ערך מהתיק, בודק אם אפשר למכור, מעדכן מסד נתונים, ומציג סיכון חדש.
        """

        # שליפת התיק מה-DB
        portfolio_data = self.dbmodel.getdata()

        # בדיקה אם נייר קיים בתיק
        matching_securities = [sec for sec in portfolio_data.values() if sec['name'] == name]
        if not matching_securities:
            return False, "❌ Security not found in portfolio."

        # בדיקת כמות נוכחית
        current_amount = sum(sec['ammont'] for sec in matching_securities)
        if current_amount < amount:
            return False, f"❌ Not enough units to sell. You own {current_amount} units."

        # ביצוע המכירה (עדכון או מחיקה לפי הכמות)
        self.dbmodel.sell(name, amount)

        # חישוב סיכון חדש אחרי המכירה
        new_risk = self.portfolio.calculate_total_risk()

        # החזרת הודעת הצלחה + סיכון חדש
        return True, f"✅ '{name}' sold successfully! Total portfolio risk after sale: {new_risk:.2f}"

    def get_portfolio_data(self):
        return self.dbmodel.get_portfolio_data()

    def get_total_risk(self):
        return self.portfolio.calculate_total_risk()
 
    def _calculate_risk_with_new_security(self, security, amount):
        current_risk = self.portfolio.calculate_total_risk()
        current_amount = sum(sec['ammont'] for sec in self.dbmodel.getdata().values())
        security_risk = security.calculate_risk()

        total_risk = (current_risk * current_amount + security_risk * amount) / (current_amount + amount)
        return total_risk

    def is_risk_acceptable(self, total_risk):
        """
        בודקת האם הסיכון הכולל של התיק **לא חורג מהטווח העליון** של רמת הסיכון שנבחרה.
        המשתמש יכול לקנות מניות/אג"ח בסיכון נמוך יותר ללא מגבלה כל עוד לא עובר את המקסימום.
        """
        _, max_risk = self._get_risk_range_for_level()  # קבלת הטווח העליון בלבד
        return total_risk <= max_risk  # מותר כל עוד לא חורגים מהעליון

    def _get_risk_range_for_level(self):
        """
        מחזירה את הטווח (min, max) של רמת הסיכון שנבחרה.
        """
        risk_ranges = {
            'Low': (0.1, 2.5),
            'Medium': (2.51, 4.5),
            'High': (4.51, float('inf'))
        }
        return risk_ranges[self.risk_level]

    def get_advice(self, question):
        print("Getting AI advice...")
        answer = self.ollamamodel.get_advice(question)
        print("AI Advice:", answer)
        return answer

# עדכון 13.03
    def calculate_projected_risk(self, name, sector, variance, security_type, subtype, amount):
        # יצירת אובייקט מניה או אג"ח
        if security_type == 'stock':
            security = Stock(name, sector, variance, subtype)
        elif security_type == 'bond':
            security = Bond(name, sector, variance, subtype)
        else:
            return self.portfolio.calculate_total_risk()  # מחזיר סיכון קיים אם לא זוהה

        # חישוב הסיכון של הנייר החדש
        security_risk = security.calculate_risk()

        # שליפת כמות כוללת בתיק הנוכחי
        current_data = self.dbmodel.getdata()
        total_current_amount = sum(sec['ammont'] for sec in current_data.values())
        current_total_risk = self.portfolio.calculate_total_risk()

        # חישוב סיכון משוקלל חדש
        total_risk = (current_total_risk * total_current_amount + security_risk * amount) / (total_current_amount + amount)

        return total_risk
    
    def get_individual_risk(self, security_obj):
        # מחשב סיכון אישי של נייר ערך לפי הנתונים.
        if security_obj.security_type == 'stock':
            security = Stock(security_obj.name, security_obj.sector, security_obj.variance, security_obj.subtype)
        elif security_obj.security_type == 'bond':
            security = Bond(security_obj.name, security_obj.sector, security_obj.variance, security_obj.subtype)
        else:
            return 0  # לא חוקי
        return security.calculate_risk()
