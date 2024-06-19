from fastapi import FastAPI, HTTPException, status, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
import asyncio
import json

app = FastAPI(
    openapi_version="3.0.0",
    title="Forex Trading Platform API",
    description="A RESTful API to simulate a Forex trading platform with WebSocket support for real-time order updates.",
    version="1.0.0",
    servers=[{'url': 'http://localhost:8000'}]
)

orders = []  #database

class OrderInput(BaseModel):
    stock: str
    quantity: int

class OrderOutput(BaseModel):
    id: int
    stock: str
    quantity: int

@app.get("/orders/", response_description="A list of orders")
async def retrieve_all_orders():
    await asyncio.sleep(random.uniform(0, 1))
    return orders

@app.post("/orders/", response_description="Order placed", status_code=status.HTTP_201_CREATED)
async def place_a_new_order(order: OrderInput):
    await asyncio.sleep(random.uniform(0, 1))
    new_order_id = len(orders)+1
    order_output = OrderOutput(id=new_order_id, stock=order.stock, quantity=order.quantity)  # convert input foramt to output
    orders.append(order_output)
    return {"msg": f"Order placed successfully with id={new_order_id}"}

@app.get("/orders/{order_id}", response_description="Order found")
async def retrieve_a_specific_order(order_id: int):
    await asyncio.sleep(random.uniform(0, 1))
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        return match

@app.delete("/orders/{order_id}", response_description="Order canceled", status_code=204)
async def cancel_an_order(order_id: int):
    await asyncio.sleep(random.uniform(0, 1))
    match = [order for order in orders if order_id == order.id]
    if not match:
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        index = orders.index(match[0])
        deleted_order = orders.pop(index)
        return deleted_order

#######################################################################################################################
############################################## Websocket ##############################################################
#######################################################################################################################

with open('app/websocket_page.html', 'r') as f:
    html = f.read()

@app.get("/ws")
async def WebSocket_connection_for_real_time_order_information():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        order_ws = await websocket.receive_text()
        order = json.loads(order_ws)  # converts json to dict
        new_order_id = len(orders) + 1
        order_output = OrderOutput(id=new_order_id, stock=order["stock"], quantity=order["quantity"])
        orders.append(order_output)
        await websocket.send_text(f"Order with id={new_order_id} is Pending...")
        await asyncio.sleep(random.uniform(0, 3))
        await websocket.send_text(f"Order with id={new_order_id} was Executed--->" + str(order_output))

#fastapi dev app/main.py