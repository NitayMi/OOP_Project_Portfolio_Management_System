import requests

# כתובת ה-API שלך (אל תשכח להפעיל uvicorn api:app --reload --workers 1)
API_BASE_URL = "http://127.0.0.1:8000"
# כתובת Ollama שמריץ deepseek
AI_API_URL = "http://127.0.0.1:11434/api/generate"

# שליפת תיק השקעות
def get_portfolio():
    response = requests.get(f"{API_BASE_URL}/portfolio")
    return response.json()

# שליפת סיכון כולל
def get_total_risk():
    response = requests.get(f"{API_BASE_URL}/risk")
    return response.json()

# שליחת שאלה ל-AI
def ask_ai(question, model="deepseek-r1:7b"):  # עדכון למודל שלך
    response = requests.post(
        AI_API_URL,
        json={
            "model": model,
            "prompt": question,
            "stream": False
        }
    )
    return response.json()

# ====== חיבור הכל ======
if __name__ == "__main__":
    print("🔄 Fetching portfolio...")
    portfolio = get_portfolio()
    print("🔄 Fetching total risk...")
    risk = get_total_risk()

    # בדיקת תקינות
    if not portfolio:
        print("❌ Portfolio is empty or error.")
        exit(1)
    if 'total_risk' not in risk:
        print("❌ Risk data error:", risk)
        exit(1)

    # ניסוח שאלה ל-AI
    question = f"""
I have this portfolio: {portfolio}.
The total risk is {risk['total_risk']}.
Based on this data, what would you advise me to do? Should I buy, sell, or hold my assets? Please explain with reasoning and possible risks.
    """

    print("🤖 Sending to AI for advice...\n")
    ai_response = ask_ai(question)
    print("========= AI Advisor Response =========")
    print(ai_response["response"])
