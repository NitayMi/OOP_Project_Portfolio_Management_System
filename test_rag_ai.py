from ollamamodel import AIAdvisorRAG
from dbmodel import SecurityData

# יוצרים אובייקט של ה-AI החדש
ai = AIAdvisorRAG()

# דוגמה לתיק השקעות פשוט (כולל basevalue)
portfolio = [
    SecurityData(id=1, name="Apple", ammont=10, sector="Technology", variance="Medium", security_type="stock", subtype="growth", basevalue=100),
    SecurityData(id=2, name="Tesla", ammont=5, sector="Automotive", variance="High", security_type="stock", subtype="growth", basevalue=100)
]

# שאלה לדוגמה
question = "What should I invest in next?"

# קריאה ל-AI
response = ai.get_advice(question, portfolio_data=portfolio)

# הדפסת התשובה
print("AI Response:", response)
