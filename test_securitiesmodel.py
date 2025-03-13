from securitiesmodel import Stock, Bond
import math  # להוסיף לדיוק בחישובים

def test_stock_risk():
    print("\n🧪 Testing Stock Risk Calculation:")

    s1 = Stock("Apple", "Technology", "High", "common")
    s2 = Stock("Teva", "Health", "Low", "preferred")

    risk1 = s1.calculate_risk()
    risk2 = s2.calculate_risk()

    print(f"Risk of Apple (High, Technology): {risk1} (Expected: 12)")
    print(f"Risk of Teva (Low, Health): {risk2} (Expected: 4)")

    assert risk1 == 12, "❌ Error in Apple Stock Risk Calculation"
    assert risk2 == 4, "❌ Error in Teva Stock Risk Calculation"
    print("✅ Stock risk tests passed.")


def test_bond_risk():
    print("\n🧪 Testing Bond Risk Calculation:")

    b1 = Bond("GovBond", "Finance", "Low", "government")
    b2 = Bond("CorpBond", "Industry", "High", "corporate")

    risk1 = b1.calculate_risk()
    risk2 = b2.calculate_risk()

    print(f"Risk of GovBond (Low, Finance): {risk1} (Expected: 1.5)")
    print(f"Risk of CorpBond (High, Industry): {risk2} (Expected: 0.6)")

    assert math.isclose(risk1, 1.5, rel_tol=1e-9), "❌ Error in GovBond Risk Calculation"
    assert math.isclose(risk2, 0.6, rel_tol=1e-9), "❌ Error in CorpBond Risk Calculation"
    print("✅ Bond risk tests passed.")


if __name__ == "__main__":
    test_stock_risk()
    test_bond_risk()
    print("\n🎉 All Securities Risk Model Tests Passed Successfully!")
