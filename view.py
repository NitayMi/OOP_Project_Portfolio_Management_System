from colorama import Fore, Style
from controller import controller
from dbmodel import dbmodel
import os
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate


class view:    
    def __init__(self):
        self.contoller=controller()
        self.db=dbmodel()
        
    def displaygraph(self):        
        dictanswer=self.db.getdata()
       # Create a pie chart
        labels = [dictanswer[key]['name'] for key in dictanswer]
        sizes = [dictanswer[key]['ammont'] for key in dictanswer]

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.title('Investment Distribution')
        plt.show()
            
    def dispalytable(self):
        data=self.db.getdata()  
        
        # Convert dictionary to list of lists for tabulate
        table_data = [[k] + list(v.values()) for k, v in data.items()]

        # Define headers
        headers = ["Key", "ID", "Name", "Base Value", "Amount"]

        # Print table
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        input("Press Enter to continue...")
  
    
    def print_menu(self):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.CYAN + "   Menu   " + Style.RESET_ALL)
            print(Fore.CYAN + "==========" + Style.RESET_ALL)
            
            print(Fore.GREEN + "1. Buy" + Style.RESET_ALL)
            print(Fore.GREEN + "2. Sell" + Style.RESET_ALL)
            print(Fore.GREEN + "3. Get Advice" + Style.RESET_ALL)
            print(Fore.GREEN + "4. Show" + Style.RESET_ALL)
            print(Fore.RED + "5. Exit" + Style.RESET_ALL)

    def show(self):
      while True:
            self.print_menu()        
            choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)            
            if choice == '1':
                print(Fore.BLUE + "You chose to buy." + Style.RESET_ALL)
                what=input("what security you want to buy?")
                ammout=input("how much you want to buy?")
                self.contoller.buy(what,ammout)
            elif choice == '2':
               self.contoller.sell()
            elif choice == '3':
                question=input("What is your question?")
                answer=self.contoller.get_advice(question)
                print(answer)
                input("Press Enter to continue...")
            elif choice == '4':
                what=input("what do you want to show? (graph/table):")
                if what=="graph":
                    self.displaygraph()
                elif what=="table":
                    self.dispalytable()
                else:
                    print("Invalid choice. Please try again.")
            elif choice == '5':
                #כאן נקרא לקוד שמייצר טבלה או גרף
                #self.contoller.show(מה) מטרתו להביא את הנתונים
                print(Fore.RED + "Exiting..." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    

