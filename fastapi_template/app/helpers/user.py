from fastapi import HTTPException
from fastapi import status


async def validate_create_password(password: str, confirm_password: str) -> bool:
    if password == confirm_password:
        return True
    raise HTTPException(
        detail={
            "message": "the password doesn't match"
        },
        status_code=status.HTTP_400_BAD_REQUEST
    )
