import sqlalchemy

import app.database.models


async def add_user(session: sqlalchemy.ext.asyncio.AsyncSession, tg_id):
    try:
        new_user = app.database.models.User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def update_user(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    tg_id,
):
    try:
        await session.execute(
            sqlalchemy.update(app.database.models.User)
            .where(app.database.models.User.tg_id == tg_id)
            .values(waiting_order=True),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def get_order(user_id):
    async with app.database.models.async_session() as session:
        result = await session.execute(
            sqlalchemy.select(app.database.models.Order).filter_by(user=user_id),
        )
        return result.scalars().first()


async def add_order(session: sqlalchemy.ext.asyncio.AsyncSession, data):
    try:
        # Проверяем, есть ли уже заказ у данного пользователя
        existing_order = await get_order(data.get("user"))
        if existing_order:
            return False
        else:
            item = app.database.models.Order(
                product=int(data.get("item_id")),
                user=data.get("user"),
            )
            session.add(item)
            await session.commit()
            return True
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        return False


async def delete_order(session: sqlalchemy.ext.asyncio.AsyncSession, user):
    try:
        await session.execute(
            sqlalchemy.delete(app.database.models.Order).where(
                app.database.models.Order.user == user,
            ),
        )
        await session.execute(
            sqlalchemy.update(app.database.models.User)
            .where(app.database.models.User.id == user)
            .values(waiting_order=False),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()


async def add_item(session: sqlalchemy.ext.asyncio.AsyncSession, data):
    try:
        item = app.database.models.Catalog(
            title=data.get("title"),
            description=data.get("description"),
            image=data.get("image").file_id,
            price=int(data.get("price")),
            deadline=int(data.get("deadline")),
        )
        session.add(item)
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def get_catalog():
    async with app.database.models.async_session() as session:
        result = await session.execute(sqlalchemy.select(app.database.models.Catalog))
        return result.scalars().all()


async def get_user(tg_id):
    async with app.database.models.async_session() as session:
        result = await session.scalar(
            sqlalchemy.select(app.database.models.User).where(
                app.database.models.User.tg_id == tg_id,
            ),
        )
        return result
