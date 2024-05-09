import sqlalchemy

import app.database.models


async def add_user(session: sqlalchemy.ext.asyncio.AsyncSession, tg_id):
    try:
        new_user = app.database.models.User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass
