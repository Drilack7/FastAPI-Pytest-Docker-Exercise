from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

orders = [
    {
        "id": 528,
        "seller": "john",
        "buyer": "chris",
        "stock": "Apple",
        "number": 1,
        "price_in_dollars": 100
    }
]

def test_post_order():
    temp = str(orders[0])
    response = client.post(url="/orders/", content=temp)
    assert response.status_code == 201

def test_get_ordes():
    response = client.get("/orders/")
    assert response.status_code == 200



#pytest -v --html=report.html