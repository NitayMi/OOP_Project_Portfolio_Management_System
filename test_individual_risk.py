from controller import controller
from dbmodel import dbmodel

def test_individual_risk():
    print("\n🧪 Testing Individual Risk Calculation:")

    # הכנה: חיבור ל-DB וניקוי התיק
    db = dbmodel()
    db.clear_portfolio()
    print("✅ Portfolio cleared for test.")

    # יצירת Controller
    ctrl = controller("Medium")  # רמת סיכון לא משפיעה על הבדיקה הזו

    # הוספת ניירות ערך לבדיקה
    db.insert_or_update(name="Apple", sector="Technology", variance="High", security_type="stock",
                        subtype="common", basevalue=360.0, amount=5)
    db.insert_or_update(name="GovBond", sector="Finance", variance="Low", security_type="bond",
                        subtype="government", basevalue=150.0, amount=10)

    # קבלת נתוני תיק
    portfolio = db.getdata()

    # בדיקה לכל נייר ערך
    for sec in portfolio.values():
        risk = ctrl.get_individual_risk(sec)
        print(f"- {sec['name']} | Type: {sec['type']} | Risk: {risk:.2f}")

    print("\n✅ Individual risk test completed successfully!")


if __name__ == "__main__":
    test_individual_risk()
