from app.database.db import get_db
from app.database.user import create_user
from app.database.user import get_user_email
from app.helpers import validate_create_password
from app.schemas import Login
from app.schemas import Register
from app.schemas import UserResponse
from app.serializers import get_user_serializer
from app.serializers import login_serializer
from app.serializers import register_serializer
from app.utils import sign_jwt
from app.utils.hash import verify_password
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

auth_router = APIRouter(
    prefix="/users",
    tags=['users']
)


@auth_router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def register(body: Register, db: Session = Depends(get_db)) -> dict:
    serializer = await register_serializer(body)
    user = await get_user_email(db, serializer.get('email'))
    if user:
        raise HTTPException(
            detail={
                "message": "email already exists"
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    await validate_create_password(serializer.get('password'), serializer.get('confirm_password'))
    user = await create_user(db, serializer)
    result = await get_user_serializer(user)
    return {
        "data": result,
        "message": "User registered successfully"
    }


@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK
)
async def login(body: Login, db: Session = Depends(get_db)) -> dict:
    serializer = await login_serializer(body)
    user = await get_user_email(db, serializer.get('email'))
    if verify_password(serializer.get('password'), user['User'].password):
        result = await get_user_serializer(user['User'])
        return {
            'data': sign_jwt(result),
            "message": "user logged in"
        }
