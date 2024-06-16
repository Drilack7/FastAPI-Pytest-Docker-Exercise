from fastapi.testclient import TestClient
from app.main import app
import json
import logging

client = TestClient(app)

ORDERS_SAMPLE = [
    {
        "id": "temp",  # changed id to string
        "seller": "john",
        "buyer": "chris",
        "stock": "Apple",
        "number": 5,
        "price_in_dollars": 100.0
    },
    {
        "id": 794,
        "seller": 40,  # changed seller to int
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
        assert response.status_code == 422
        order_id = order["id"]
        logging.debug(f"Asserting response msg for post order id={order_id}")
        assert "Unprocessable Entity" in str(response)


def test_get_orders():
    response = client.get("/order/")  # changed endpoint to "order" instead of "orders"
    assert response.status_code == 404
    logging.debug(f"Asserting response msg for get orders")
    assert "Not Found" in str(response)

def test_get_order():
    response = client.get("/orders/35")  # get order id that does not exist
    assert response.status_code == 404
    logging.debug(f"Asserting response msg for get order")
    assert "Not Found" in str(response)

def test_delete_order():
    response = client.delete("/orders/60")  # delete order id that does not exist
    assert response.status_code == 404
    logging.debug(f"Asserting response msg for get order")
    assert "Not Found" in str(response)

#pytest tests/test_negative.py -v --html=report.html --self-contained-html