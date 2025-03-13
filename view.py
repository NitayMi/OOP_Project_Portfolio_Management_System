# from colorama import Fore, Style
# from controller import controller
# from dbmodel import dbmodel
# import os
# import seaborn as sns
# import matplotlib.pyplot as plt
# from tabulate import tabulate


# class view:    
#     def __init__(self):
#         self.controller=controller()
#         self.db=dbmodel()
        
#     def displaygraph(self):        
#         dictanswer=self.db.getdata()
#        # Create a pie chart
#         labels = [dictanswer[key]['name'] for key in dictanswer]
#         sizes = [dictanswer[key]['ammont'] for key in dictanswer]

#         plt.figure(figsize=(10, 6))
#         plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
#         plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#         plt.title('Investment Distribution')
#         plt.show()
            
#     def dispalytable(self):
#         data=self.db.getdata()  
        
#         # Convert dictionary to list of lists for tabulate
#         table_data = [[k] + list(v.values()) for k, v in data.items()]

#         # Define headers
#         headers = ["Key", "ID", "Name", "Base Value", "Amount"]

#         # Print table
#         print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
#         input("Press Enter to continue...")
  
    
#     def print_menu(self):
#             os.system('cls' if os.name == 'nt' else 'clear')
#             print(Fore.CYAN + "   Menu   " + Style.RESET_ALL)
#             print(Fore.CYAN + "==========" + Style.RESET_ALL)
            
#             print(Fore.GREEN + "1. Buy" + Style.RESET_ALL)
#             print(Fore.GREEN + "2. Sell" + Style.RESET_ALL)
#             print(Fore.GREEN + "3. Get Advice" + Style.RESET_ALL)
#             print(Fore.GREEN + "4. Show" + Style.RESET_ALL)
#             print(Fore.RED + "5. Exit" + Style.RESET_ALL)

#     def show(self):
#       while True:
#             self.print_menu()        
#             choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)            
#             if choice == '1':
#                 print(Fore.BLUE + "You chose to buy." + Style.RESET_ALL)
#                 what=input("what security you want to buy?")
#                 ammout=input("how much you want to buy?")
#                 self.contoller.buy(what,ammout)
#             elif choice == '2':
#                self.contoller.sell()
#             elif choice == '3':
#                 question=input("What is your question?")
#                 answer=self.contoller.get_advice(question)
#                 print(answer)
#                 input("Press Enter to continue...")
#             elif choice == '4':
#                 what=input("what do you want to show? (graph/table):")
#                 if what=="graph":
#                     self.displaygraph()
#                 elif what=="table":
#                     self.dispalytable()
#                 else:
#                     print("Invalid choice. Please try again.")
#             elif choice == '5':
#                 #כאן נקרא לקוד שמייצר טבלה או גרף
#                 #self.contoller.show(מה) מטרתו להביא את הנתונים
#                 print(Fore.RED + "Exiting..." + Style.RESET_ALL)
#                 break
#             else:
#                 print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


# קוד חדש 12.03
from controller import controller
from tabulate import tabulate
from colorama import Fore, Style
import matplotlib.pyplot as plt

class view:
    def __init__(self):
        risk_level = input("Enter your risk level (Low / Medium / High): ").capitalize()
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
        print(Fore.YELLOW + "\n📋 Available Securities to Buy:" + Style.RESET_ALL)
        securities = self.controller.get_available_securities()

        for idx, sec in enumerate(securities, start=1):
            print(Fore.LIGHTYELLOW_EX + f"{idx}. {sec['name']} ({sec['type']}, {sec['sub_type']}, {sec['sector']}, Variance: {sec['variance']}, Price: {sec['basevalue']})" + Style.RESET_ALL)

        try:
            choice = int(input("\nChoose security number to buy: ")) - 1
            amount = int(input("Enter amount to buy: "))
            if choice < 0 or choice >= len(securities):
                print(Fore.RED + "Invalid security choice." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "Invalid input." + Style.RESET_ALL)
            return

        sec = securities[choice]
        success, message = self.controller.buy(
            name=sec['name'], sector=sec['sector'], variance=sec['variance'],
            security_type=sec['type'], subtype=sec['sub_type'],
            amount=amount, basevalue=sec['basevalue']
        )
        print(Fore.GREEN + message if success else Fore.RED + message + Style.RESET_ALL)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def sell(self):
        print(Fore.YELLOW + "\n📋 Your Portfolio:" + Style.RESET_ALL)
        portfolio = self.controller.get_portfolio_data()

        if not portfolio:
            print(Fore.RED + "Your portfolio is empty." + Style.RESET_ALL)
            return

        portfolio_list = list(portfolio.values())
        for idx, sec in enumerate(portfolio_list, start=1):
            print(Fore.LIGHTYELLOW_EX + f"{idx}. {sec['name']} (Amount: {sec['ammont']}, Base Value: {sec['basevalue']})" + Style.RESET_ALL)

        try:
            choice = int(input("\nChoose security number to sell: ")) - 1
            amount = int(input("Enter amount to sell: "))
            if choice < 0 or choice >= len(portfolio_list):
                print(Fore.RED + "Invalid security choice." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "Invalid input." + Style.RESET_ALL)
            return

        name = portfolio_list[choice]['name']
        success, message = self.controller.sell(name, amount)
        print(Fore.GREEN + message if success else Fore.RED + message + Style.RESET_ALL)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def get_advice(self):
        question = input("Enter your question for AI Advisor: ")
        self.controller.get_advice(question)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def show_portfolio(self):
        portfolio = self.controller.get_portfolio_data()

        if not portfolio:
            print(Fore.RED + "Your portfolio is empty." + Style.RESET_ALL)
            return

        print(Fore.YELLOW + "\nYour Portfolio (Table):" + Style.RESET_ALL)
        table = [[sec['name'], sec['ammont'], sec['basevalue']] for sec in portfolio.values()]
        print(tabulate(table, headers=["Name", "Amount", "Base Value"], tablefmt="pretty"))

        total_risk = self.controller.get_total_risk()
        print(Fore.YELLOW + f"\nTotal Portfolio Risk: {total_risk:.2f}" + Style.RESET_ALL)

        show_graph = input("\nDo you want to see a graph? (yes/no): ").lower()
        if show_graph == 'yes':
            self.display_graph(portfolio)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def display_graph(self, portfolio):
        names = [sec['name'] for sec in portfolio.values()]
        amounts = [sec['ammont'] for sec in portfolio.values()]

        plt.figure(figsize=(7, 7))
        plt.pie(amounts, labels=names, autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Distribution')
        plt.show()
