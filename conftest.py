import pytest
from api_methods.user_methods import UserMethods
from generators import generate_user_payload

@pytest.fixture
def user_cleanup():
    body = generate_user_payload()
    response = UserMethods.create_user(body)
    token = response.json().get("accessToken")
    headers = {"Authorization": token} if token else {}
    yield body
    if token:
        UserMethods.delete_user(headers)


@pytest.fixture
def created_user():
    body = generate_user_payload()
    response = UserMethods.create_user(body)
    
    token = response.json().get("accessToken")
    headers = {"Authorization": token} if token else {}
    
    yield {
        "body": body,
        "response": response,
        "token": token,
        "headers": headers,
    }

    if token:
        UserMethods.delete_user(headers)