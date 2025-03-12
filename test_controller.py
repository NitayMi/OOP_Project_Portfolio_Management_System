from controller import controller

# Create a controller with Medium risk level
my_controller = controller(risk_level="Medium")

# --- Test 1: Buying a stock that fits the risk level ---
print("\n--- Test 1: Buy Stock (Should be Accepted) ---")
my_controller.buy(
    name="TechStock",
    sector="Technology",
    variance="High",
    security_type="stock",
    preferred=False,
    amount=10
)

# --- Test 2: Buying a bond that fits the risk level ---
print("\n--- Test 2: Buy Bond (Should be Accepted) ---")
my_controller.buy(
    name="GovBond",
    sector="Industry",
    variance="Low",
    security_type="bond",
    government=True,
    amount=5
)

# --- Test 3: Trying to buy a security that may exceed risk level ---
print("\n--- Test 3: Buy Stock (May be Rejected if exceeds risk) ---")
my_controller.buy(
    name="RiskyTech",
    sector="Technology",
    variance="High",
    security_type="stock",
    preferred=False,
    amount=15
)

# --- Test 4: Selling a security ---
print("\n--- Test 4: Sell Stock (TechStock) ---")
my_controller.sell(name="TechStock")

# --- Test 5: Getting AI advice ---
print("\n--- Test 5: Get AI Advice ---")
response = my_controller.get_advice("Should I invest in Tesla?")
print("AI Response:", response)

# --- Test 6: Show Portfolio ---
print("\n--- Test 6: Show Portfolio ---")
my_controller.show()
