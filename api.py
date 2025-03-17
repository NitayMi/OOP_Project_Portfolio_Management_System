from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from controller import controller, ControllerV2
from dbmodel import SqliteRepository
from ollamamodel import AIAdvisorRAG

app = FastAPI()

class TradeRequest(BaseModel):
    name: str
    sector: str
    security_type: str
    subtype: str
    amount: int
    variance: float = None
    basevalue: float = None


@app.get("/portfolio")
def get_portfolio():
    try:
        c = controller("Medium")
        portfolio = c.get_portfolio_data()
        return [vars(item) for item in portfolio]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/risk")
def get_total_risk():
    try:
        c = controller("Medium")
        risk = c.get_total_risk()
        return {"total_risk": risk}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/buy")
def buy(trade: TradeRequest):
    try:
        c = controller("Medium")
        success, message = c.buy(trade.name, trade.sector, trade.variance, trade.security_type, trade.subtype, trade.amount, trade.basevalue)
        return {"success": success, "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sell")
def sell(trade: TradeRequest):
    try:
        c = controller("Medium")
        success, message = c.sell(trade.name, trade.security_type, trade.sector, trade.subtype, trade.amount)
        return {"success": success, "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# =============================================================================
class AIRequest(BaseModel):
    question: str


@app.post("/rag_advice")
def rag_advice(request: AIRequest):
    """
    API endpoint to get AI investment advice using RAG and personalized portfolio.
    :param request: AIRequest containing the user's question.
    :return: AI-generated advice as JSON.
    """
    try:
        # יצירת מחברים לפי OOP (הזרקת תלויות)
        db = SqliteRepository()
        ai = AIAdvisorRAG()
        c = ControllerV2(risk_level='Medium', db_repo=db, ai_advisor=ai)

        # קבלת תשובה מה-AI
        answer = c.get_advice(request.question)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
