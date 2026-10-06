from dao import user_dao
from schemas.user import LoginRequest, RegisterRequest, UserResponse


def register_user(register_data: RegisterRequest) -> dict:
    return user_dao.register_user(register_data)


def login_user(login_data: LoginRequest) -> dict:
    return user_dao.login_user(login_data)


def get_current_user() -> UserResponse:
    return user_dao.get_current_user()


def get_admin_stats() -> dict:
    return user_dao.get_admin_stats()
