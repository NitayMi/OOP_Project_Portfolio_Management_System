import tkinter as tk
from tkinter import simpledialog, messagebox
from controller import controller
from dbmodel import dbmodel


class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Manager")
        self.root.geometry("600x400")  # Set window size

        # DB + Controller connection
        self.db = dbmodel()

        # Step 1: Ask for risk level and initialize controller
        self.risk_level = simpledialog.askstring("Risk Level", "Enter your risk level (Low/Medium/High):").capitalize()
        self.controller = controller(risk_level=self.risk_level)

        # Display risk level at the top
        self.risk_label = tk.Label(
            root,
            text=f"Risk Level: {self.risk_level}",
            font=("Arial", 14, "bold"),
            fg='blue'
        )
        self.risk_label.pack(pady=20)

        # Title
        self.title_label = tk.Label(
            root,
            text="Portfolio Management System",
            font=("Arial", 16, "bold"),
            fg='green'
        )
        self.title_label.pack(pady=10)

        # Action Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Buy Security", command=self.buy_security, width=15, height=2).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Sell Security", command=self.sell_security, width=15, height=2).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Show Portfolio", command=self.show_portfolio, width=15, height=2).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="AI Advice", command=self.get_advice, width=15, height=2).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Exit", command=root.quit, width=15, height=2, bg='red', fg='white').grid(row=2, column=0, columnspan=2, pady=10)

        # Footer (placeholder for future risk updates)
        self.footer_label = tk.Label(root, text="System Ready...", font=("Arial", 10), fg='gray')
        self.footer_label.pack(side=tk.BOTTOM, pady=10)

    # Placeholder methods (to be implemented in next steps)
    def buy_security(self):
        messagebox.showinfo("Coming Soon", "Buy Security Functionality will be implemented in Step 2.")

    def sell_security(self):
        messagebox.showinfo("Coming Soon", "Sell Security Functionality will be implemented in Step 3.")

    def show_portfolio(self):
        messagebox.showinfo("Coming Soon", "Show Portfolio Functionality will be implemented in Step 4.")

    def get_advice(self):
        messagebox.showinfo("Coming Soon", "AI Advice Functionality will be implemented in Step 5.")


# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()
