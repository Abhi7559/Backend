from fastapi import APIRouter

from handlers import user_handler
from schemas.user import LoginRequest, RegisterRequest

router = APIRouter(
    tags=["Auth / Users"],
)


@router.post("/auth/register")
def register(request: RegisterRequest):
    return user_handler.register_user(request)


@router.post("/auth/login")
def login(request: LoginRequest):
    return user_handler.login_user(request)


@router.get("/users/me")
def get_me():
    return user_handler.get_current_user()


@router.get("/admin/stats")
def get_admin_stats():
    return user_handler.get_admin_stats()
