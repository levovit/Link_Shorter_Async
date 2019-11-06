from sqlalchemy.sql import text


async def select_all(request):
    async with request.app["db"].acquire() as connection:
        query = text("Select * from links;")
        result = await connection.fetch(query)

    return result
