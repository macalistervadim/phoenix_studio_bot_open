import os

import dotenv
import sqlalchemy
import sqlalchemy.ext.asyncio


dotenv.load_dotenv()


engine = sqlalchemy.ext.asyncio.create_async_engine(
    os.getenv("SQLACLHEMY_URL_CONNECT", "url"),
    echo=True,
)
async_session = sqlalchemy.ext.asyncio.async_sessionmaker(engine)


class Base(sqlalchemy.ext.asyncio.AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    __abstract__ = True

    created_on = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    updated_on = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
