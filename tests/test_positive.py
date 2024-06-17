from fastapi.testclient import TestClient
from app.main import app
import json
import logging

client = TestClient(app)

ORDERS_SAMPLE = [
    {
        "stock": "Apple",
        "quantity": 5,
    },
    {
        "stock": "Google",
        "quantity": 30,
    }
]


def test_post_orders():
    for order in ORDERS_SAMPLE:
        order_in_json = json.dumps(order)  # converts from Python dict to JSON format
        logging.debug(f"Order in json format: {order_in_json}")
        response = client.post(url="/orders/", content=order_in_json)
        assert response.status_code == 201
        order_index = ORDERS_SAMPLE.index(order)
        order_id = order_index+1  # if it's the first List element, then id=1, etc.
        ORDERS_SAMPLE[order_index]["id"] = order_id  # create a new key-value pair for the id, inside the ORDERS_SAMPLE list
        logging.debug(f"Asserting response msg for post order id={order_id}")
        assert response.json() == {"msg": f"Order placed successfully with id={order_id}"}


def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    logging.debug(f"Asserting response msg for get orders")
    for i in range(0, len(ORDERS_SAMPLE)):
        assert response.json()[i] == ORDERS_SAMPLE[i]

def test_get_order():
    for order in ORDERS_SAMPLE:
        order_id = order["id"]
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        logging.debug(f"Asserting response msg for get order id={order_id}")
        assert response.json()[0] == order

def test_delete_order():
    order_id = ORDERS_SAMPLE[0]["id"]
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204
    logging.debug(f"Asserting response msg for delete order id={order_id}")
    assert response.content == b''
    ORDERS_SAMPLE.pop(0)
    logging.debug(f"ORDERS_SAMPLE list after deletion:{ORDERS_SAMPLE}")

def test_get_orders_after_delete():
    response = client.get("/orders/")
    assert response.status_code == 200
    logging.debug(f"Asserting response msg for get orders after delete")
    for i in range(0, len(ORDERS_SAMPLE)):
        assert response.json()[i] == ORDERS_SAMPLE[i]

#pytest tests/test_positive.py -v --html=report.html --self-contained-html