# טסט ישן
# from controller import controller

# # Create a controller with Medium risk level
# my_controller = controller(risk_level="Medium")

# # --- Test 1: Buying a stock that fits the risk level ---
# print("\n--- Test 1: Buy Stock (Should be Accepted) ---")
# my_controller.buy(
#     name="TechStock",
#     sector="Technology",
#     variance="High",
#     security_type="stock",
#     preferred=False,
#     amount=10
# )

# # --- Test 2: Buying a bond that fits the risk level ---
# print("\n--- Test 2: Buy Bond (Should be Accepted) ---")
# my_controller.buy(
#     name="GovBond",
#     sector="Industry",
#     variance="Low",
#     security_type="bond",
#     government=True,
#     amount=5
# )

# # --- Test 3: Trying to buy a security that may exceed risk level ---
# print("\n--- Test 3: Buy Stock (May be Rejected if exceeds risk) ---")
# my_controller.buy(
#     name="RiskyTech",
#     sector="Technology",
#     variance="High",
#     security_type="stock",
#     preferred=False,
#     amount=15
# )

# # --- Test 4: Selling a security ---
# print("\n--- Test 4: Sell Stock (TechStock) ---")
# my_controller.sell(name="TechStock")

# # --- Test 5: Getting AI advice ---
# print("\n--- Test 5: Get AI Advice ---")
# response = my_controller.get_advice("Should I invest in Tesla?")
# print("AI Response:", response)

# # --- Test 6: Show Portfolio ---
# print("\n--- Test 6: Show Portfolio ---")
# my_controller.show()







# טסט חדש 13.03
from controller import controller
from dbmodel import dbmodel

def reset_db():
    db = dbmodel()
    db.clear_portfolio()  # פונקציה לניקוי התיק - נכתוב אותה עוד רגע

def test_buy():
    print("\n✅ Testing Buy Function")
    reset_db()
    ctrl = controller("High")

    success, message = ctrl.buy(name="TestStock", sector="Finance", variance="Low", security_type="stock", amount=10, basevalue=150.0)
    assert success, "Buy failed when should succeed"
    print("Buy Passed:", message)

    # Test buying same stock again
    success, message = ctrl.buy(name="TestStock", sector="Finance", variance="Low", security_type="stock", amount=5, basevalue=150.0)
    assert success, "Failed to update existing stock"
    print("Buy Update Passed:", message)

def test_sell():
    print("\n✅ Testing Sell Function")
    reset_db()
    ctrl = controller("High")
    ctrl.buy(name="TestStock", sector="Finance", variance="Low", security_type="stock", amount=10, basevalue=150.0)

    success, message = ctrl.sell(name="TestStock", amount=5)
    assert success, "Sell failed when should succeed"
    print("Sell Passed:", message)

    success, message = ctrl.sell(name="TestStock", amount=10)
    assert not success, "Sell should fail when selling too much"
    print("Sell Over Amount Passed:", message)

def test_portfolio():
    print("\n✅ Testing Portfolio Fetch")
    reset_db()
    ctrl = controller("High")
    ctrl.buy(name="TestStock", sector="Finance", variance="Low", security_type="stock", amount=10, basevalue=150.0)

    portfolio = ctrl.get_portfolio_data()
    assert len(portfolio) == 1, "Portfolio should contain one item"
    print("Portfolio Fetch Passed:", portfolio)

def test_available_securities():
    print("\n✅ Testing Available Securities Fetch")
    ctrl = controller("High")
    available = ctrl.get_available_securities()
    assert len(available) > 0, "Should fetch available securities"
    print("Available Securities Passed:", available)

def test_advice():
    print("\n✅ Testing AI Advice")
    ctrl = controller("High")
    answer = ctrl.get_advice("Should I invest in Tesla?")
    assert isinstance(answer, str), "AI should return a string"
    print("AI Advice Passed:", answer)


if __name__ == "__main__":
    test_buy()
    test_sell()
    test_portfolio()
    test_available_securities()
    test_advice()
    print("\n🎉 All tests passed successfully.")
