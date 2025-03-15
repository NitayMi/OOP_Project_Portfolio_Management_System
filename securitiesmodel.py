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
        """
        מחשבת את הסיכון הכולל של התיק לפי הנתונים במסד הנתונים.
        אם אין ניירות ערך, מחזירה 0.
        """

        # שליפת ניירות ערך מהתיק דרך dbmodel (כעת מחזיר רשימת SecurityData)
        securities = self.db.get_portfolio_data()

        if not securities:
            return 0  # אין ניירות ערך, אין סיכון

        # חישוב סך כל שווי ההשקעות
        total_value = sum(float(sec.basevalue) * float(sec.ammont) for sec in securities)

        if total_value == 0:
            return 0  # אין שווי השקעה, אין סיכון

        weighted_risk = 0  # סיכון משוקלל סופי

        for sec in securities:
            # יצירת אובייקט Stock/Bond לפי סוג
            if sec.security_type == 'stock':
                security_obj = Stock(sec.name, sec.sector, sec.variance, sec.subtype)
            elif sec.security_type == 'bond':
                security_obj = Bond(sec.name, sec.sector, sec.variance, sec.subtype)
            else:
                continue  # דילוג על סוג לא חוקי (למשל future סוג חדש)

            # חישוב סיכון אישי
            risk = security_obj.calculate_risk()

            # חישוב ערך השקעה (basevalue * amount)
            value = float(sec.basevalue) * float(sec.ammont)

            # חישוב משקל נייר בתיק
            weight = value / total_value

            # חישוב תרומת נייר לסיכון התיק
            weighted_risk += risk * weight

        return weighted_risk
