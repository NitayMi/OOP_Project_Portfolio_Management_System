# כדאי לבקש למלא בתכונות מסוכן וכך נוכל להגדיר סוגי ניירות ערך ולהגדיר קשרים ביניהם

# class secuity:
#     def __init__(self):
#         pass 

# class stock(secuity):
#     def __init__(self):
#         super().__init__()

# class bond(secuity):
#     def __init__(self):
#         super().__init__()

# class regularstock(stock):
#     def __init__(self):
#         super().__init__()

# class preferredstock(stock):
#     def __init__(self):
#         super().__init__()

# class corporatebond(bond):
#     def __init__(self):
#         super().__init__()

# class govermentalbond(bond):
#     def __init__(self):
#         super().__init__()


        

# ------------------------------------------

from abc import ABC, abstractmethod

# 1. Abstract base class for all securities
class Security(ABC):
    def __init__(self, name: str, sector: str, variance: str, security_type: str):
        self.name = name  # Security name
        self.sector = sector  # Sector (e.g., Technology, Real Estate)
        self.variance = variance  # Variance (Low/High)
        self.security_type = security_type  # Stock or Bond

    @abstractmethod
    def calculate_risk(self) -> float:
        pass  # Abstract method for calculating risk

    @abstractmethod
    def get_info(self) -> dict:
        pass  # Abstract method to return security information

# 2 Stock class inheriting from Security
class Stock(Security):
    def __init__(self, name: str, sector: str, variance: str, preferred: bool = False):
        super().__init__(name, sector, variance, "Stock")
        self.preferred = preferred  # Preferred stock (True/False)

    def calculate_risk(self) -> float:
        alpha, beta, gamma = 0.5, 0.3, 0.2
        sector_risk = self._get_sector_risk()
        variance_risk = self._get_variance_risk()
        type_risk = 1  # Stock is always 1

        return alpha * sector_risk + beta * variance_risk + gamma * type_risk

    def _get_sector_risk(self) -> float:
        sectors = {
            "Technology": 6, "Transportation and Aviation": 5,
            "Energy": 4, "Health": 4, "Industry": 3,
            "Finance": 3, "Real Estate": 2, "Private Consumption": 1
        }
        return sectors.get(self.sector, 3)

    def _get_variance_risk(self) -> float:
        return 2 if self.variance.lower() == "high" else 1

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "sector": self.sector,
            "variance": self.variance,
            "type": "Preferred Stock" if self.preferred else "Common Stock",
            "risk": self.calculate_risk()
        }

# 3. Bond class inheriting from Security
class Bond(Security):
    def __init__(self, name: str, sector: str, variance: str, government: bool = True):
        super().__init__(name, sector, variance, "Bond")
        self.government = government  # Government bond (True/False)

    def calculate_risk(self) -> float:
        alpha, beta, gamma = 0.5, 0.3, 0.2
        sector_risk = self._get_sector_risk()
        variance_risk = self._get_variance_risk()
        type_risk = 0.5 if self.government else 0.1  # Government or Corporate

        base_risk = alpha * sector_risk + beta * variance_risk + gamma * type_risk
        final_risk = base_risk * (0.5 if self.government else 0.1)
        return final_risk

    def _get_sector_risk(self) -> float:
        sectors = {
            "Technology": 6, "Transportation and Aviation": 5,
            "Energy": 4, "Health": 4, "Industry": 3,
            "Finance": 3, "Real Estate": 2, "Private Consumption": 1
        }
        return sectors.get(self.sector, 3)

    def _get_variance_risk(self) -> float:
        return 2 if self.variance.lower() == "high" else 1

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "sector": self.sector,
            "variance": self.variance,
            "type": "Government Bond" if self.government else "Corporate Bond",
            "risk": self.calculate_risk()
        }

# 4.Portfolio class to manage a list of securities
class Portfolio:
    def __init__(self):
        self.securities = []  # List of securities

    def add_security(self, security: Security):
        self.securities.append(security)

    def remove_security(self, name: str):
        self.securities = [sec for sec in self.securities if sec.name != name]

    def calculate_total_risk(self) -> float:
        if not self.securities:
            return 0
        total_risk = sum(sec.calculate_risk() for sec in self.securities)
        return total_risk / len(self.securities)

    def display_portfolio(self):
        for sec in self.securities:
            print(sec.get_info())
