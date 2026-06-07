import allure
from api_methods.user_methods import UserMethods
from generators import generate_user_payload
from data import *

class TestCreateUser:

    @allure.title('Тест на создание уникального пользователя')
    def test_create_user(self, created_user):
        response = created_user["response"]
        token = created_user["token"]
        body = created_user["body"]
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert token is not None
        assert body["email"].endswith("@yandex.ru")

    @allure.title('Тест на ошибку при создании дубликата пользователя')
    def test_create_duplicate_user_conflict(self, user_cleanup):
        body = user_cleanup
        duplicate_response = UserMethods.create_user(body)
        assert duplicate_response.status_code == 403
        assert duplicate_response.json().get("success") is False
        assert duplicate_response.json().get("message") == MSG_USER_EXISTS


    @allure.title('Ошибка при создании пользователя: отсутствует email')
    def test_create_user_without_email(self):
        body = generate_user_payload()
        del body["email"]
        response = UserMethods.create_user(body)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == MSG_MISSING_FIELDS


    @allure.title('Ошибка при создании пользователя: отсутствует password')
    def test_create_user_without_password(self):
        body = generate_user_payload()
        del body["password"]
        response = UserMethods.create_user(body)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == MSG_MISSING_FIELDS


    @allure.title('Ошибка при создании пользователя: отсутствует name')
    def test_create_user_without_name(self):
        body = generate_user_payload()
        del body["name"]
        response = UserMethods.create_user(body)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == MSG_MISSING_FIELDS