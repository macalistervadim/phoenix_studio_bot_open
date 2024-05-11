import sqlalchemy

import app.database.models


async def add_user(session: sqlalchemy.ext.asyncio.AsyncSession, tg_id):
    try:
        new_user = app.database.models.User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def get_catalog():
    async with app.database.models.async_session() as session:
        result = await session.execute(sqlalchemy.select(app.database.models.Catalog))
        return result.scalars().all()
