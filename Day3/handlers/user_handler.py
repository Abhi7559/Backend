from schemas.user import LoginRequest, RegisterRequest, UserResponse
from services import user_service


def register_user(register_data: RegisterRequest) -> dict:
    return user_service.register_user(register_data)


def login_user(login_data: LoginRequest) -> dict:
    return user_service.login_user(login_data)


def get_current_user() -> UserResponse:
    return user_service.get_current_user()


def get_admin_stats() -> dict:
    return user_service.get_admin_stats()
