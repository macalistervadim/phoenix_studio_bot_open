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


async def get_pcode(name):
    async with app.database.models.async_session() as session:
        result = await session.scalar(
            sqlalchemy.select(app.database.models.Pcode).where(
                app.database.models.Pcode.name == name,
            ),
        )
        return result


async def add_pcode(session: sqlalchemy.ext.asyncio.AsyncSession, data):
    try:
        new_pcode = app.database.models.Pcode(
            name=data.get("name"),
            discount=int(data.get("discount")),
            activations=int(data.get("activations")),
            author=data.get("author"),
        )
        session.add(new_pcode)
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def delete_pcode(session: sqlalchemy.ext.asyncio.AsyncSession, name):
    try:
        await session.execute(
            sqlalchemy.delete(app.database.models.Pcode).where(
                app.database.models.Pcode.name == name,
            ),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def delete_item(session: sqlalchemy.ext.asyncio.AsyncSession, title):
    try:
        await session.execute(
            sqlalchemy.delete(app.database.models.Catalog).where(
                app.database.models.Catalog.title == title,
            ),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def updata_item_title(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    item,
    new_title,
):
    try:
        item = await session.execute(
            sqlalchemy.update(app.database.models.Catalog)
            .where(app.database.models.Catalog.title == item)
            .values(title=new_title),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def updata_item_description(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    item,
    new_description,
):
    try:
        item = await session.execute(
            sqlalchemy.update(app.database.models.Catalog)
            .where(app.database.models.Catalog.description == item)
            .values(description=new_description),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def updata_item_price(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    item,
    new_price,
):
    try:
        item = await session.execute(
            sqlalchemy.update(app.database.models.Catalog)
            .where(app.database.models.Catalog.price == item)
            .values(price=int(new_price)),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def updata_item_deadline(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    item,
    new_deadline,
):
    try:
        item = await session.execute(
            sqlalchemy.update(app.database.models.Catalog)
            .where(app.database.models.Catalog.deadline == item)
            .values(price=int(new_deadline)),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


async def updata_item_image(
    session: sqlalchemy.ext.asyncio.AsyncSession,
    item,
    new_image,
):
    try:
        item = await session.execute(
            sqlalchemy.update(app.database.models.Catalog)
            .where(app.database.models.Catalog.image == item)
            .values(image=new_image),
        )
        await session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass
