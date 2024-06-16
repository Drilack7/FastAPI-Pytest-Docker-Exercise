from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import random
import time

orders = []  #database

class Order(BaseModel):
    id: int
    seller: str
    buyer: str
    stock: str
    number: int
    price_in_dollars: float

app = FastAPI()

@app.get("/orders/", response_description="A list of orders")
def retrieve_all_orders():
    time.sleep(random.uniform(0, 1))
    return orders

@app.post("/orders/", response_description="Order placed", status_code=status.HTTP_201_CREATED)
async def place_a_new_order(order: Order):
    time.sleep(random.uniform(0, 1))
    orders.append(order)
    return {"msg": f"Order placed successfully with id={order.id}"}

@app.get("/orders/{order_id}", response_description="Order found")
def retrieve_a_specific_order(order_id: int):
    time.sleep(random.uniform(0, 1))
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        return match

@app.delete("/orders/{order_id}", response_description="Order canceled", status_code=204)
def cancel_an_order(order_id: int):
    time.sleep(random.uniform(0, 1))
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        index = orders.index(match[0])
        deleted_order = orders.pop(index)
        return deleted_order

#fastapi dev app/main.py