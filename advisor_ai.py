import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from datetime import datetime
import requests
import threading

# הגדרת כתובת ה-AI
AI_API_URL = "http://127.0.0.1:11434/api/generate"

# -------------------- פונקציה לניתוח תיק -------------------- #
def run_ai_advisor(portfolio, total_risk):
    try:
        print("📊 Portfolio sent to AI:", portfolio)
        print("⚠️ Total risk:", total_risk)

        # בניית תיאור התיק
        portfolio_description = "\n".join(
            [f"{item.name}, Amount: {item.ammont}, Base Value: {item.basevalue}, Sector: {item.sector}, Type: {item.security_type}, Risk: {item.variance}" for item in portfolio]
        )

        # ניסוח שאלה חכמה
        question = (
            f"My portfolio:\n{portfolio_description}\n"
            f"Total risk: {total_risk:.2f}\n\n"
            f"Please analyze this portfolio."
        )

        print("🧠 Question to AI:", question)

        # שליחה ל-AI
        response = requests.post(AI_API_URL, json={
            "model": "deepseek-r1:7b",
            "prompt": question,
            "stream": False
        }).json()

        # הצגה ושמירה
        save_response_to_file(response['response'])
        show_ai_response(response['response'])

    except Exception as e:
        print(f"❌ AI Error: {e}")
        messagebox.showerror("AI Error", f"Failed to get AI advice: {e}")


# -------------------- פונקציה לשאלה חופשית -------------------- #
def ask_custom_question():
    # קודם לקבל את השאלה מהמשתמש
    question = simpledialog.askstring("Ask AI", "What would you like to ask?")

    if question:
        # שליחה ל-AI ב-thread נפרד
        threading.Thread(target=lambda: send_question_to_ai(question)).start()


# שליחת שאלה חופשית ל-AI
def send_question_to_ai(question):
    try:
        # ניסוח פקודה קשוחה
        question = (
            f"{question}\n\n"
            f"ANSWER STRICT FORMAT: ANSWER: <your short answer here>. NOTHING ELSE.\n"
            f"Return ONLY short answer.\n"
            f"Do NOT explain, do NOT say 'sure', do NOT analyze. Just answer directly."
        )

        print("🟡 Sending free question to AI:", question)
        response = requests.post(AI_API_URL, json={
            "model": "deepseek-r1:7b",
            "prompt": question,
            "stream": False
        })

        print("🟡 AI Raw Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            save_response_to_file(data['response'])
            show_ai_response(data['response'])
        else:
            raise Exception(f"AI returned status code {response.status_code}")

    except Exception as e:
        print(f"❌ AI Free Question Error: {e}")
        tk.Tk().after(0, lambda: messagebox.showerror("AI Error", f"Failed to get AI response. Please check AI connection. Error: {e}"))


# -------------------- הצגת תשובה בפופאפ -------------------- #
def show_ai_response(response):
    popup = tk.Toplevel()
    popup.title("AI Response")
    text = scrolledtext.ScrolledText(popup, wrap='word', font='Sans 12')
    text.insert('1.0', response)
    text.pack(expand=True, fill='both')


# -------------------- שמירת תשובה לקובץ -------------------- #
def save_response_to_file(response):
    with open("ai_advisor_history.log", "a", encoding="utf-8") as file:
        file.write(f"\n[{datetime.now()}]\n{response}\n{'-'*50}\n")



# פונקציה שיוצרת את ה-prompt לניתוח התיק
def generate_portfolio_prompt(portfolio, total_risk):
    portfolio_description = "\n".join(
        [f"{item.name}, Amount: {item.ammont}, Base Value: {item.basevalue}, Sector: {item.sector}, Type: {item.security_type}, Risk: {item.variance}" for item in portfolio]
    )
    question = (
        f"My portfolio:\n{portfolio_description}\n"
        f"Total risk: {total_risk:.2f}\n\n"
        f"Please analyze this portfolio"
    )
    return question
