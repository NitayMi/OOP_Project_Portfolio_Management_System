from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from controller import controller  # מייבא את הקונטרולר הקיים שלך

app = FastAPI()

# מודל לבקשות קנייה/מכירה
class TradeRequest(BaseModel):
    name: str
    sector: str
    security_type: str
    subtype: str
    amount: int
    variance: float = None  # לשימוש בקנייה בלבד
    basevalue: float = None  # לשימוש בקנייה בלבד

# קבלת תיק השקעות
@app.get("/portfolio")
def get_portfolio():
    try:
        c = controller("Medium")  # יצירת קונטרולר חדש בכל קריאה
        portfolio = c.get_portfolio_data()
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# קבלת סיכון כולל
@app.get("/risk")
def get_total_risk():
    try:
        c = controller("Medium")  # יצירת קונטרולר חדש בכל קריאה
        risk = c.get_total_risk()
        return {"total_risk": risk}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# קנייה
@app.post("/buy")
def buy_stock(trade: TradeRequest):
    try:
        c = controller("Medium")  # יצירת קונטרולר חדש בכל קריאה
        success, message = c.buy(
            trade.name, trade.sector, trade.variance, trade.security_type,
            trade.subtype, trade.amount, trade.basevalue
        )
        return {"success": success, "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# מכירה
@app.post("/sell")
def sell_stock(trade: TradeRequest):
    try:
        c = controller("Medium")  # יצירת קונטרולר חדש בכל קריאה
        success, message = c.sell(
            trade.name, trade.security_type, trade.sector, trade.subtype, trade.amount
        )
        return {"success": success, "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
