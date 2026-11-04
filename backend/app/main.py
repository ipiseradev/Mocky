from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.logging import configure_logging
from app.core.request_id import RequestIdMiddleware
from app.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Validar la configuración antes de iniciar la aplicación.
    # No registrar valores de variables de entorno.
    settings = get_settings()
    configure_logging(settings.log_level)

    yield


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Mocky API",
        description="Backend de la plataforma Mocky",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestIdMiddleware)
    app.include_router(router)

    return app


app = create_app()
