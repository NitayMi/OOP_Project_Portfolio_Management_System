import ollama

def getanswer( question):   
    response = ollama.generate(model='deepseek-r1:7b', prompt=question)
    return response['response']
    
    
if __name__ == "__main__":
     question = input("ask a question:")
     print(getanswer(question)) 

