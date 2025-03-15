import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from controller import controller


class PortfolioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Portfolio Management System")
        self.geometry("900x600")

        # שאלת רמת סיכון בהתחלה
        self.risk_level = simpledialog.askstring("Risk Level", "Enter your risk level (Low, Medium, High):", initialvalue="Medium")
        if self.risk_level not in ["Low", "Medium", "High"]:
            messagebox.showerror("Error", "Invalid risk level! Defaulting to 'Medium'.")
            self.risk_level = "Medium"

        self.controller = controller(self.risk_level)

        # טאבים
        self.tab_control = ttk.Notebook(self)
        self.portfolio_tab = ttk.Frame(self.tab_control)
        self.buy_tab = ttk.Frame(self.tab_control)
        self.sell_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.portfolio_tab, text='Portfolio')
        self.tab_control.add(self.buy_tab, text='Buy')
        self.tab_control.add(self.sell_tab, text='Sell')
        self.tab_control.pack(expand=1, fill='both')

        self.create_portfolio_tab()
        self.create_buy_tab()
        self.create_sell_tab()

    # ========================= Portfolio Tab ===========================
    def create_portfolio_tab(self):
        self.tree = ttk.Treeview(self.portfolio_tab, columns=("Name", "Base Value", "Amount", "Sector", "Type"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill='both')

        btn_refresh = ttk.Button(self.portfolio_tab, text="Refresh Portfolio", command=self.load_portfolio)
        btn_refresh.pack(pady=5)

        btn_graph = ttk.Button(self.portfolio_tab, text="Show Graph", command=self.show_graph)
        btn_graph.pack(pady=5)

        btn_risk = ttk.Button(self.portfolio_tab, text="Show Total Risk", command=self.show_total_risk)
        btn_risk.pack(pady=5)

    def load_portfolio(self):
        self.tree.delete(*self.tree.get_children())
        self.portfolio_securities = self.controller.get_portfolio_data()
        for item in self.portfolio_securities:
            self.tree.insert('', 'end', values=(item.name, item.basevalue, item.ammont, item.sector, item.security_type))

    def show_graph(self):
        if not hasattr(self, 'portfolio_securities'):
            self.load_portfolio()
        names = [item.name for item in self.portfolio_securities]
        amounts = [item.ammont for item in self.portfolio_securities]

        fig, ax = plt.subplots()
        ax.pie(amounts, labels=names, autopct='%1.1f%%')
        ax.set_title('Portfolio Distribution')

        canvas = FigureCanvasTkAgg(fig, master=self.portfolio_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def show_total_risk(self):
        risk = self.controller.get_total_risk()
        messagebox.showinfo("Total Risk", f"Total portfolio risk: {risk:.2f}")

    # ========================= Buy Tab with Buttons ===========================
    def create_buy_tab(self):
        self.available_securities = self.controller.get_available_securities()
        self.buy_selected_security = tk.StringVar()
        securities_names = [sec.name for sec in self.available_securities]
        dropdown = ttk.Combobox(self.buy_tab, textvariable=self.buy_selected_security, values=securities_names, state='readonly')
        dropdown.pack(pady=10, fill='x')

        # Amount Entry
        row_amount = ttk.Frame(self.buy_tab)
        label_amount = ttk.Label(row_amount, text="Amount to Buy: ")
        self.buy_amount_entry = ttk.Entry(row_amount)
        row_amount.pack(fill='x', pady=5)
        label_amount.pack(side='left')
        self.buy_amount_entry.pack(side='right', expand=True, fill='x')

        # Button to Buy
        btn_buy = ttk.Button(self.buy_tab, text="Buy Security", command=self.buy_security)
        btn_buy.pack(pady=20)

    def buy_security(self):
        try:
            selected_name = self.buy_selected_security.get()
            amount = int(self.buy_amount_entry.get())

            sec = next((s for s in self.available_securities if s.name == selected_name), None)
            if not sec:
                messagebox.showerror("Error", "Security not found.")
                return

            success, message = self.controller.buy(
                sec.name, sec.sector, sec.variance, sec.security_type,
                sec.subtype, amount, sec.basevalue
            )
            messagebox.showinfo("Result", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ========================= Sell Tab with Buttons ===========================
    def create_sell_tab(self):
        self.load_portfolio()  # Load portfolio when opening the tab
        self.sell_selected_security = tk.StringVar()
        securities_names = [sec.name for sec in self.portfolio_securities]
        dropdown = ttk.Combobox(self.sell_tab, textvariable=self.sell_selected_security, values=securities_names, state='readonly')
        dropdown.pack(pady=10, fill='x')

        # Amount Entry
        row_amount = ttk.Frame(self.sell_tab)
        label_amount = ttk.Label(row_amount, text="Amount to Sell: ")
        self.sell_amount_entry = ttk.Entry(row_amount)
        row_amount.pack(fill='x', pady=5)
        label_amount.pack(side='left')
        self.sell_amount_entry.pack(side='right', expand=True, fill='x')

        # Button to Sell
        btn_sell = ttk.Button(self.sell_tab, text="Sell Security", command=self.sell_security)
        btn_sell.pack(pady=20)

    def sell_security(self):
        try:
            selected_name = self.sell_selected_security.get()
            amount = int(self.sell_amount_entry.get())

            sec = next((s for s in self.portfolio_securities if s.name == selected_name), None)
            if not sec:
                messagebox.showerror("Error", "Security not found in portfolio.")
                return

            success, message = self.controller.sell(
                sec.name, sec.security_type, sec.sector, sec.subtype, amount
            )
            messagebox.showinfo("Result", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = PortfolioApp()
    app.mainloop()
