import tkinter as tk
from tkinter import messagebox, simpledialog
from matplotlib import pyplot as plt
from controller import controller


class PortfolioGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Portfolio Manager")
        self.controller = None  # נגדיר אחרי בחירת סיכון
        self.create_risk_selection_window()

    def create_risk_selection_window(self):
        risk_window = tk.Toplevel(self.root)
        risk_window.title("Select Risk Level")
        tk.Label(risk_window, text="Select your risk level:").pack(pady=10)

        for risk in ["Low", "Medium", "High"]:
            tk.Button(risk_window, text=risk, command=lambda r=risk: self.set_risk_level(r, risk_window)).pack(pady=5)

    def set_risk_level(self, risk, window):
        self.controller = controller(risk)
        window.destroy()
        self.create_main_menu()

    def create_main_menu(self):
        tk.Label(self.root, text="Portfolio Manager", font=("Arial", 18)).pack(pady=10)
        tk.Button(self.root, text="Show Portfolio", width=30, command=self.show_portfolio).pack(pady=5)
        tk.Button(self.root, text="Buy Security", width=30, command=self.buy_security).pack(pady=5)
        tk.Button(self.root, text="Sell Security", width=30, command=self.sell_security).pack(pady=5)
        tk.Button(self.root, text="Get AI Advice", width=30, command=self.get_advice).pack(pady=5)
        tk.Button(self.root, text="Show Portfolio Graph", width=30, command=self.show_graph).pack(pady=5)
        tk.Button(self.root, text="Exit", width=30, command=self.root.quit).pack(pady=20)

    def show_portfolio(self):
        portfolio = self.controller.get_portfolio_data()
        if not portfolio:
            messagebox.showinfo("Portfolio", "Your portfolio is empty.")
            return
        portfolio_str = "\n".join(
            [f"{sec.name} | Amount: {sec.ammont} | Base Value: {sec.basevalue} | Risk: {self.controller.get_individual_risk(sec):.2f}" for sec in portfolio]
        )
        total_risk = self.controller.get_total_risk()
        messagebox.showinfo("Portfolio", f"{portfolio_str}\n\nTotal Risk: {total_risk:.2f}")

    def buy_security(self):
        securities = self.controller.get_available_securities()
        sec_list = "\n".join([f"{i+1}. {sec.name} ({sec.security_type}, {sec.subtype}, {sec.sector}, Variance: {sec.variance}, Price: {sec.basevalue})" for i, sec in enumerate(securities)])
        choice = simpledialog.askinteger("Buy Security", f"Choose security number:\n{sec_list}")
        if not choice or choice < 1 or choice > len(securities):
            messagebox.showerror("Error", "Invalid choice.")
            return
        amount = simpledialog.askinteger("Buy Amount", "Enter amount to buy:")
        if not amount or amount <= 0:
            messagebox.showerror("Error", "Invalid amount.")
            return

        sec = securities[choice - 1]
        success, message = self.controller.buy(
            name=sec.name, sector=sec.sector, variance=sec.variance,
            security_type=sec.security_type, subtype=sec.subtype,
            amount=amount, basevalue=sec.basevalue
        )
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Failed", message)

    def sell_security(self):
        portfolio = self.controller.get_portfolio_data()
        if not portfolio:
            messagebox.showinfo("Portfolio", "Your portfolio is empty.")
            return
        sec_list = "\n".join([f"{i+1}. {sec.name} | Amount: {sec.ammont}" for i, sec in enumerate(portfolio)])
        choice = simpledialog.askinteger("Sell Security", f"Choose security number:\n{sec_list}")
        if not choice or choice < 1 or choice > len(portfolio):
            messagebox.showerror("Error", "Invalid choice.")
            return
        sec = portfolio[choice - 1]
        amount = simpledialog.askinteger("Sell Amount", f"Enter amount to sell (Available: {sec.ammont}):")
        if not amount or amount <= 0 or amount > sec.ammont:
            messagebox.showerror("Error", "Invalid amount.")
            return

        # מכירה דרך קונטרולר
        success, message = self.controller.sell(sec.name, amount)

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Failed", message)

    def get_advice(self):
        question = simpledialog.askstring("AI Advisor", "Enter your question for AI:")
        if not question:
            return
        advice = self.controller.ask_ai(question)
        messagebox.showinfo("AI Advice", advice)

    def show_graph(self):
        portfolio = self.controller.get_portfolio_data()
        if not portfolio:
            messagebox.showinfo("Portfolio", "Your portfolio is empty.")
            return
        labels = [sec.name for sec in portfolio]
        sizes = [sec.ammont * sec.basevalue for sec in portfolio]

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Portfolio Distribution')
        plt.show()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PortfolioGUI()
    app.run()
