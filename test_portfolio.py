from controller import controller
from dbmodel import dbmodel

def test_portfolio_advanced():
    print("\n🧪 Starting Advanced Portfolio Test with DB Checks:")

    db = dbmodel()
    db.clear_portfolio()  # מנקה תיק קיים
    ctrl = controller("High")

    # 1. קניית Apple ו-GovBond
    print("\n💸 Buying 'Apple' x10")
    ctrl.buy("Apple", "Technology", "High", "stock", "common", 10, 360.0)
    print("\n💸 Buying 'GovBond' x5")
    ctrl.buy("GovBond", "Finance", "Low", "bond", "government", 5, 150.0)

    # בדיקת מצב ה-DB
    print("\n📊 Portfolio after buys:")
    data = db.getdata()
    for sec in data.values():
        print(sec)

    # 2. מכירת 3 Apple
    print("\n💸 Selling 'Apple' x3")
    success, msg = ctrl.sell("Apple", 3)
    print(msg)

    # בדיקת מצב ה-DB
    print("\n📊 Portfolio after selling 3 Apple:")
    data = db.getdata()
    for sec in data.values():
        print(sec)

    # 3. מכירת כל GovBond
    print("\n💸 Selling 'GovBond' x5")
    success, msg = ctrl.sell("GovBond", 5)
    print(msg)

    # בדיקת מצב ה-DB
    print("\n📊 Portfolio after selling all GovBond:")
    data = db.getdata()
    for sec in data.values():
        print(sec)

    # 4. חישוב סיכון
    total_risk = ctrl.get_total_risk()
    print(f"\n📊 Total Portfolio Risk: {total_risk:.2f}")

    # 5. ניסיון למכור יותר ממה שיש
    print("\n⚠️ Trying to oversell 'Apple' x100")
    success, msg = ctrl.sell("Apple", 100)
    print(msg)

    # 6. בדיקה אחרונה של מצב ה-DB
    print("\n📊 Final Portfolio:")
    data = db.getdata()
    for sec in data.values():
        print(sec)

    print("\n✅ Advanced Portfolio tests completed.\n")

if __name__ == "__main__":
    test_portfolio_advanced()
