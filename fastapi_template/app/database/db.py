import sys

from app.configs.settings import DBSettings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
database = DBSettings.config
if sys.argv[-1] == '--test':
    database = DBSettings.config_test


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = create_async_engine(
            database,
            future=True,
            echo=True,
        )
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


session = AsyncDatabaseSession()


async def get_db():
    _session = AsyncDatabaseSession()
    try:
        yield _session
    finally:
        await _session.close()
