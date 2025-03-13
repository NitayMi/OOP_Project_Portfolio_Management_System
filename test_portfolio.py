# from controller import controller


# def test_portfolio_operations():
#     print("\n✅ Starting Portfolio Operations Test")
    
#     # יצירת אובייקט Controller
#     ctrl = controller("High")  # High risk level, לא להגביל קנייה
    
#     # ניקוי התיק לניסוי נקי
#     ctrl.dbmodel.clear_portfolio()
#     print("Portfolio cleared for tests.")

#     # קנייה ראשונה
#     print("\n🟢 Test: Buying 5 Apple")
#     success, message = ctrl.buy(
#         name="Apple",
#         sector="Technology",
#         variance="High",
#         security_type="stock",
#         subtype="common",
#         amount=5,
#         basevalue=360.0
#     )
#     print(message)
#     assert success, "Failed to buy Apple"

#     # קנייה שנייה
#     print("\n🟢 Test: Buying 10 Teva")
#     success, message = ctrl.buy(
#         name="Teva",
#         sector="Health",
#         variance="Low",
#         security_type="stock",
#         subtype="common",
#         amount=10,
#         basevalue=100.0
#     )
#     print(message)
#     assert success, "Failed to buy Teva"

#     # בדיקה: הצגת תיק ונכון סיכון
#     print("\n📊 Portfolio after purchases:")
#     portfolio_data = ctrl.get_portfolio_data()
#     print(portfolio_data)

#     total_risk = ctrl.portfolio.calculate_total_risk()
#     print(f"\n🔑 Total Portfolio Risk: {total_risk:.2f}")

#     # מכירה חלקית
#     print("\n🔻 Test: Selling 3 Apple")
#     success, message = ctrl.sell("Apple", 3)
#     print(message)
#     assert success, "Failed to sell Apple"

#     # בדיקה: הצגת תיק לאחר מכירה
#     print("\n📊 Portfolio after partial sale:")
#     portfolio_data = ctrl.get_portfolio_data()
#     print(portfolio_data)

#     total_risk_after_sell = ctrl.portfolio.calculate_total_risk()
#     print(f"\n🔑 Total Portfolio Risk after sale: {total_risk_after_sell:.2f}")

#     # בדיקה סופית
#     print("\n✅ Portfolio test completed successfully!")


# if __name__ == "__main__":
#     test_portfolio_operations()










from controller import controller
from dbmodel import dbmodel

def test_portfolio_full():
    print("\n🧪 Starting Full Portfolio Test with DB Sync:")

    db = dbmodel()
    db.clear_portfolio()  # מתחילים תיק ריק

    ctrl = controller("High")  # הגדרת רמת סיכון חופשי

    # Step 1: קניה ראשונה
    print("\n💸 Buying 'Apple' x10")
    ctrl.buy(name="Apple", sector="Technology", variance="High", security_type="stock",
             subtype="common", amount=10, basevalue=360.0)

    # בדיקה שהוזן לDB
    data = db.getdata()
    assert any(sec['name'] == "Apple" and sec['ammont'] == 10 for sec in data.values()), "❌ Apple not added correctly"

    # Step 2: קניה שניה
    print("\n💸 Buying 'GovBond' x5")
    ctrl.buy(name="GovBond", sector="Finance", variance="Low", security_type="bond",
             subtype="government", amount=5, basevalue=150.0)

    # בדיקה שהוזן לDB
    data = db.getdata()
    assert any(sec['name'] == "GovBond" and sec['ammont'] == 5 for sec in data.values()), "❌ GovBond not added correctly"

    # Step 3: בדיקת סיכון
    total_risk = ctrl.get_total_risk()
    print(f"📊 Total Portfolio Risk after buying: {total_risk:.2f}")

    # Step 4: מכירה חלקית
    print("\n💸 Selling 'Apple' x5")
    ctrl.sell("Apple", 5)

    # בדיקה שהעודכן בDB
    data = db.getdata()
    assert any(sec['name'] == "Apple" and sec['ammont'] == 5 for sec in data.values()), "❌ Apple partial sell failed"

    # Step 5: מכירה מלאה
    print("\n💸 Selling 'GovBond' x5")
    ctrl.sell("GovBond", 5)

    # בדיקה שהוסר מהDB
    data = db.getdata()
    assert not any(sec['name'] == "GovBond" for sec in data.values()), "❌ GovBond not removed after full sell"

    # Step 6: בדיקת סיכון אחרי המכירות
    total_risk = ctrl.get_total_risk()
    print(f"📊 Total Portfolio Risk after selling: {total_risk:.2f}")

    print("\n✅ All Portfolio tests passed successfully!\n")

if __name__ == "__main__":
    test_portfolio_full()
