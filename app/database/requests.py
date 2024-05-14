import sqlalchemy

import app.database.models


async def add_user(session: sqlalchemy.ext.asyncio.AsyncSession, tg_id):
    try:
        new_user = app.database.models.User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


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
