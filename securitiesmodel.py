# # כדאי לבקש למלא בתכונות מסוכן וכך נוכל להגדיר סוגי ניירות ערך ולהגדיר קשרים ביניהם

# # class secuity:
# #     def __init__(self):
# #         pass 

# # class stock(secuity):
# #     def __init__(self):
# #         super().__init__()

# # class bond(secuity):
# #     def __init__(self):
# #         super().__init__()

# # class regularstock(stock):
# #     def __init__(self):
# #         super().__init__()

# # class preferredstock(stock):
# #     def __init__(self):
# #         super().__init__()

# # class corporatebond(bond):
# #     def __init__(self):
# #         super().__init__()

# # class govermentalbond(bond):
# #     def __init__(self):
# #         super().__init__()


# קוד חדש 13.03
from abc import ABC, abstractmethod

class Security(ABC):
    def __init__(self, name, sector, variance, security_type, subtype):
        self.name = name
        self.sector = sector
        self.variance = variance
        self.security_type = security_type
        self.subtype = subtype

    @abstractmethod
    def calculate_risk(self):
        pass

class Stock(Security):
    def __init__(self, name, sector, variance, subtype):
        super().__init__(name, sector, variance, 'stock', subtype)

    def calculate_risk(self):
        variance_weight = 2 if self.variance.lower() == 'high' else 1  # שונות
        sector_weight = {
            'Technology': 6,
            'Transportation and Aviation': 5,
            'Energy': 4,
            'Health': 4,
            'Industry': 3,
            'Finance': 3,
            'Real Estate': 2,
            'Private Consumption': 1
        }.get(self.sector, 3)  # ברירת מחדל 3
        type_weight = 1  # מניות תמיד 1
        return variance_weight * sector_weight * type_weight
    
    # def calculate_risk(self):
    #     alpha, beta, gamma = 0.5, 0.3, 0.2
    #     sector_risk = self._get_sector_risk()
    #     variance_risk = self._get_variance_risk()
    #     type_risk = 1  # always 1 for stock

    #     return alpha * sector_risk + beta * variance_risk + gamma * type_risk

    def _get_sector_risk(self):
        sectors = {
            "Technology": 6, "Transportation and Aviation": 5, "Energy": 4, "Health": 4,
            "Industry": 3, "Finance": 3, "Real Estate": 2, "Private Consumption": 1
        }
        return sectors.get(self.sector, 3)

    def _get_variance_risk(self):
        return 2 if self.variance.lower() == "high" else 1

class Bond(Security):
    def __init__(self, name, sector, variance, subtype):
        super().__init__(name, sector, variance, 'bond', subtype)

    def calculate_risk(self):
        variance_weight = 2 if self.variance.lower() == 'high' else 1  # שונות
        sector_weight = {
            'Technology': 6,
            'Transportation and Aviation': 5,
            'Energy': 4,
            'Health': 4,
            'Industry': 3,
            'Finance': 3,
            'Real Estate': 2,
            'Private Consumption': 1
        }.get(self.sector, 3)  # ברירת מחדל 3
        if self.subtype == 'government':
            type_weight = 0.5  # אג"ח ממשלתי
        else:
            type_weight = 0.1  # אג"ח קונצרני
        return variance_weight * sector_weight * type_weight

    # def calculate_risk(self):
    #     alpha, beta, gamma = 0.5, 0.3, 0.2
    #     sector_risk = self._get_sector_risk()
    #     variance_risk = self._get_variance_risk()
    #     type_risk = 0.5 if self.subtype == "government" else 0.1  # government/corporate

    #     base_risk = alpha * sector_risk + beta * variance_risk + gamma * type_risk
    #     return base_risk * (0.5 if self.subtype == "government" else 0.1)

    def _get_sector_risk(self):
        sectors = {
            "Technology": 6, "Transportation and Aviation": 5, "Energy": 4, "Health": 4,
            "Industry": 3, "Finance": 3, "Real Estate": 2, "Private Consumption": 1
        }
        return sectors.get(self.sector, 3)

    def _get_variance_risk(self):
        return 2 if self.variance.lower() == "high" else 1

class Portfolio:
    def __init__(self, db):
        self.db = db

    def calculate_total_risk(self):
        data = self.db.getdata()
        if not data:
            return 0

        total_risk = 0
        total_amount = 0
        for sec in data.values():
            if sec['type'] == 'stock':
                security = Stock(sec['name'], sec['sector'], sec['variance'], sec['subtype'])
            elif sec['type'] == 'bond':
                security = Bond(sec['name'], sec['sector'], sec['variance'], sec['subtype'])
            else:
                continue  # skip unknown types

            risk = security.calculate_risk()
            total_risk += risk * sec['ammont']
            total_amount += sec['ammont']

        if total_amount == 0:
            return 0

        return total_risk / total_amount
