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

    


# # קוד ישן שלי
# from colorama import Fore, Style
# from controller import controller
# from dbmodel import dbmodel
# import os
# import seaborn as sns
# import matplotlib.pyplot as plt
# from tabulate import tabulate

# class view:
    
#     def __init__(self):
#         # Prompt user for risk level once at start
#         risk_level = input("Enter your risk level (Low/Medium/High): ").capitalize()
#         self.controller = controller(risk_level=risk_level)
#         self.db = dbmodel()

#     def print_menu(self):
#         os.system('cls' if os.name == 'nt' else 'clear')
#         print(Fore.CYAN + "   Menu   " + Style.RESET_ALL)
#         print(Fore.CYAN + "==========" + Style.RESET_ALL)
#         print(Fore.GREEN + "1. Buy" + Style.RESET_ALL)
#         print(Fore.GREEN + "2. Sell" + Style.RESET_ALL)
#         print(Fore.GREEN + "3. Get Advice" + Style.RESET_ALL)
#         print(Fore.GREEN + "4. Show" + Style.RESET_ALL)
#         print(Fore.RED + "5. Exit" + Style.RESET_ALL)

#     def show(self):
#         while True:
#             self.print_menu()
#             choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)

#             if choice == '1':
#                 print(Fore.BLUE + "You chose to buy." + Style.RESET_ALL)
#                 name = input("Enter security name: ")
#                 sector = input("Enter sector: ")
#                 variance = input("Enter variance (Low/High): ")
#                 security_type = input("Enter type (Stock/Bond): ").lower()
#                 amount = float(input("Enter amount to buy: "))

#                 preferred = False
#                 government = True

#                 if security_type == "stock":
#                     preferred_input = input("Is it preferred stock? (yes/no): ").lower()
#                     preferred = preferred_input == 'yes'
#                 elif security_type == "bond":
#                     government_input = input("Is it government bond? (yes/no): ").lower()
#                     government = government_input == 'yes'

#                 self.controller.buy(name, sector, variance, security_type, preferred, government, amount)
#                 input("Press Enter to continue...")

#             elif choice == '2':
#                 print(Fore.BLUE + "You chose to sell." + Style.RESET_ALL)
#                 name = input("Enter security name to sell: ")
#                 self.controller.sell(name)
#                 input("Press Enter to continue...")

#             elif choice == '3':
#                 print(Fore.BLUE + "You chose to get AI advice." + Style.RESET_ALL)
#                 question = input("What is your question? ")
#                 answer = self.controller.get_advice(question)
#                 print(Fore.GREEN + "AI Advice: " + answer['answer'] + Style.RESET_ALL)
#                 input("Press Enter to continue...")

#             elif choice == '4':
#                 print(Fore.BLUE + "You chose to show portfolio." + Style.RESET_ALL)
#                 what = input("What do you want to show? (graph/table): ").lower()
#                 if what == "graph":
#                     self.displaygraph()
#                 elif what == "table":
#                     self.displaytable()
#                 input("Press Enter to continue...")

#             elif choice == '5':
#                 print(Fore.RED + "Exiting the system. Goodbye!" + Style.RESET_ALL)
#                 break

#             else:
#                 print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
#                 input("Press Enter to continue...")

#     def displaygraph(self):
#         data = self.db.getdata()
#         names = [data[key]['name'] for key in data]
#         amounts = [data[key]['ammont'] for key in data]

#         sns.barplot(x=names, y=amounts)
#         plt.title('Portfolio Graph')
#         plt.xlabel('Security')
#         plt.ylabel('Amount')
#         plt.show()


# קוד חדש 12.03
from controller import controller
from colorama import Fore, Style
from tabulate import tabulate
import matplotlib.pyplot as plt


