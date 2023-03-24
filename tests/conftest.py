import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from app.database.db import db
from httpx import AsyncClient

from fastapi_template.app.app import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class test:
    pass


@pytest_asyncio.fixture(scope="function")
async def test_client(mocker):
    await db.drop_all()
    await db.create_all()
    mocker.patch("fastapi_template.app.utils.auth.JWTBearer", return_value=test)

    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        yield test_client
