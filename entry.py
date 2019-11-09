import asyncio
import argparse
from aiohttp import web
import aioreloader
from app import create_app
from app.settings import load_config


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("Library uvloop is not available")

parser = argparse.ArgumentParser(description="aiohttp")
parser.add_argument("--host", help="Host to listen", default="0.0.0.0")
parser.add_argument("--port", help="Port to accept connection", default="8080")
parser.add_argument("--debug", action="store_true", help="Autoreload code on change")
parser.add_argument("--db", help="Path to database")
parser.add_argument("-c", "--config", type=argparse.FileType(), help="Path to configuration file")

args = parser.parse_args()

app = create_app(config=load_config(args.config), db_url = args.db)

if args.debug:
    print("Debug mode activated")
    aioreloader.start()

if __name__ == '__main__':
    web.run_app(app, host=args.host, port=args.port)
