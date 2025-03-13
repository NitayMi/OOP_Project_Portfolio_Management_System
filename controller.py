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
from dbmodel import dbmodel
from ollamamodel import ollamamodel
from securitiesmodel import Stock, Bond, Portfolio

class controller:
    def __init__(self, risk_level: str):
        self.dbmodel = dbmodel()  # Database model
        self.portfolio = Portfolio(self.dbmodel)  # Portfolio instance linked to DB
        self.ollamamodel = ollamamodel()  # AI Advisor
        self.risk_level = risk_level  # Risk preference

    def buy(self, name, sector, variance, security_type, subtype, amount, basevalue):
        # Create security object for risk calculation
        if security_type == 'stock':
            security = Stock(name, sector, variance, subtype)
        elif security_type == 'bond':
            security = Bond(name, sector, variance, subtype)
        else:
            return False, "Invalid security type."

        # Risk check
        temp_risk = self._calculate_risk_with_new_security(security, amount)
        if not self.is_risk_acceptable(temp_risk):
            return False, f"Cannot buy '{name}'. Total risk {temp_risk:.2f} exceeds acceptable range for '{self.risk_level}' risk level."

        # Insert or update in DB
        self.dbmodel.insert_or_update(name, sector, variance, security_type, subtype, basevalue, amount)
        return True, f"'{name}' bought successfully! Total portfolio risk: {temp_risk:.2f}"

    def sell(self, name, amount):
        portfolio_data = self.dbmodel.getdata()
        if name not in [sec['name'] for sec in portfolio_data.values()]:
            return False, "Security not found in portfolio."

        current_amount = sum(sec['ammont'] for sec in portfolio_data.values() if sec['name'] == name)
        if current_amount < amount:
            return False, f"Not enough units to sell. You own {current_amount} units."

        self.dbmodel.sell(name, amount)
        return True, f"'{name}' sold successfully!"

    def get_portfolio_data(self):
        return self.dbmodel.getdata()

    def get_total_risk(self):
        return self.portfolio.calculate_total_risk()
 
    def _calculate_risk_with_new_security(self, security, amount):
        current_risk = self.portfolio.calculate_total_risk()
        current_amount = sum(sec['ammont'] for sec in self.dbmodel.getdata().values())
        security_risk = security.calculate_risk()

        total_risk = (current_risk * current_amount + security_risk * amount) / (current_amount + amount)
        return total_risk

    def is_risk_acceptable(self, total_risk):
        if self.risk_level == 'High':
            # רמת סיכון גבוהה - תמיד מאושר
            return True
        # רמות סיכון Low ו-Medium עם גבול
        risk_ranges = {
            'Low': (0.1, 2.5),
            'Medium': (2.51, 4.5)
        }
        min_risk, max_risk = risk_ranges[self.risk_level]
        return min_risk <= total_risk <= max_risk

    def get_available_securities(self):
        return self.dbmodel.get_available_securities()

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

    def get_individual_risk(self, security_dict):
        """מחזירה את סיכון הנייר ע"פ הנתונים שלו כפי שמופיעים בתיק"""
        if security_dict['type'] == 'stock':
            security = Stock(security_dict['name'], security_dict['sector'], security_dict['variance'], security_dict['subtype'])
        elif security_dict['type'] == 'bond':
            security = Bond(security_dict['name'], security_dict['sector'], security_dict['variance'], security_dict['subtype'])
        else:
            return 0  # אם זה לא מניה או אג"ח, מחזירים 0
        return security.calculate_risk()
