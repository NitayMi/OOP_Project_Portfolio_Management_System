from abc import ABC, abstractmethod
from dbmodel import SecurityData

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

    def _calculate_risk_for_securities(self, securities):
        """
        פונקציה פנימית שמחשבת סיכון משוקלל עבור כל רשימת ניירות ערך.
        """
        total_value = sum(float(sec.basevalue) * float(sec.ammont) for sec in securities)
        if total_value == 0:
            return 0

        weighted_risk = 0
        for sec in securities:
            # יצירת אובייקט Stock/Bond
            if sec.security_type == 'stock':
                security_obj = Stock(sec.name, sec.sector, sec.variance, sec.subtype)
            elif sec.security_type == 'bond':
                security_obj = Bond(sec.name, sec.sector, sec.variance, sec.subtype)
            else:
                continue  # סוג לא חוקי

            # חישוב סיכון יחסי
            risk = security_obj.calculate_risk()
            value = sec.basevalue * sec.ammont
            weight = value / total_value
            weighted_risk += risk * weight

        return weighted_risk

    def calculate_total_risk(self):
        """
        מחשבת את הסיכון הכולל של התיק לפי הנתונים במסד הנתונים.
        """
        securities = self.db.get_portfolio_data()
        return self._calculate_risk_for_securities(securities)

    def calculate_projected_risk_with_new_security(self, new_security, amount):
        """
        מחשב את הסיכון הכולל של התיק לאחר הוספת נייר ערך חדש.
        """
        securities = self.db.get_portfolio_data()

        # הוספת הנייר החדש כאילו קנינו אותו
        projected_securities = securities + [SecurityData(
            id=None,
            name=new_security.name,
            basevalue=new_security.basevalue,
            ammont=amount,
            sector=new_security.sector,
            variance=new_security.variance,
            security_type=new_security.security_type,
            subtype=new_security.subtype
        )]

        return self._calculate_risk_for_securities(projected_securities)
