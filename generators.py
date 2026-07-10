from helpers import *

def random_email() -> str:
    return f"email_{random_string(6)}@yandex.ru"

def random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return "".join(random.choice(alphabet) for _ in range(length))

def random_name() -> str:
    return f"name_{random_string(6)}"


def generate_user_payload() -> dict:
    return {
        "email": random_email(),
        "password": random_password(),
        "name": random_name()
    }