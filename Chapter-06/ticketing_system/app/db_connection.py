from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///.database.db"


def get_engine():
    return create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


AsyncSessionLocal = async_sessionmaker(
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession,
)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


def ping_mongo_db_server():
    return None


def mongo_client():
    return None