from dbmodel import dbmodel, SecurityData, IDataRepository
from ollamamodel import IAIAdvisor  # ✅ יבוא רק הממשק ולא מחלקות בעייתיות
from securitiesmodel import Stock, Bond, Portfolio
from rag_loader import get_collection  # טעינת הקולקשן תתבצע רק כשצריך
from ollamamodel import AIAdvisorRAG

class ControllerV2:
    def __init__(self, risk_level: str, db_repo: IDataRepository, ai_advisor: None):
        self.db = db_repo
        self.portfolio = Portfolio(self.db)
        self.risk_level = risk_level

        # טעינת AI פעם אחת בלבד
        if ai_advisor is None:
            self.ai_advisor = AIAdvisorRAG(model="deepseek-r1:7b")
        else:
            self.ai_advisor = ai_advisor

    def set_risk_level(self, risk_level: str):
        """
        Set risk level dynamically based on user input.
        """
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

    def get_advice(self, question, portfolio, total_risk):
        """
        Get AI-based investment advice using AIAdvisorRAG, based on user's portfolio.
        """
        print("🔍 Getting AI advice with RAG and personalized portfolio context...")
        # שימוש בנתוני התיק שכבר נטענו, כדי לא לקרוא שוב ל-DB
        answer = self.ai_advisor.get_advice(f"Give a concise investment recommendation in 2 sentences: {question}", portfolio_data=portfolio)

        print("💡 AI Advice:", answer)
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
