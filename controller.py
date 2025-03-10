
from dbmodel import dbmodel
from ollamamodel import ollamamodel

class controller():
    def __init__(self):
        self.dbmodel = dbmodel()
        self.ollamamodel = ollamamodel()       
        
    def buy(self,whatsecurity,ammout):
        print("Buying...")
        self.dbmodel.insert(whatsecurity,ammout)

    def sell(self):
       print("Selling...")
       self.dbmodel.delete()

    def get_advice(self,question):
       print("Getting advice...")
       answer= self.ollamamodel.get_advice(question)
       return answer

  
    
