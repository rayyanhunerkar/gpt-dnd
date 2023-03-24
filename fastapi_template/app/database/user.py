from app.database.db import session
from app.models import User
from app.utils.hash import hash_password
from sqlalchemy import select
from sqlalchemy import update

__all__ = (
    'create_user',
    'get_user',
    'get_user_email',
)


async def create_user(db: session, user: dict) -> User:
    hashed_password = hash_password(user.get('password'))
    db_user = User(
        email=user.get('email'),
        password=hashed_password,
        name=user.get('name')
    )
    db.add(db_user)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return db_user


async def get_user(db: session, _id: str):
    query = select(User).where(User.id == _id)
    try:
        users = await db.execute(query)
    except Exception:
        raise
    user = users.first()
    return user


async def get_user_email(db: session, email):
    query = select(User).where(User.email == email)
    try:
        users = await db.execute(query)
    except Exception:
        raise
    user = users.first()
    return user


async def update_user(db: session, _id, **kwargs):
    query = (
        update(User)
        .where(User.id == _id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
