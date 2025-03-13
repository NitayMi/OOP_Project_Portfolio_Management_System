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

  
# # קוד ישן 11.03  
# from dbmodel import dbmodel
# from ollamamodel import ollamamodel
# from securitiesmodel import Stock, Bond, Portfolio

# class controller:
#     def __init__(self, risk_level: str):
#         self.portfolio = Portfolio()  # Our Portfolio instance
#         self.dbmodel = dbmodel()  # Database model
#         self.ollamamodel = ollamamodel()  # AI Advisor
#         self.risk_level = risk_level  # Desired risk level: 'Low', 'Medium', 'High'

#     def buy(self, name, sector, variance, security_type, preferred=False, government=True, amount=1):
#         if security_type.lower() == "stock":
#             security = Stock(name, sector, variance, preferred)
#         elif security_type.lower() == "bond":
#             security = Bond(name, sector, variance, government)
#         else:
#             return False, "Invalid security type. Please choose 'stock' or 'bond'."

#         # Create a temp portfolio to check risk before adding
#         temp_portfolio = Portfolio()
#         temp_portfolio.securities = self.portfolio.securities + [security]
#         total_risk = temp_portfolio.calculate_total_risk()

#         if self.is_risk_acceptable(total_risk):
#             self.portfolio.add_security(security)
#             self.dbmodel.insert(name, amount)  # Save to database
#             return True, f"{security_type.capitalize()} '{name}' bought successfully. Total portfolio risk: {total_risk:.2f}"
#         else:
#             return False, f"Cannot buy {security_type} '{name}'. Total risk {total_risk:.2f} exceeds acceptable range for '{self.risk_level}' risk level."


#     def sell(self, name):
#         self.portfolio.remove_security(name)
#         self.dbmodel.delete(name)  # Delete from database
#         print(f"Security '{name}' sold (removed) successfully.")

#     def get_advice(self, question):
#         print("Getting AI advice...")
#         answer = self.ollamamodel.get_advice(question)
#         print("AI Advice:", answer)
#         return answer

#     def show(self):
#         print("\n--- Current Portfolio ---")
#         self.portfolio.display_portfolio()
#         total_risk = self.portfolio.calculate_total_risk()
#         print(f"Total Portfolio Risk: {total_risk:.2f}")

#     def is_risk_acceptable(self, total_risk):
#         risk_ranges = {
#             'Low': (0.1, 2.5),
#             'Medium': (0.1, 4.5),
#             'High': (0.1, float('inf'))
#         }
#         min_risk, max_risk = risk_ranges[self.risk_level]
#         return min_risk <= total_risk <= max_risk

#     def get_available_securities(self):
#         return self.dbmodel.get_available_securities()

#     def get_portfolio_data(self):
#         portfolio_securities = [
#             sec.get_info() for sec in self.portfolio.securities
#         ]
#         total_risk = self.portfolio.calculate_total_risk()

#         return {
#             'securities': portfolio_securities,
#             'total_risk': total_risk
#         }



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
