# כדאי לבקש למלא בתכונות מסוכן וכך נוכל להגדיר סוגי ניירות ערך ולהגדיר קשרים ביניהם

class secuity:
    def __init__(self):
        pass 

class stock(secuity):
    def __init__(self):
        super().__init__()

class bond(secuity):
    def __init__(self):
        super().__init__()

class regularstock(stock):
    def __init__(self):
        super().__init__()

class preferredstock(stock):
    def __init__(self):
        super().__init__()

class corporatebond(bond):
    def __init__(self):
        super().__init__()

class govermentalbond(bond):
    def __init__(self):
        super().__init__()