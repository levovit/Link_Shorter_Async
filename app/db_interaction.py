from datetime import datetime, timedelta
from sqlalchemy.sql import text
from aiohttp.web_request import Request


async def select_all(request: Request) -> list:
    async with request.app["db"].acquire() as connection:
        query = text("Select * from links;")
        result = await connection.fetch(query)
    return result


async def insert_link(request: Request, long_link: str, short_link: str, days_active: int = 90) -> None:
    async with request.app["db"].acquire() as connection:
        active_until = datetime.utcnow() + timedelta(days=days_active)
        query = text(f"""INSERT INTO links
                    values 
                    (default, 
                    '{long_link}',
                    '{short_link}', 
                    default, 
                    '{active_until}', 
                    default);""")
        await connection.fetch(query)


async def is_link_in_database(request: Request, short_link: str) -> bool:
    async with request.app["db"].acquire() as connection:
        query = text(f"""select  exists(select 1 from links where short_link='{short_link}' and active);""")
        result = await connection.fetch(query)
    return result[0]
