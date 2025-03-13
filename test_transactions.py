from controller import controller

def test_transactions():
    print("\n🧪 Starting Full Transaction Test:\n")
    ctrl = controller("High")  # בוחרים רמת סיכון 'High' לצורך בדיקה

    # ניקוי תיק ההשקעות
    ctrl.dbmodel.clear_portfolio()
    print("✅ Portfolio cleared for fresh test.\n")

    # ----- בדיקת קנייה -----
    print("💸 Buying 'Apple' x5")
    success, message = ctrl.buy(
        name="Apple", sector="Technology", variance="High",
        security_type="stock", subtype="common", amount=5, basevalue=360
    )
    print("✅" if success else "❌", message)

    print("\n💸 Buying 'GovBond' x10")
    success, message = ctrl.buy(
        name="GovBond", sector="Industry", variance="Low",
        security_type="bond", subtype="government", amount=10, basevalue=150
    )
    print("✅" if success else "❌", message)

    # הצגת התיק לאחר קניות
    print("\n📊 Portfolio after buying:")
    portfolio = ctrl.get_portfolio_data()
    for sec in portfolio.values():
        print(f"- {sec['name']} | Amount: {sec['ammont']} | Base Value: {sec['basevalue']}")
    total_risk = ctrl.get_total_risk()
    print(f"Total Portfolio Risk: {total_risk:.2f}")

    # ----- בדיקת מכירה -----
    print("\n💸 Selling 'Apple' x3")
    success, message = ctrl.sell(name="Apple", amount=3)
    print("✅" if success else "❌", message)

    print("\n💸 Selling 'GovBond' x5")
    success, message = ctrl.sell(name="GovBond", amount=5)
    print("✅" if success else "❌", message)

    # הצגת התיק לאחר מכירה
    print("\n📊 Portfolio after selling:")
    portfolio = ctrl.get_portfolio_data()
    for sec in portfolio.values():
        print(f"- {sec['name']} | Amount: {sec['ammont']} | Base Value: {sec['basevalue']}")
    total_risk = ctrl.get_total_risk()
    print(f"Total Portfolio Risk: {total_risk:.2f}")

    print("\n✅ All transaction tests completed successfully!\n")


if __name__ == "__main__":
    test_transactions()
