import allure
from api_methods.order_methods import OrderMethods
from api_methods.user_methods import UserMethods
from generators import generate_user_payload
from data import *

class TestCreateOrder:    

    @allure.title('Тест на создание заказа c авторизацией')
    def test_create_order_authorize(self):
        body = generate_user_payload()
        UserMethods.create_user(body)
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 200

    @allure.title('Тест на создание заказа без авторизации')
    def test_create_order_unauthorize(self):
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Тест на создание заказа с ингредиентами')
    def test_create_order_with_ingredients(self, user_cleanup):
        body = user_cleanup
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        actual_ids = OrderMethods.get_actual_ingredients()
        order_payload = {"ingredients": actual_ids}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()
        assert "number" in response.json().get("order", {})
        assert "name" in response.json()

    @allure.title('Тест на создание заказа без ингредиентов: 400 Bad Request')
    def test_create_order_without_ingredients_error(self, user_cleanup):
        body = user_cleanup
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        order_payload = {"ingredients": []}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == MSG_INGREDIENTS_REQUIRED

    @allure.title('Тест создание заказа с неверным хешем ингредиентов: 500 Internal Server Error')
    def test_create_order_invalid_ingredient_hash_error(self, user_cleanup):
        body = user_cleanup
        login_response = UserMethods.enter_user(body)
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token} if token else {}
        order_payload = {"ingredients": [INVALID_INGREDIENT_ID]}
        response = OrderMethods.create_order(order_payload, headers=headers)
        assert response.status_code == 500