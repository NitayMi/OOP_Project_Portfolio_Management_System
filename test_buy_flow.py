from controller import controller

def test_buy_scenario():
    # יצירת controller עם רמת סיכון בינונית (אפשר לשנות ל-High או Low)
    c = controller(risk_level='Medium')  # תוכל לשנות את ה-risk_level לפי בדיקות שונות

    # הצגת מצב התיק הנוכחי
    print("📊 Current Portfolio Data Before Test:")
    portfolio_data = c.get_portfolio_data()
    for item in portfolio_data:
        print(item)

    # הצגת סיכון נוכחי של התיק
    current_risk = c.get_total_risk()
    print(f"\n🧮 Total current portfolio risk before test: {current_risk:.2f}\n")

    # ----------------------
    # בדיקה 1: קניית מניה "Apple" עם סיכון נמוך
    print("🔵 Test 1: Buying 'Apple' (Stock, expected to PASS or borderline)")
    success, message = c.buy(
        name='Apple',
        sector='Technology',
        variance='Low',
        security_type='stock',
        subtype='regular',
        amount=10,
        basevalue=150
    )
    print(message)
    print("\n--------------------------\n")

    # ----------------------
    # בדיקה 2: קניית אג"ח ממשלתי "US Gov Bond" עם סיכון נמוך
    print("🟢 Test 2: Buying 'US Gov Bond' (Bond, expected to PASS)")
    success, message = c.buy(
        name='US Gov Bond',
        sector='Finance',
        variance='Low',
        security_type='bond',
        subtype='government',
        amount=5,
        basevalue=100
    )
    print(message)
    print("\n--------------------------\n")

    # ----------------------
    # בדיקה 3: קניית מניה מסוכנת "Risky Tech" בכמות גבוהה (צפוי להיכשל)
    print("🔴 Test 3: Buying 'Risky Tech' (High risk, expected to FAIL)")
    success, message = c.buy(
        name='Risky Tech',
        sector='Technology',
        variance='High',
        security_type='stock',
        subtype='regular',
        amount=1000,
        basevalue=50
    )
    print(message)
    print("\n--------------------------\n")

    # ----------------------
    # בדיקה 4: ניסיון לקנות נייר מסוג לא חוקי (crypto)
    print("⚫ Test 4: Buying 'Unknown' (Invalid security type, expected to FAIL)")
    success, message = c.buy(
        name='Unknown',
        sector='Unknown',
        variance='Low',
        security_type='crypto',  # לא חוקי
        subtype='none',
        amount=10,
        basevalue=500
    )
    print(message)
    print("\n--------------------------\n")


if __name__ == "__main__":
    test_buy_scenario()