class view:
    def __init__(self):
        # Ask user for risk level
        risk_level = input("Enter your risk level (Low / Medium / High): ").capitalize()
        self.controller = controller(risk_level=risk_level)

    def show(self):
        while True:
            print(Fore.CYAN + '''
            Menu
            ==========
            1. Buy
            2. Sell
            3. Get Advice
            4. Show Portfolio (Graph/Table)
            5. Exit
            ''' + Style.RESET_ALL)

            choice = input("Enter your choice: ")

            if choice == '1':
                self.buy()
            elif choice == '2':
                self.sell()
            elif choice == '3':
                self.get_advice()
            elif choice == '4':
                self.show_portfolio()
            elif choice == '5':
                print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    def buy(self):
        print(Fore.BLUE + "\n📋 Available Securities to Buy:" + Style.RESET_ALL)
        available_securities = self.controller.get_available_securities()

        for idx, sec in enumerate(available_securities, start=1):
            print(Fore.YELLOW + f"{idx}. {sec['name']} ({sec['type']}, {sec['sub_type']}, {sec['sector']}, Variance: {sec['variance']}, Price: {sec['basevalue']})" + Style.RESET_ALL)

        try:
            choice = int(input("\nChoose security number to buy: ")) - 1
            if choice < 0 or choice >= len(available_securities):
                print(Fore.RED + "❌ Invalid choice. Please try again." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Please enter a number." + Style.RESET_ALL)
            return

        chosen_security = available_securities[choice]

        try:
            amount = int(input("Enter amount to buy: "))
            if amount <= 0:
                print(Fore.RED + "❌ Amount must be greater than zero." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Please enter a valid number." + Style.RESET_ALL)
            return

        success, message = self.controller.buy(
            name=chosen_security['name'],
            sector=chosen_security['sector'],
            variance=chosen_security['variance'],
            security_type=chosen_security['type'],
            preferred=chosen_security['sub_type'] == 'preferred',
            government=chosen_security['sub_type'] == 'government',
            amount=amount
        )

        print(Fore.GREEN + message if success else Fore.RED + message)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def sell(self):
        print(Fore.BLUE + "\n📋 Your Portfolio:" + Style.RESET_ALL)
        portfolio_data = self.controller.get_portfolio_data()
        securities = portfolio_data['securities']

        if not securities:
            print(Fore.RED + "Your portfolio is empty." + Style.RESET_ALL)
            return

        for idx, sec in enumerate(securities, start=1):
            print(Fore.YELLOW + f"{idx}. {sec['name']} ({sec['type']}, {sec['sector']}, Risk: {sec['risk']:.2f})" + Style.RESET_ALL)

        try:
            choice = int(input("\nChoose security number to sell: ")) - 1
            if choice < 0 or choice >= len(securities):
                print(Fore.RED + "❌ Invalid choice." + Style.RESET_ALL)
                return
        except ValueError:
            print(Fore.RED + "❌ Invalid input." + Style.RESET_ALL)
            return

        name_to_sell = securities[choice]['name']
        success, message = self.controller.sell(name_to_sell)
        print(Fore.GREEN + message if success else Fore.RED + message)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def get_advice(self):
        question = input(Fore.CYAN + "Enter your question for AI: " + Style.RESET_ALL)
        print(Fore.YELLOW + "\n🤖 AI is typing..." + Style.RESET_ALL)
        answer = self.controller.get_advice(question)
        print(Fore.GREEN + "\nAI Advice: " + answer + Style.RESET_ALL)
        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def show_portfolio(self):
        data = self.controller.get_portfolio_data()
        securities = data['securities']
        total_risk = data['total_risk']

        if not securities:
            print(Fore.RED + "Your portfolio is empty." + Style.RESET_ALL)
            return

        print(Fore.YELLOW + "\nYour Portfolio (Table):" + Style.RESET_ALL)
        headers = ["Name", "Type", "Sector", "Variance", "Risk"]
        table = [[sec['name'], sec['type'], sec['sector'], sec['variance'], f"{sec['risk']:.2f}"] for sec in securities]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        print(Fore.GREEN + f"\nTotal Portfolio Risk: {total_risk:.2f}" + Style.RESET_ALL)

        choice = input("\nDo you want to see a graph? (yes/no): ").strip().lower()
        if choice == 'yes':
            self.displaygraph(securities)

        input(Fore.CYAN + "\nPress Enter to return to menu..." + Style.RESET_ALL)

    def displaygraph(self, securities):
        names = [sec['name'] for sec in securities]
        risks = [sec['risk'] for sec in securities]

        plt.figure(figsize=(8, 6))
        plt.pie(risks, labels=names, autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Risk Distribution')
        plt.show()


    def displaytable(self):
        data = self.db.getdata()
        table = []
        for key in data:
            row = data[key]
            table.append([row['name'], row['basevalue'], row['ammont']])
        print(tabulate(table, headers=["Name", "Base Value", "Amount"], tablefmt="pretty"))
