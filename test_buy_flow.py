from controller import controller
from dbmodel import dbmodel

def test_buy_flow():
    print("\n🧪 Starting Full Buy Flow Test:")

    # אתחול DB וניקוי תיק ההשקעות
    db = dbmodel()
    db.clear_portfolio()
    ctrl = controller("High")  # רמת סיכון High כדי לא לחסום רכישות

    # שליפת ניירות ערך זמינים
    available_securities = ctrl.get_available_securities()
    assert len(available_securities) > 0, "❌ No available securities found!"

    # בחירת נייר ערך לבדיקה
    test_security = available_securities[0]  # ניקח את הראשון
    name = test_security['name']
    sector = test_security['sector']
    variance = test_security['variance']
    security_type = test_security['type']
    subtype = test_security['sub_type']
    basevalue = test_security['basevalue']
    amount_to_buy = 10

    print(f"\n➡️ Selected Security to Buy: {name}, Type: {security_type}, Sector: {sector}, Variance: {variance}")

    # חישוב סיכון צפוי לפני קנייה
    projected_risk = ctrl.calculate_projected_risk(name, sector, variance, security_type, subtype, amount_to_buy)
    print(f"📊 Projected Portfolio Risk after buying {amount_to_buy} of {name}: {projected_risk:.2f}")

    # ביצוע קנייה
    success, message = ctrl.buy(
        name=name, sector=sector, variance=variance, security_type=security_type,
        subtype=subtype, amount=amount_to_buy, basevalue=basevalue
    )
    assert success, f"❌ Failed to buy security: {message}"
    print(f"✅ {message}")

    # בדיקת סיכון כולל בתיק לאחר הקנייה
    total_risk = ctrl.get_total_risk()
    print(f"📊 Total Portfolio Risk Now: {total_risk:.2f}")

    # בדיקת נוכחות נייר ערך בתיק דרך ה-DB
    portfolio_data = ctrl.get_portfolio_data()
    found = any(sec['name'] == name for sec in portfolio_data.values())
    assert found, "❌ Security not found in portfolio after buy!"
    print(f"✅ Security '{name}' found in portfolio with amount {amount_to_buy}.")

    print("\n✅ All Buy Flow Tests Passed Successfully!")


if __name__ == "__main__":
    test_buy_flow()
