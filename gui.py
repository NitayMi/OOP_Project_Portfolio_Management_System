import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkbootstrap import Style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

# שימוש בקונטרולר החדש
from dbmodel import SqliteRepository
from ollamamodel import AIAdvisorRAG as OllamaAIAdvisor
from controller import ControllerV2


USE_NEW_CONTROLLER = True  # שנה ל-False כדי לעבוד עם ה-controller הישן


# AI Advisor Import (with safe fallback if file not exists)
try:
    from advisor_ai import run_ai_advisor, ask_custom_question
except ImportError:
    from tkinter import messagebox
    def run_ai_advisor():
        messagebox.showinfo("AI", "AI Advisor is not available.")
    def ask_custom_question():
        messagebox.showinfo("AI", "AI Advisor is not available.")

class PortfolioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = Style(theme='flatly')  # Light modern theme
        self.title("Portfolio Management System")
        self.geometry("1200x800")
        self.option_add("*Font", "Sans 12")  # Set modern readable font

        self.ask_risk_level()

    def ask_risk_level(self):
        self.risk_frame = ttk.Frame(self)
        self.risk_frame.pack(expand=True, fill='both')

        ttk.Label(self.risk_frame, text="Select your risk level:", font="Sans 16").pack(pady=30)

        button_frame = ttk.Frame(self.risk_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Low", command=lambda: self.set_risk("Low"), width=20).pack(pady=10)
        ttk.Button(button_frame, text="Medium", command=lambda: self.set_risk("Medium"), width=20).pack(pady=10)
        ttk.Button(button_frame, text="High", command=lambda: self.set_risk("High"), width=20).pack(pady=10)

    def set_risk(self, level):
        self.risk_level = level
        self.risk_frame.destroy()  # מוחק את ה-frame של בחירת סיכון
        self.start_main_ui()  # ממשיך לממשק המלא

    def start_main_ui(self):
        self.controller = None
        if USE_NEW_CONTROLLER:
            db = SqliteRepository()
            ai = OllamaAIAdvisor()
            self.controller = ControllerV2(risk_level=self.risk_level, db_repo=db, ai_advisor=ai)
        else:
            self.controller = ControllerV2(risk_level=self.risk_level, db_repo=SqliteRepository(), ai_advisor=OllamaAIAdvisor())

        self.create_summary()
        self.create_tabs()
        self.refresh_all()

    def create_summary(self):
        """יוצר את החלק העליון של הממשק עם סיכום התיק והכפתורים הראשיים."""
        self.summary_frame = ttk.Frame(self)
        self.summary_frame.pack(fill='x', pady=10)

        # תוויות להצגת ערכי הסיכון והערך הכולל
        self.total_value_label = ttk.Label(self.summary_frame, text="Total Value: Calculating...")
        self.total_value_label.pack(side='left', padx=10)

        self.total_risk_label = ttk.Label(self.summary_frame, text="Total Risk: Calculating...")
        self.total_risk_label.pack(side='left', padx=10)

        # 🔹 אתחול נכון של status_label למניעת שגיאות בגישה אליו בהמשך
        self.status_label = ttk.Label(self.summary_frame, text="")  # יצירת תווית סטטוס
        self.status_label.pack(side='left', padx=10)

        # כפתור ייעוץ AI לתיק
        ttk.Button(self.summary_frame, text="AI Portfolio Analysis", command=self.ask_ai_advisor).pack(side='right', padx=10)

        # כפתור לשאלות חופשיות ל-AI
        ttk.Button(self.summary_frame, text="Ask AI (Free Question)", command=self.ask_ai_free).pack(side='right', padx=10)

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self)
        self.portfolio_tab = ttk.Frame(self.tab_control)
        self.buy_tab = ttk.Frame(self.tab_control)
        self.graph_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.portfolio_tab, text='Portfolio')
        self.tab_control.add(self.buy_tab, text='Buy Securities')
        self.tab_control.add(self.graph_tab, text='Portfolio Graphs')
        self.tab_control.pack(expand=1, fill='both')

        self.create_portfolio_tab()
        self.create_buy_tab()
        self.create_graph_tab()

    def create_portfolio_tab(self):
        self.tree = ttk.Treeview(self.portfolio_tab, columns=("Name", "Amount", "Base Value", "Sector", "Type", "Risk", "Value"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both')
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def create_buy_tab(self):
        self.buy_tree = ttk.Treeview(self.buy_tab, columns=("Name", "Sector", "Risk", "Base Value", "Type"), show='headings')
        for col in self.buy_tree["columns"]:
            self.buy_tree.heading(col, text=col)
        self.buy_tree.pack(expand=True, fill='both')
        self.buy_tree.bind("<Double-1>", self.on_buy_double_click)

    def create_graph_tab(self):
        self.graph_canvas = None

    def refresh_all(self):
        self.load_portfolio()
        self.load_buy_options()
        self.update_summary()
        self.refresh_graph()

    def load_portfolio(self):
        self.tree.delete(*self.tree.get_children())
        self.portfolio_securities = self.controller.get_portfolio_data()
        self.total_value = 0
        for item in self.portfolio_securities:
            individual_risk = self.controller.get_individual_risk(item)
            value = item.basevalue * item.ammont
            self.total_value += value
            self.tree.insert('', 'end', values=(item.name, item.ammont, item.basevalue, item.sector, item.security_type, f"{individual_risk:.2f}", f"{value:.2f}"))

    def load_buy_options(self):
        self.buy_tree.delete(*self.buy_tree.get_children())
        self.available_securities = self.controller.get_available_securities()
        for sec in self.available_securities:
            self.buy_tree.insert('', 'end', values=(sec.name, sec.sector, sec.variance, sec.basevalue, sec.security_type))

    def update_summary(self):
        risk = self.controller.get_total_risk()
        self.total_risk_label.config(text=f"Total Risk: {risk:.2f}")
        self.total_value_label.config(text=f"Total Value: {self.total_value:.2f}")

    def refresh_graph(self):
        if self.graph_canvas:
            self.graph_canvas.get_tk_widget().destroy()

        names = [item.name for item in self.portfolio_securities]
        amounts = [item.ammont for item in self.portfolio_securities]

        fig, axs = plt.subplots(1, 2, figsize=(14, 6))
        axs[0].pie(amounts, labels=names, autopct='%1.1f%%')
        axs[0].set_title('Pie Chart')

        axs[1].bar(names, amounts)
        axs[1].set_title('Bar Chart')

        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_tab)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(expand=True, fill='both')

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()[0]
        name = self.tree.item(selected_item, "values")[0]
        self.open_sell_popup(name)

    def on_buy_double_click(self, event):
        selected_item = self.buy_tree.selection()[0]
        name = self.buy_tree.item(selected_item, "values")[0]
        self.open_buy_popup(name)

    def open_sell_popup(self, name):
        popup = tk.Toplevel(self)
        popup.title(f"Sell {name}")
        popup.geometry("300x250")

        # Retrieve the security from portfolio to get the amount
        sec = next((s for s in self.portfolio_securities if s.name == name), None)

        tk.Label(popup, text=f"Sell {name}", font="Sans 14").pack(pady=10)
        tk.Label(popup, text=f"Amount available: {sec.ammont}").pack(pady=5)

        tk.Label(popup, text="Amount to Sell:").pack()
        amount_entry = ttk.Entry(popup)
        amount_entry.pack(pady=5)

        def confirm_sell():
            amount = int(amount_entry.get())
            success, message = self.controller.sell(sec.name, sec.security_type, sec.sector, sec.subtype, amount)
            messagebox.showinfo("Result", message)
            popup.destroy()
            self.refresh_all()

        def sell_all():
            amount = sec.ammont
            success, message = self.controller.sell(sec.name, sec.security_type, sec.sector, sec.subtype, amount)
            messagebox.showinfo("Result", message)
            popup.destroy()
            self.refresh_all()

        ttk.Button(popup, text="Confirm Sell", command=confirm_sell).pack(pady=10, fill='x')
        ttk.Button(popup, text="Sell All", command=sell_all).pack(pady=5, fill='x')  # כפתור חדש למכירה מלאה


    def open_buy_popup(self, name):
        popup = tk.Toplevel(self)
        popup.title(f"Buy {name}")
        popup.geometry("300x200")

        tk.Label(popup, text=f"Buy {name}").pack(pady=10)
        tk.Label(popup, text="Amount to Buy:").pack()
        amount_entry = ttk.Entry(popup)
        amount_entry.pack(pady=5)

        def confirm_buy():
            amount = int(amount_entry.get())
            sec = next((s for s in self.available_securities if s.name == name), None)
            if sec:
                success, message = self.controller.buy(sec.name, sec.sector, sec.variance, sec.security_type, sec.subtype, amount, sec.basevalue)
                messagebox.showinfo("Result", message)
                popup.destroy()
                self.refresh_all()

        ttk.Button(popup, text="Confirm Buy", command=confirm_buy).pack(pady=10)

    def ask_ai_advisor(self):
        """ מבקש ייעוץ AI תוך מניעת קריאות כפולות ועדכון סטטוס UI """
        
        if hasattr(self, "ai_processing") and self.ai_processing:
            return  # מונע קריאה כפולה בזמן שה-AI כבר מעבד מידע

        self.ai_processing = True  # מסמן שה-AI בתהליך עבודה
        self.status_label.config(text="⏳ AI is processing...")  # הצגת חיווי למשתמש

        # שולף את הנתונים הדרושים לפונקציה כדי למנוע TypeError
        portfolio = self.controller.get_portfolio_data()
        total_risk = self.controller.get_total_risk()
        question = "What should I invest in next based on my current portfolio and risk level?"

        def worker():
            try:
                answer = self.controller.get_advice(question, portfolio, total_risk)  # קריאה עם הנתונים הנכונים
            except Exception as e:
                answer = f"⚠️ AI Error: {str(e)}"  # במקרה של שגיאה, החזר תשובה מתאימה

            # עדכון ה-UI חייב להיעשות מתוך ה-Thread הראשי
            self.after(0, lambda: self.show_ai_response(answer))  # הצגת התוצאה
            self.after(0, lambda: self.status_label.config(text="✅ AI Response Ready"))  # עדכון סטטוס
            self.after(0, lambda: setattr(self, "ai_processing", False))  # משחרר את היכולת לקרוא שוב

        threading.Thread(target=worker, daemon=True).start()

    def run_ai(self, question):
        """ מפעיל את ה-AI בצורה אסינכרונית עם חיווי מצב """
        
        self.status_label.config(text="⏳ AI is processing...")  # הצגת חיווי שה-AI עובד

        def worker():
            db = SqliteRepository()  # יצירת חיבור חדש למסד הנתונים (נדרש לכל Thread)
            portfolio = db.get_portfolio_data()  # טעינת התיק מהמסד בתוך ה-Thread הנכון
            total_risk = self.controller.get_total_risk()

            answer = self.controller.get_advice(question)  # קריאת התשובה מה-AI
            
            # עדכון ה-UI חייב להיעשות מתוך ה-Thread הראשי
            self.after(0, lambda: self.show_ai_response(answer))  # הצגת התוצאה
            self.after(0, lambda: self.status_label.config(text="✅ AI Response Ready"))  # עדכון סטטוס

        threading.Thread(target=worker, daemon=True).start()

    def show_ai_response(self, answer):
        """
        הצגת התשובה של ה-AI בחלון נגלל.
        """
        popup = tk.Toplevel(self)
        popup.title("AI Advisor Response")
        
        text = tk.Text(popup, wrap='word', height=15, width=80)
        text.insert('1.0', answer)
        text.pack(expand=True, fill='both')

        scrollbar = ttk.Scrollbar(popup, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)

    def ask_ai_free(self):
        """ פותח דיאלוג להזנת שאלה ושולח אותה ל-AI """
        def get_user_question():
            question = simpledialog.askstring("Ask AI", "What would you like to ask?")
            if question:  # אם המשתמש הזין שאלה, שולחים אותה ל-AI
                self.process_ai_question(question)
            else:
                messagebox.showinfo("AI", "No question entered.")

        self.after(0, get_user_question)  # מבצע את הפעולה מתוך ה-Thread הראשי

# עובד טוב בלי לשאול אם להתייחס לנתונים שולח דיםולטיבי
    # def process_ai_question(self, question):
    #     """ שולח את השאלה ל-AI, מציג סטטוס ומביא את התשובה חזרה ל-UI """
    #     self.status_label.config(text="⏳ AI is processing...")  # עדכון חיווי למשתמש

    #     def worker():
    #         try:
    #             # שליפת הנתונים שה-AI זקוק להם
    #             portfolio = self.controller.get_portfolio_data()  
    #             total_risk = self.controller.get_total_risk()
                
    #             # שליחת השאלה ל-AI עם כל הנתונים הנדרשים
    #             answer = self.controller.get_advice(question, portfolio, total_risk)  

    #             if not answer:
    #                 answer = "⚠️ AI did not return a response."
    #         except Exception as e:
    #             answer = f"⚠️ AI Error: {str(e)}"

    #         # עדכון ה-UI חייב להתבצע מה-Thread הראשי
    #         self.after(0, lambda: self.show_ai_response(answer))
    #         self.after(0, lambda: self.status_label.config(text="✅ AI Response Ready"))

    #     threading.Thread(target=worker, daemon=True).start()

# שואל אם להתייחס לנתונים בתיק ועובד טוב
    def process_ai_question(self, question):
        """
        שולח את השאלה ל-AI, עם או בלי נתוני התיק, לפי בחירת המשתמש.
        """
        use_portfolio = messagebox.askyesno("AI Question", "Do you want to include your portfolio data in the AI response?")

        self.status_label.config(text="⏳ AI is processing...")  # עדכון חיווי למשתמש

        def worker():
            try:
                if use_portfolio:
                    portfolio = self.controller.get_portfolio_data()
                    total_risk = self.controller.get_total_risk()
                    answer = self.controller.get_advice(question, portfolio, total_risk)  # קריאה עם נתונים
                else:
                    answer = self.controller.get_advice(question, [], 0)  # במקום להשאיר ריק, נעביר רשימה ריקה ו-0 כדי למנוע שגיאה

                if not answer:
                    answer = "⚠️ AI did not return a response."
            except TypeError as e:
                answer = f"⚠️ AI Error: {str(e)}\nCheck if `get_advice` supports questions without portfolio data."
            except Exception as e:
                answer = f"⚠️ AI Error: {str(e)}"

            # עדכון ה-UI חייב להתבצע מה-Thread הראשי
            self.after(0, lambda: self.show_ai_response(answer))
            self.after(0, lambda: self.status_label.config(text="✅ AI Response Ready"))

        threading.Thread(target=worker, daemon=True).start()



if __name__ == "__main__":
    app = PortfolioApp()
    app.mainloop()

