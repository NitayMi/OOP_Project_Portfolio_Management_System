from controller import controller
from tabulate import tabulate
from colorama import Fore, Style
import matplotlib.pyplot as plt
from dbmodel import SecurityData, dbmodel
# שימוש בקונטרולר החדש
from controller import ControllerV2
from dbmodel import SqliteRepository
from ollamamodel import OllamaAIAdvisor

USE_NEW_CONTROLLER = True  # שנה ל-False כדי לעבוד עם ה-controller הישן


class view:
    def __init__(self):
        risk_level = input("Enter your risk level (Low / Medium / High): ").capitalize()
        # self.controller = controller(risk_level=risk_level)
        if USE_NEW_CONTROLLER:
            db = SqliteRepository()
            ai = OllamaAIAdvisor()
            self.controller = ControllerV2(risk_level=risk_level, db_repo=db, ai_advisor=ai)
        else:
            self.controller = controller(risk_level=risk_level)


    def show(self):
        while True:
            print(Fore.CYAN + """
            Menu
            ==========
            1. Buy
            2. Sell
            3. Get Advice
            4. Show Portfolio (Graph/Table)
            5. Exit
            """ + Style.RESET_ALL)

            choice = input("Enter your choice: ")

            if choice == "1":
                self.buy()
            elif choice == "2":
                self.sell()
            elif choice == "3":
                self.get_advice()
            elif choice == "4":
                self.show_portfolio()
            elif choice == "5":
                print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    def buy(self):
        print(Fore.BLUE + "\n📋 Available Securities to Buy:" + Style.RESET_ALL)
        securities = self.controller.get_available_securities()

        if not securities:
            print(Fore.RED + "❌ No available securities to buy." + Style.RESET_ALL)
            return

        # הצגת ניירות ערך
        for idx, sec in enumerate(securities, start=1):
            print(Fore.YELLOW + f"{idx}. {sec.name} ({sec.security_type}, {sec.subtype}, {sec.sector}, Variance: {sec.variance}, Price: {sec.basevalue})" + Style.RESET_ALL)

        # בחירת נייר ערך
        try:
            choice = int(input("\nChoose security number to buy: ")) - 1
            if choice < 0 or choice >= len(securities):
                print(Fore.RED + "❌ Invalid choice." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input." + Style.RESET_ALL)
            return

        # בחירת כמות
        try:
            amount = int(input("Enter amount to buy: "))
            if amount <= 0:
                print(Fore.RED + "❌ Amount must be positive." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input." + Style.RESET_ALL)
            return

        sec = securities[choice]

        # ביצוע קנייה
        success, message = self.controller.buy(
            name=sec.name,
            sector=sec.sector,
            variance=sec.variance,
            security_type=sec.security_type,
            subtype=sec.subtype,
            amount=amount,
            basevalue=sec.basevalue
        )

        # תוצאה למשתמש
        print(Fore.GREEN + message + Style.RESET_ALL if success else Fore.RED + message + Style.RESET_ALL)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def sell(self):
        print(Fore.BLUE + "\n📋 Your Portfolio:" + Style.RESET_ALL)
        portfolio = self.controller.get_portfolio_data()

        if not portfolio:
            print(Fore.RED + "❌ Your portfolio is empty." + Style.RESET_ALL)
            return

        # הצגת התיק
        for idx, sec in enumerate(portfolio, start=1):
            print(Fore.YELLOW + f"{idx}. {sec.name} | Amount: {sec.ammont} | Base Value: {sec.basevalue}" + Style.RESET_ALL)

        # בחירת נייר למכירה
        try:
            choice = int(input("\nChoose security number to sell: ")) - 1
            if choice < 0 or choice >= len(portfolio):
                print(Fore.RED + "❌ Invalid choice." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input." + Style.RESET_ALL)
            return

        sec = portfolio[choice]

        # כמות למכירה
        print(Fore.YELLOW + f"\nYou chose to sell '{sec.name}'. You own {sec.ammont} units." + Style.RESET_ALL)
        try:
            amount = int(input(f"Enter amount to sell (Available: {sec.ammont}): "))
            if amount <= 0:
                print(Fore.RED + "❌ Amount must be positive." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input." + Style.RESET_ALL)
            return

        # ביצוע מכירה
        success, message = self.controller.sell(
            name=sec.name,
            security_type=sec.security_type,
            sector=sec.sector,
            subtype=sec.subtype,
            amount=amount
        )

        # תוצאה למשתמש
        print(Fore.GREEN + message + Style.RESET_ALL if success else Fore.RED + message + Style.RESET_ALL)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)


    def get_advice(self):
        question = input("Enter your question for AI Advisor: ")
        self.controller.get_advice(question)
        answer = self.controller.get_advice(question)
        print(Fore.GREEN + f"\nAI Advisor says: {answer}" + Style.RESET_ALL)

        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def show_portfolio(self):
        data = self.controller.get_portfolio_data()
        if not data:
            print(Fore.RED + "Your portfolio is empty." + Style.RESET_ALL)
            return

        table = []
        for sec in data:
            risk = self.controller.get_individual_risk(sec)
            table.append([
                sec.name,
                sec.ammont,
                sec.basevalue,
                f"{risk:.2f}"
            ])

        print(Fore.YELLOW + "\nYour Portfolio (Table):" + Style.RESET_ALL)
        print(tabulate(table, headers=["Name", "Amount", "Base Value", "Risk"], tablefmt="pretty"))

        total_risk = self.controller.get_total_risk()
        print(Fore.YELLOW + f"\nTotal Portfolio Risk: {total_risk:.2f}" + Style.RESET_ALL)

        show_graph = input("\nDo you want to see a graph? (yes/no): ").lower()
        if show_graph == 'yes':
            self.display_graph(data)

        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

        graph_choice = input("Do you want to see a graph? (yes/no): ").strip().lower()
        if graph_choice == "yes":
            self.show_portfolio_graph()


    def display_graph(self, portfolio):
        names = [sec.name for sec in portfolio]
        amounts = [sec.ammont for sec in portfolio]

        plt.figure(figsize=(7, 7))
        plt.pie(amounts, labels=names, autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Distribution')
        plt.show()

    def show_portfolio_graph(self):
        portfolio = self.controller.get_portfolio_data()
        if not portfolio:
            print("❌ Your portfolio is empty.")
            return

        # סיכום נתוני התיק
        labels = [sec.name for sec in portfolio]
        sizes = [sec.basevalue * sec.ammont for sec in portfolio]

        # גרף פאי לפי שווי השקעה
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Distribution by Value')
        plt.axis('equal')  # עיגול
        plt.show()

        # גרף עמודות לפי סקטור
        sectors = {}
        for sec in portfolio:
            sectors[sec.sector] = sectors.get(sec.sector, 0) + (sec.basevalue * sec.ammont)

        plt.figure(figsize=(10, 6))
        plt.bar(sectors.keys(), sectors.values())
        plt.title('Portfolio Distribution by Sector')
        plt.xlabel('Sector')
        plt.ylabel('Total Value')
        plt.show()
