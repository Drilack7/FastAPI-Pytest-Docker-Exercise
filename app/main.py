from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import random
import time

orders = []  #database

class OrderInput(BaseModel):
    stock: str
    quantity: int

class OrderOutput(BaseModel):
    id: int
    stock: str
    quantity: int

app = FastAPI(
    openapi_version="3.0.0",
    title="Forex Trading Platform API",
    description="A RESTful API to simulate a Forex trading platform with WebSocket support for real-time order updates.",
    version="1.0.0",
    servers=[{'url': 'http://localhost:8000'}]
)

@app.get("/orders/", response_description="A list of orders")
async def retrieve_all_orders():
    time.sleep(random.uniform(0, 1))
    return orders

@app.post("/orders/", response_description="Order placed", status_code=status.HTTP_201_CREATED)
async def place_a_new_order(order: OrderInput):
    time.sleep(random.uniform(0, 1))
    new_order_id = len(orders)+1
    order_output = OrderOutput(id=new_order_id, stock=order.stock, quantity=order.quantity)
    orders.append(order_output)
    return {"msg": f"Order placed successfully with id={new_order_id}"}

@app.get("/orders/{order_id}", response_description="Order found")
async def retrieve_a_specific_order(order_id: int):
    time.sleep(random.uniform(0, 1))
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        return match

@app.delete("/orders/{order_id}", response_description="Order canceled", status_code=204)
async def cancel_an_order(order_id: int):
    time.sleep(random.uniform(0, 1))
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        index = orders.index(match[0])
        deleted_order = orders.pop(index)
        return deleted_order

#fastapi dev app/main.py