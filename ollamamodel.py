# import ollama

# class ollamamodel():   
#     def __init__(self):
#         pass
    
#     def get_advice(self,question):
#         response = ollama.generate(model='deepseek-r1:7b', prompt=question)
#         return(response['response'])

import ollama

class ollamamodel:   
    def __init__(self, model='deepseek-r1:7b'):
        self.model = model  # שמירה של המודל למקרה ונרצה להחליף

    def get_advice(self, question):
        try:
            response = ollama.generate(model=self.model, prompt=question)
            answer = response.get('response', '').strip()
            if not answer:
                return "❌ AI did not return a valid response. Please try again."
            return f"💡 AI Advisor: {answer}"
        except Exception as e:
            return f"❌ AI Error: {e}"
