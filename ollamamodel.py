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
    
# =============================================================================
from rag_engine import query as rag_query
import ollama

class AIAdvisorRAG:
    def __init__(self, model='deepseek-r1:7b'):
        self.model = model

    def get_advice(self, question, portfolio_data=None):
        portfolio_context = ""
        if portfolio_data:
            portfolio_context = "\n".join([
                f"- {item.name}, {item.security_type}, Sector: {item.sector}, Risk: {item.variance}, Amount: {item.ammont}"
                for item in portfolio_data
            ])

        rag_context = rag_query(question, top_k=3)  # רק שאילתא
        full_question = f"""
You are a professional investment advisor AI.

User's Risk Profile and Portfolio:
{portfolio_context}

Relevant Background Knowledge:
{rag_context}

Question:
{question}

Provide a professional and personalized investment recommendation.
"""
        response = ollama.generate(
            model=self.model,
            prompt=full_question
        )
        return response.get('response', '❌ No valid response')
