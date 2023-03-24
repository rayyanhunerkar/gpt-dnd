from app.schemas import Login
from app.schemas import Register
from app.schemas import User

__all__ = (
    'register_serializer',
    'login_serializer',
    'get_user_serializer'
)


async def register_serializer(user: Register) -> dict | None:
    if user:
        return {
            "email": user.email,
            "name": user.name,
            "password": user.password,
            "confirm_password": user.confirm_password
        }
    return None


async def login_serializer(user: Login) -> dict | None:
    if user:
        return {
            "email": user.email,
            "password": user.password
        }


async def get_user_serializer(user: User) -> dict | None:
    if user:
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
