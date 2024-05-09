import os

import dotenv
import sqlalchemy
import sqlalchemy.ext.asyncio


dotenv.load_dotenv()

# Асихнронное подключение к БД
engine = sqlalchemy.ext.asyncio.create_async_engine(
    os.getenv("SQLACLHEMY_URL_CONNECT", "url"),
    echo=True,
)
async_session = sqlalchemy.ext.asyncio.async_sessionmaker(engine)


class Base(sqlalchemy.ext.asyncio.AsyncAttrs, sqlalchemy.orm.DeclarativeBase):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    created_on = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    updated_on = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )


class User(Base):
    __tablename__ = "user"

    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)


class Catalog(Base):
    __tablename__ = "catalog"

    title = sqlalchemy.Column(sqlalchemy.String(50), unique=True)
    description = sqlalchemy.Column(sqlalchemy.String(100))
    image = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    price = sqlalchemy.Column(sqlalchemy.SmallInteger)
    deadline = sqlalchemy.Column(sqlalchemy.SmallInteger)


class Order(Base):
    __tablename__ = "order"

    class _OrderStateEnum(sqlalchemy.Enum):
        __name__ = "order_state_enum"
        __tablename__ = "order_state_enum"
        CREATED = "создан"
        IN_PROGRESS = "в процессе"
        COMPLETED = "завершен"

    product = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("catalog.id", ondelete="CASCADE"),
        index=True,
    )
    user = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )
    state_order = sqlalchemy.Column(
        _OrderStateEnum(name="order_state_enum"),
        default=_OrderStateEnum.CREATED,
    )


# Обновление и создание всех таблиц при запуске бота
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
