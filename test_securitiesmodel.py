# from securitiesmodel import Stock, Bond, Portfolio

# def test_stock():
#     print("\n--- Test: Stock ---")
#     stock1 = Stock(name="Tech Stock", sector="Technology", variance="High", preferred=False)
#     print("Stock Info:", stock1.get_info())

#     stock2 = Stock(name="Real Estate Preferred", sector="Real Estate", variance="Low", preferred=True)
#     print("Stock Info:", stock2.get_info())

# def test_bond():
#     print("\n--- Test: Bond ---")
#     bond1 = Bond(name="Government Bond", sector="Industry", variance="Low", government=True)
#     print("Bond Info:", bond1.get_info())

#     bond2 = Bond(name="Corporate Bond", sector="Finance", variance="High", government=False)
#     print("Bond Info:", bond2.get_info())

# def test_portfolio():
#     print("\n--- Test: Portfolio ---")
#     portfolio = Portfolio()
#     portfolio.add_security(Stock(name="Tech Stock", sector="Technology", variance="High"))
#     portfolio.add_security(Bond(name="Government Bond", sector="Industry", variance="Low"))
#     portfolio.add_security(Stock(name="Real Estate Stock", sector="Real Estate", variance="Low"))
    
#     portfolio.display_portfolio()
#     print("Total Portfolio Risk:", portfolio.calculate_total_risk())

# if __name__ == "__main__":
#     test_stock()
#     test_bond()
#     test_portfolio()

# טסט חדש 13.03





from dbmodel import dbmodel
from securitiesmodel import Portfolio

def test_portfolio():
    db = dbmodel()
    port = Portfolio(db)

    print("\n--- Current Portfolio ---")
    port.display_portfolio()

    total_risk = port.calculate_total_risk()
    print(f"Total Portfolio Risk: {total_risk:.2f}")

if __name__ == "__main__":
    test_portfolio()
