import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import requests

AI_API_URL = "http://127.0.0.1:11434/api/generate"

# הפונקציה שמקבלת את התיק והסיכון ושולחת ל-AI
def run_ai_advisor(portfolio, total_risk):
    try:
        print("📊 Portfolio sent to AI:", portfolio)  # לבדוק מה נשלח
        print("⚠️ Total risk:", total_risk)

        # הכנת התיק בצורת טקסט
        portfolio_description = "\n".join(
            [f"{item.name}, Amount: {item.ammont}, Base Value: {item.basevalue}, Sector: {item.sector}, Type: {item.security_type}, Risk: {item.variance}" for item in portfolio]
        )

        # ניסוח שאלה חזקה שמכריחה אותו לענות קצר
        question = (
            f"My portfolio:\n{portfolio_description}\n"
            f"Total risk: {total_risk:.2f}\n\n"
            f"Please analyze this portfolio and give me ONLY 5 very short bullet points. "
            f"Each point should be 1 simple sentence. "
            f"Do NOT explain. Do NOT elaborate. "
            f"Be extremely concise and straight to the point."
        )

        print("🧠 Question to AI:", question)  # לבדוק מה נשלח בפועל

        # שליחה ל-AI **בלי חיתוך קשוח** (כדי לא לחתוך באמצע)
        response = requests.post(AI_API_URL, json={
            "model": "deepseek-r1:7b",
            "prompt": question,
            "stream": False,
            "options": {
            }
        }).json()

        save_response_to_file(response['response'])
        show_ai_response(response['response'])

    except Exception as e:
        print(f"❌ AI Error: {e}")  # אם יש שגיאה
        messagebox.showerror("AI Error", f"Failed to get AI advice: {e}")


# שמירת תשובה לקובץ
def save_response_to_file(response):
    with open("ai_advisor_history.log", "a", encoding="utf-8") as file:
        file.write(f"\n[{datetime.now()}]\n{response}\n{'-'*50}\n")


# הצגת התשובה בפופאפ
def show_ai_response(response):
    popup = tk.Toplevel()
    popup.title("AI Advisor Response")
    text = scrolledtext.ScrolledText(popup, wrap='word', font='Sans 12')
    text.insert('1.0', response)
    text.pack(expand=True, fill='both')


# שאלה חופשית (לפי השאלה שלך):
def ask_custom_question():
    try:
        question = simpledialog.askstring("Ask AI", "What would you like to ask?")
        if question:
            response = requests.post(AI_API_URL, json={
                "model": "deepseek-r1:7b",
                "prompt": question,
                "stream": False
            }).json()

            save_response_to_file(response['response'])
            show_ai_response(response['response'])

    except Exception as e:
        messagebox.showerror("AI Error", f"Failed to get AI response: {e}")
