from fastapi import FastAPI
from sqlalchemy import create_engine

from src.config import database, get_db_uri
from src.orm import metadata

from .routers import auth, purchases, resellers


def create_app():
    app = FastAPI()
    engine = create_engine(
        get_db_uri(), connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)

    app.include_router(resellers.router)
    app.include_router(purchases.router)
    app.include_router(auth.router)

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app