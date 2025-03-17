import ollama
from abc import ABC, abstractmethod

class IAIAdvisor(ABC):
    @abstractmethod
    def get_advice(self, question: str) -> str:
        pass

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

class OllamaAIAdvisor(IAIAdvisor):
    def __init__(self):
        self.ai = ollamamodel()

    def get_advice(self, question: str) -> str:
        return self.ai.get_advice(question)