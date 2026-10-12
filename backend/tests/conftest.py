import asyncio
import os

from dotenv import load_dotenv

# Tests TRUNCATE tables, so they must never run against the dev database.
# Load backend/.env first, then swap only the database name for finance_test —
# credentials must be the user's own (asyncpg does not support Windows SSPI auth).
load_dotenv()
_base = os.environ.get('DATABASE_URL', 'postgresql://finance_user:CHANGE_ME@localhost:5432/finance_test')
_query = ''
if '?' in _base:
    _base, _query = _base.split('?', 1)
    _query = '?' + _query
# Tests TRUNCATE: point them at a dedicated DB, never the app's database
os.environ['DATABASE_URL'] = _base.rsplit('/', 1)[0] + '/finance_test_unit' + _query

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from app.main import app
from app.core.database import AsyncSessionLocal, engine, Base
from app.api.deps import get_db


@pytest.fixture(scope="session", autouse=True)
def _create_tables():
    """Create schema in the test DB once (app lifespan does not run under httpx ASGI transport)."""
    async def _create():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(_create())
    yield


@pytest.fixture(scope="function")
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def clean_db(db_session):
    await db_session.execute(text("TRUNCATE TABLE transactions, keywords, categories, documents RESTART IDENTITY CASCADE"))
    await db_session.commit()
    yield db_session
    await db_session.execute(text("TRUNCATE TABLE transactions, keywords, categories, documents RESTART IDENTITY CASCADE"))
    await db_session.commit()


@pytest.fixture(scope="function")
async def async_client(clean_db):
    async def override_get_db():
        yield clean_db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
