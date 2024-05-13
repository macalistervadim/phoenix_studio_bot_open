import sqlalchemy

import app.database.models


async def get_editable_item(title):
    async with app.database.models.async_session() as session:
        result = await session.scalar(
            sqlalchemy.select(app.database.models.Catalog).where(
                app.database.models.Catalog.title == title,
            ),
        )
        return result
