import allure
import pytest
from api_methods.user_methods import UserMethods
from generators import generate_user_payload
from data import *

class TestCreateUser:

    @allure.title('Тест на создание уникального пользователя')
    def test_create_user(self):
        body= generate_user_payload()
        response= UserMethods.create_user(body)
        token = response.json().get("accessToken")
        if token:
            headers = {"Authorization": token}
            UserMethods.delete_user(headers)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Тест на ошибку при создании дубликата пользователя')
    def test_create_duplicate_user_conflict(self, user_cleanup):
        body = user_cleanup
        duplicate_response = UserMethods.create_user(body)
        assert duplicate_response.status_code == 403
        assert duplicate_response.json().get("success") is False
        assert duplicate_response.json().get("message") == MSG_USER_EXISTS

    @allure.title('Тест на ошибку при отсутствии одного из полей')
    @pytest.mark.parametrize(
    "missing_field,expected_message",
    [("email", MSG_MISSING_FIELDS),
     ("password", MSG_MISSING_FIELDS),
     ("name", MSG_MISSING_FIELDS)
    ])
    def test_create_user_without_first_name(self, missing_field, expected_message):
        body = generate_user_payload()
        body_without_field = {
            key: value
            for key, value in body.items()
            if key != missing_field
            }
        response = UserMethods.create_user(body_without_field)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json().get("message") == expected_message