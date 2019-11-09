from datetime import datetime, timedelta
from sqlalchemy.sql import text
from aiohttp.web_request import Request


async def select_all(request: Request) -> list:
    async with request.app["db"].acquire() as connection:
        query = text("Select * from links;")
        result = await connection.fetch(query)
    return result


async def insert_link(request: Request, long_link: str, short_link: str, days_active: int = 90, name="anon") -> None:
    async with request.app["db"].acquire() as connection:
        if "http" not in long_link:
            long_link = "http://" + long_link
        active_until = datetime.utcnow() + timedelta(days=days_active)
        query = text(f"""INSERT INTO links
                    values 
                    (default, 
                    '{long_link}',
                    '{short_link}', 
                    '{name}', 
                    '{active_until}');""")
        await connection.fetch(query)


async def is_link_in_database(request: Request, short_link: str) -> bool:
    async with request.app["db"].acquire() as connection:
        query = text(f"""select exists(select 1 from links where short_link='{short_link}');""")
        result = await connection.fetch(query)
    return result[0]


async def get_link(request: Request, short_link: str) -> list:
    async with request.app["db"].acquire() as connection:
        query = text(f"""select long_link, active_until from links where short_link = '{short_link}';""")
        result = await connection.fetch(query)
    return result
