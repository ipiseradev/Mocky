
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Validar la configuración antes de iniciar la aplicación.
    # No registrar valores de variables de entorno.
    get_settings()

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mocky API",
        description="Backend de la plataforma Mocky",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(router)

    return app


app = create_app()
