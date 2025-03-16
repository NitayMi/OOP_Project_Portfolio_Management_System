from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from controller import controller

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
