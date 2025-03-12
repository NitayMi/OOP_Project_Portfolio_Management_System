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

  
# הקוד שלי  
from dbmodel import dbmodel
from ollamamodel import ollamamodel
from securitiesmodel import Stock, Bond, Portfolio

class controller:
    def __init__(self, risk_level: str):
        self.portfolio = Portfolio()  # Our Portfolio instance
        self.dbmodel = dbmodel()  # Database model
        self.ollamamodel = ollamamodel()  # AI Advisor
        self.risk_level = risk_level  # Desired risk level: 'Low', 'Medium', 'High'

    def buy(self, name, sector, variance, security_type, preferred=False, government=True, amount=1):
        if security_type.lower() == "stock":
            security = Stock(name, sector, variance, preferred)
        elif security_type.lower() == "bond":
            security = Bond(name, sector, variance, government)
        else:
            return False, "Invalid security type. Please choose 'stock' or 'bond'."

        # Create a temp portfolio to check risk before adding
        temp_portfolio = Portfolio()
        temp_portfolio.securities = self.portfolio.securities + [security]
        total_risk = temp_portfolio.calculate_total_risk()

        if self.is_risk_acceptable(total_risk):
            self.portfolio.add_security(security)
            self.dbmodel.insert(name, amount)  # Save to database
            return True, f"{security_type.capitalize()} '{name}' bought successfully. Total portfolio risk: {total_risk:.2f}"
        else:
            return False, f"Cannot buy {security_type} '{name}'. Total risk {total_risk:.2f} exceeds acceptable range for '{self.risk_level}' risk level."


    def sell(self, name):
        self.portfolio.remove_security(name)
        self.dbmodel.delete(name)  # Delete from database
        print(f"Security '{name}' sold (removed) successfully.")

    def get_advice(self, question):
        print("Getting AI advice...")
        answer = self.ollamamodel.get_advice(question)
        print("AI Advice:", answer)
        return answer

    def show(self):
        print("\n--- Current Portfolio ---")
        self.portfolio.display_portfolio()
        total_risk = self.portfolio.calculate_total_risk()
        print(f"Total Portfolio Risk: {total_risk:.2f}")

    def is_risk_acceptable(self, total_risk):
        risk_ranges = {
            'Low': (0.1, 2.5),
            'Medium': (0.1, 4.5),
            'High': (0.1, float('inf'))
        }
        min_risk, max_risk = risk_ranges[self.risk_level]
        return min_risk <= total_risk <= max_risk

    def get_available_securities(self):
        return self.dbmodel.get_available_securities()

    def get_portfolio_data(self):
        portfolio_securities = [
            sec.get_info() for sec in self.portfolio.securities
        ]
        total_risk = self.portfolio.calculate_total_risk()

        return {
            'securities': portfolio_securities,
            'total_risk': total_risk
        }
