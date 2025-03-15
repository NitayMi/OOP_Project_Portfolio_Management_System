
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkbootstrap import Style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
from controller import controller


class PortfolioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = Style(theme='flatly')  # Light modern theme
        self.title("Portfolio Management System")
        self.geometry("1200x800")
        self.option_add("*Font", "Sans 12")  # Set modern readable font

        self.ask_risk_level()

    def ask_risk_level(self):
        popup = tk.Toplevel(self)
        popup.title("Select Risk Level")
        popup.geometry("300x150")
        tk.Label(popup, text="Select your risk level:", font="Sans 14").pack(pady=10)

        def set_risk(level):
            self.risk_level = level
            popup.destroy()
            self.start_main_ui()

        ttk.Button(popup, text="Low", command=lambda: set_risk("Low")).pack(pady=5, fill='x')
        ttk.Button(popup, text="Medium", command=lambda: set_risk("Medium")).pack(pady=5, fill='x')
        ttk.Button(popup, text="High", command=lambda: set_risk("High")).pack(pady=5, fill='x')

    def start_main_ui(self):
        self.controller = controller(self.risk_level)
        self.create_summary()
        self.create_tabs()
        self.refresh_all()

    def create_summary(self):
        self.summary_frame = ttk.Frame(self)
        self.summary_frame.pack(fill='x', pady=10)

        self.total_value_label = ttk.Label(self.summary_frame, text="Total Value: Calculating...")
        self.total_value_label.pack(side='left', padx=10)

        self.total_risk_label = ttk.Label(self.summary_frame, text="Total Risk: Calculating...")
        self.total_risk_label.pack(side='left', padx=10)

        ttk.Button(self.summary_frame, text="Ask AI Advisor", command=self.ask_ai_advisor).pack(side='right', padx=10)

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
        question = simpledialog.askstring("AI Advisor", "What would you like to ask?")
        if question:
            threading.Thread(target=self.process_ai_advice, args=(question,)).start()

    def process_ai_advice(self, question):
        answer = self.controller.get_advice(question)
        popup = tk.Toplevel(self)
        popup.title("AI Advisor Response")
        text = tk.Text(popup, wrap='word')
        text.insert('1.0', answer)
        text.pack(expand=True, fill='both')


if __name__ == "__main__":
    app = PortfolioApp()
    app.mainloop()
