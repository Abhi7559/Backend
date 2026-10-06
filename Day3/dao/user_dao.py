from schemas.user import LoginRequest, RegisterRequest, UserResponse


def register_user(register_data: RegisterRequest) -> dict:
    print(f"[User DAO] Registering new user with email: {register_data.email}")
    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": register_data.name,
            "email": register_data.email,
        },
    }


def login_user(login_data: LoginRequest) -> dict:
    print(f"[User DAO] Authenticating user with email: {login_data.email}")
    return {
        "message": "User logged in successfully",
        "email": login_data.email,
    }


def get_current_user() -> UserResponse:
    print("[User DAO] Fetching current authenticated user profile")

    # In a real application, database records often contain sensitive fields like password hashes
    internal_user_record = {
        "id": 1,
        "username": "abhishek",
        "email": "abhi@example.com",
        "role": "admin",
        "password": "supersecretpassword123",
        "password_hash": "$2b$12$e80yq91jfkdlsajfkdl",
    }

    # UserResponse uses Pydantic's response serialization to selectively return only safe fields
    # Notice: 'password' and 'password_hash' are ignored and never exposed to the client
    return UserResponse.model_validate(internal_user_record)


def get_admin_stats() -> dict:
    print("[User DAO] Fetching admin statistics")
    return {
        "message": "Admin statistics retrieved successfully",
        "total_users": 10,
        "total_reviews": 45,
    }
