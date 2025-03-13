from dbmodel import dbmodel

def test_dbmodel():
    db = dbmodel()

    print("\n✅ Testing DB Operations")

    # 1. Clear existing data to start clean
    db.clear_portfolio()
    print("Portfolio cleared for tests.")

    # 2. Test Insert
    db.insert("TestStock", 10, 150.0, "stock", "Finance", "common")
    data = db.getdata()
    assert len(data) == 1, "Insert failed"
    print("Insert passed.")

    # 3. Test Update
    db.update_amount("TestStock", "stock", "Finance", "common", 5)
    data = db.getdata()
    assert list(data.values())[0]['ammont'] == 15, "Update failed"
    print("Update passed.")

    # 4. Test Find
    found = db.find_security("TestStock", "stock", "Finance", "common")
    assert found is not None, "Find failed"
    print("Find passed.")

    # 5. Test Delete
    db.delete("TestStock", "stock", "Finance", "common")
    data = db.getdata()
    assert len(data) == 0, "Delete failed"
    print("Delete passed.")

    print("\n✅ All DB tests passed successfully.\n")

if __name__ == "__main__":
    test_dbmodel()
