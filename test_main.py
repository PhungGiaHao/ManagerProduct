from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}



def test_register():
    response = client.post(
        "/auth/register",
        json={"username": "test", "password": "test"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["username"] == "test"

##test router login and password
def test_login_incorrect():
    response = client.post(
        "/auth/login",
        data={"username": "test02", "password": "test02"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid credentials"}

def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "test", "description": "test", "price": 12.0, "stock_level": 12, "imageurl": "test", "inventory": 12, "category_id": 1}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "test"
    assert response_json["description"] == "test"
    assert response_json["price"] == 12.0
    assert response_json["stock_level"] == 12
    assert response_json["imageurl"] == "test"
    assert response_json["inventory"] == 12
    assert response_json["category_id"] == 1




##test create product oder
def test_create_order():
    response = client.post(
        "/orders/createOrder/",
        json={"product_id": 7, "quantity": 2, 'weight': 12.0}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["product_id"] == 7
    assert response_json["quantity"] == 2


# def test_update_product():
#     response = client.put(
#         "/products/10",
#         json={"name": "test", "description": "test", "price": 12.0, "stock_level": 12, "imageurl": "test", "inventory": 12, "category_id": 1}
#     )
#     assert response.status_code == 200
#     response_json = response.json()
#     assert response_json["name"] == "test"
#     assert response_json["description"] == "test"
#     assert response_json["price"] == 12.0
#     assert response_json["stock_level"] == 12
#     assert response_json["imageurl"] == "test"
#     assert response_json["inventory"] == 12
#     assert response_json["category_id"] == 1