import allure
from api_methods.user_methods import UserMethods
from generators import *
from data import *

class TestLoginUser:

    @allure.title('Тест на вход под существующим пользователем')
    def test_login_success(self, user_cleanup):
        body = user_cleanup
        response = UserMethods.enter_user(body)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Тест на вход с неверным логином и паролем')
    def test_login_wrong_credentials_returns_error(self):
        body = {
            "email": random_email(),
            "password": random_password()
            }
        response = UserMethods.enter_user(body)
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == MSG_INVALID_CREDENTIALS