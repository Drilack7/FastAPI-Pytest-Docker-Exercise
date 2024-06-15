from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders = []  #database

class Order(BaseModel):
    id: int
    seller: str
    buyer: str
    stock: str
    number: int
    price_in_dollars: float

app = FastAPI()

@app.get("/orders/")
def get_orders():
    return orders

@app.post("/orders/")
async def create_order(order: Order):
    orders.append(order)
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        return match

#fastapi dev main.py