

import ollama

class ollamamodel():   
    def __init__(self):
        pass
    
    def get_advice(self,question):
        response = ollama.generate(model='deepseek-r1:latest', prompt=question)
        return(response['response'])