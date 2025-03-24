from contextlib import asynccontextmanager

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route





starlette_app = Starlette(
    routes=[
        Route("/telegram", telegram, methods=["POST"]),
        Route("/healthcheck", health, methods=["GET"]),
        Route("/submitpayload", custom_updates, methods=["POST", "GET"]),
    ]
    
)
webserver = uvicorn.Server(
    config=uvicorn.Config(
        app=starlette_app,
        port=PORT,
        use_colors=False,
        host="127.0.0.1",
    )
)

@asynccontextmanager
async def lifespan(app):
    print('Startup')
    yield
    print('Shutdpwn')