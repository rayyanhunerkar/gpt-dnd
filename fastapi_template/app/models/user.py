from datetime import datetime
from uuid import uuid4

from app.database.db import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(25), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f")>"
        )
    #
    # @classmethod
    # async def create(cls, _password, **kwargs):
    #     user = cls(id=str(uuid4()), password=hash_password(_password) ** kwargs)
    #     db.add(user)
    #     try:
    #         await db.commit()
    #     except Exception:
    #         await db.rollback()
    #         raise
    #     return user
    #
    # @classmethod
    # async def update(cls, id, **kwargs):
    #     query = (
    #         sqlalchemy_update(cls)
    #         .where(cls.id == id)
    #         .values(**kwargs)
    #         .execution_options(synchronize_session="fetch")
    #     )
    #     await db.execute(query)
    #
    #     try:
    #         await db.commit()
    #     except Exception:
    #         await db.rollback()
    #         raise
    #
    # @classmethod
    # async def get(cls, id):
    #     query = select(cls).where(cls.id == id)
    #     users = await db.execute(query)
    #     (user,) = users.first()
    #     return user
    #
    # @classmethod
    # async def get_email(cls, email):
    #     query = select(cls).where(cls.email == email)
    #     users = await db.execute(query)
    #     (user,) = users.first()
    #     return user
    #
    # @classmethod
    # async def get_all(cls):
    #     query = select(cls)
    #     users = await db.execute(query)
    #     users = users.scalars().all()
    #     return users
    #
    # @classmethod
    # async def delete(cls, id):
    #     query = sqlalchemy_delete(cls).where(cls.id == id)
    #     await db.execute(query)
    #     try:
    #         await db.commit()
    #     except Exception:
    #         await db.rollback()
    #         raise
    #     return True
