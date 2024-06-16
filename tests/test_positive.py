from fastapi.testclient import TestClient
from app.main import app
import json
import logging

client = TestClient(app)

ORDERS_SAMPLE = [
    {
        "id": 528,
        "seller": "john",
        "buyer": "chris",
        "stock": "Apple",
        "number": 5,
        "price_in_dollars": 100.0
    },
    {
        "id": 794,
        "seller": "sophie",
        "buyer": "jane",
        "stock": "Google",
        "number": 23,
        "price_in_dollars": 80.0
    }
]


def test_post_orders():
    for order in ORDERS_SAMPLE:
        order_in_json = json.dumps(order)  # converts from Python dict to JSON format
        logging.debug(f"Order in json format: {order_in_json}")
        response = client.post(url="/orders/", content=order_in_json)
        assert response.status_code == 201
        order_id = order["id"]
        logging.debug(f"Asserting response msg for post order id={order_id}")
        assert response.json() == {"msg": f"Order placed successfully with id={order_id}"}


def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    logging.debug(f"Asserting response msg for get orders")
    for i in range(0, len(ORDERS_SAMPLE)):
        assert str(response.json()[i]) == str(ORDERS_SAMPLE[i])  # convert to strings because as JSON object it was failing

def test_get_order():
    for order in ORDERS_SAMPLE:
        order_id = order["id"]
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        logging.debug(f"Asserting response msg for get order id={order_id}")
        assert str(response.json()[0]) == str(order)

def test_delete_order():
    order_id = ORDERS_SAMPLE[0]["id"]
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204
    logging.debug(f"Asserting response msg for delete order id={order_id}")
    assert response.content == b''

def test_get_orders_after_delete():
    response = client.get("/orders/")
    assert response.status_code == 200
    logging.debug(f"Asserting response msg for get orders after delete")
    assert str(response.json()[0]) == str(ORDERS_SAMPLE[1])  # asserting that only the second order remained in database

#pytest tests/test_positive.py -v --html=report.html --self-contained-html