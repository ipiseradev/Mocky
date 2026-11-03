
import os
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

DEFAULT_ALLOWED_ORIGIN = "http://localhost:3000"


def validar_log_level(valor: str) -> LogLevel:
    if valor == "DEBUG":
        return "DEBUG"

    if valor == "INFO":
        return "INFO"

    if valor == "WARNING":
        return "WARNING"

    if valor == "ERROR":
        return "ERROR"

    raise ValueError(
        "LOG_LEVEL inválido. "
        "Valores permitidos: DEBUG, INFO, WARNING, ERROR. "
        "Corregí la variable de entorno LOG_LEVEL."
    )


class Settings(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)

    database_url: str
    backend_allowed_origins: list[str]
    log_level: LogLevel = "INFO"

    @field_validator("database_url")
    @classmethod
    def validar_database_url(cls, valor: str) -> str:
        mensaje = (
            "DATABASE_URL inválida. "
            "Configurá una URI PostgreSQL válida con esquema, "
            "usuario, contraseña, servidor y nombre de base de datos."
        )

        try:
            url = urlsplit(valor)

            if url.scheme not in (
                "postgresql",
                "postgresql+psycopg",
            ):
                raise ValueError(mensaje)

            if not url.hostname:
                raise ValueError(mensaje)

            if not url.username or not url.password:
                raise ValueError(mensaje)

            if not url.path.strip("/"):
                raise ValueError(mensaje)

            if url.port is not None and not (
                1 <= url.port <= 65535
            ):
                raise ValueError(mensaje)

            if url.query or url.fragment:
                raise ValueError(mensaje)

            if any(char.isspace() for char in valor):
                raise ValueError(mensaje)

        except ValueError:
            raise ValueError(mensaje) from None

        return valor

    @field_validator("backend_allowed_origins")
    @classmethod
    def validar_origins(cls, origins: list[str]) -> list[str]:
        mensaje = (
            "BACKEND_ALLOWED_ORIGINS contiene un origen inválido. "
            "Configurá una lista de orígenes HTTP o HTTPS "
            "separados por comas, sin credenciales, rutas, "
            "parámetros ni fragmentos."
        )

        if not origins:
            raise ValueError(
                "BACKEND_ALLOWED_ORIGINS inválida. "
                "Configurá al menos un origen HTTP o HTTPS."
            )

        for origin in origins:
            try:
                url = urlsplit(origin)

                if url.scheme not in ("http", "https"):
                    raise ValueError(mensaje)

                if not url.hostname:
                    raise ValueError(mensaje)

                if url.username is not None:
                    raise ValueError(mensaje)

                if url.password is not None:
                    raise ValueError(mensaje)

                if url.path or url.query or url.fragment:
                    raise ValueError(mensaje)

                if url.port is not None and not (
                    1 <= url.port <= 65535
                ):
                    raise ValueError(mensaje)

                if any(char.isspace() for char in origin):
                    raise ValueError(mensaje)

                if origin != f"{url.scheme}://{url.netloc}":
                    raise ValueError(mensaje)

            except ValueError:
                raise ValueError(mensaje) from None

        return origins


def get_settings() -> Settings:
    database_url = os.getenv("DATABASE_URL")

    origins = os.getenv(
        "BACKEND_ALLOWED_ORIGINS",
        DEFAULT_ALLOWED_ORIGIN,
    )

    log_level = os.getenv("LOG_LEVEL", "INFO")

    if not database_url:
        raise ValueError(
            "DATABASE_URL es obligatoria. "
            "Configurala en las variables de entorno "
            "con una URI PostgreSQL válida."
        )

    if not origins or not origins.strip():
        raise ValueError(
            "BACKEND_ALLOWED_ORIGINS inválida. "
            "Configurá al menos un origen HTTP o HTTPS."
        )

    nivel_validado = validar_log_level(log_level)

    try:
        return Settings(
            database_url=database_url,
            backend_allowed_origins=[
                origin.strip()
                for origin in origins.split(",")
            ],
            log_level=nivel_validado,
        )

    except ValidationError as error:
        claves = {
            "database_url": "DATABASE_URL",
            "backend_allowed_origins": "BACKEND_ALLOWED_ORIGINS",
            "log_level": "LOG_LEVEL",
        }

        campos_invalidos = {
            claves.get(str(item["loc"][0]), "CONFIGURACION")
            for item in error.errors(include_input=False)
        }

        raise ValueError(
            "Configuración inválida en: "
            + ", ".join(sorted(campos_invalidos))
            + ". Revisá DATABASE_URL (URI PostgreSQL), "
            "BACKEND_ALLOWED_ORIGINS (orígenes HTTP/HTTPS) "
            "y LOG_LEVEL (DEBUG, INFO, WARNING, ERROR)."
        ) from None
