from fastapi.testclient import TestClient
from app.main import app
import json
import logging

client = TestClient(app)

ORDERS_SAMPLE = [
    {
        "stock": 10,  # changed stock from string to int
        "quantity": 5,
    },
    {
        "stock": "Google",
        "quantity": "something",  # changed quantity from int to str
    }
]


def test_post_orders_wrong_types():
    for order in ORDERS_SAMPLE:
        order_in_json = json.dumps(order)  # converts from Python dict to JSON format
        logging.debug(f"Order in json format: {order_in_json}")
        response = client.post(url="/orders/", content=order_in_json)
        assert response.status_code == 422
        assert "Unprocessable Entity" in str(response)

def test_get_orders_wrong_endpoint():
    response = client.get("/order/")  # changed endpoint to "order" instead of "orders"
    assert response.status_code == 404
    logging.debug(f"Asserting response msg for get orders")
    assert "Not Found" in str(response)

def test_get_order_non_exising_id():
    response = client.get("/orders/35")  # get order id that does not exist
    assert response.status_code == 404
    logging.debug(f"Asserting response msg for get order")
    assert "Not Found" in str(response)

def test_delete_order_non_exising_id():
    response = client.delete("/orders/60")  # delete order id that does not exist
    assert response.status_code == 404
    logging.debug(f"Asserting response msg for get order")
    assert "Not Found" in str(response)

#pytest tests/test_negative.py -v --html=report.html --self-contained-html