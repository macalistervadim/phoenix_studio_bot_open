import enum
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
    waiting_order = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


class Catalog(Base):
    __tablename__ = "catalog"

    title = sqlalchemy.Column(sqlalchemy.String(50), unique=True)
    description = sqlalchemy.Column(sqlalchemy.String(250))
    image = sqlalchemy.Column(sqlalchemy.String, unique=True)
    price = sqlalchemy.Column(sqlalchemy.SmallInteger)
    deadline = sqlalchemy.Column(sqlalchemy.SmallInteger)


class Pcode(Base):
    __tablename__ = "pcode"

    name = sqlalchemy.Column(sqlalchemy.String(50), unique=True)
    discount = sqlalchemy.Column(sqlalchemy.Integer)
    activations = sqlalchemy.Column(sqlalchemy.SmallInteger)
    author = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
    )


class OrderStatusEnum(enum.Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Order(Base):
    __tablename__ = "order"

    product = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("catalog.id", ondelete="CASCADE"),
        index=True,
    )
    user = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        unique=True,
    )
    status = sqlalchemy.Column(
        sqlalchemy.dialects.postgresql.ENUM(OrderStatusEnum, name="order_status_enum"),
        default=OrderStatusEnum.CREATED,
    )


# Обновление и создание всех таблиц при запуске бота
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
