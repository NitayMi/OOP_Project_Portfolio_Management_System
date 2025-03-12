from controller import controller

# יצירת אינסטנס של הקונטרולר (שים לב, תבחר רמת סיכון כלשהי, זה חובה לפי הקוד שלך)
my_controller = controller(risk_level="Medium")  # אפשר גם "Low" או "High"

# קבלת רשימת ניירות הערך
securities = my_controller.get_available_securities()

# הדפסת הרשימה
print("\nAvailable Securities:")
for idx, sec in enumerate(securities, start=1):
    print(f"{idx}. {sec['name']} ({sec['type']}, {sec['sub_type']}, {sec['sector']}, Variance: {sec['variance']}, Price: {sec['basevalue']})")
