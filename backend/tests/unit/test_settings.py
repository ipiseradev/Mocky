
import pytest

from app.core.settings import get_settings

DATABASE_URL_VALIDA = (
    "postgresql://usuario:CLAVE_SECRETA@localhost:5432/mocky"
)

DATABASE_URL_PSYCOPG = (
    "postgresql+psycopg://usuario:clave@postgres:5432/mocky"
)

ORIGINS_VALIDOS = "http://localhost:3000,https://mocky.com"


@pytest.fixture
def configurar_entorno(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL_VALIDA)
    monkeypatch.setenv("BACKEND_ALLOWED_ORIGINS", ORIGINS_VALIDOS)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv(
        "NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS",
        raising=False,
    )


@pytest.mark.parametrize("valor", [None, ""])
def test_database_url_ausente_o_vacia(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
    valor: str | None,
) -> None:
    if valor is None:
        monkeypatch.delenv("DATABASE_URL")
    else:
        monkeypatch.setenv("DATABASE_URL", valor)

    with pytest.raises(ValueError, match="DATABASE_URL"):
        get_settings()


@pytest.mark.parametrize(
    "valor",
    [
        "no-es-una-url",
        "mysql://usuario:clave@localhost/mocky",
        "postgresql://localhost/mocky",
        "postgresql://usuario:clave@localhost",
        "postgresql://usuario:clave@localhost:99999/mocky",
    ],
)
def test_database_url_invalida(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
    valor: str,
) -> None:
    monkeypatch.setenv("DATABASE_URL", valor)

    with pytest.raises(ValueError, match="DATABASE_URL"):
        get_settings()


def test_database_url_psycopg_valida(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
) -> None:
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL_PSYCOPG)

    settings = get_settings()

    assert settings.database_url == DATABASE_URL_PSYCOPG


def test_origins_ausentes_usan_valor_predeterminado(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
) -> None:
    monkeypatch.delenv("BACKEND_ALLOWED_ORIGINS")

    settings = get_settings()

    assert settings.backend_allowed_origins == [
        "http://localhost:3000"
    ]


@pytest.mark.parametrize("valor", ["", "   "])
def test_origins_vacios_son_invalidos(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
    valor: str,
) -> None:
    monkeypatch.setenv("BACKEND_ALLOWED_ORIGINS", valor)

    with pytest.raises(
        ValueError,
        match="BACKEND_ALLOWED_ORIGINS",
    ):
        get_settings()


@pytest.mark.parametrize(
    "valor",
    [
        "localhost:3000",
        "ftp://localhost:3000",
        "http://",
        "http://usuario:clave@localhost:3000",
        "http://localhost:3000/ruta",
        "http://localhost:3000?token=secreto",
        "http://localhost:99999",
        "*",
    ],
)
def test_origins_invalidos(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
    valor: str,
) -> None:
    monkeypatch.setenv("BACKEND_ALLOWED_ORIGINS", valor)

    with pytest.raises(
        ValueError,
        match="BACKEND_ALLOWED_ORIGINS",
    ):
        get_settings()


def test_configuracion_valida(
    configurar_entorno: None,
) -> None:
    settings = get_settings()

    assert settings.database_url == DATABASE_URL_VALIDA

    assert settings.backend_allowed_origins == [
        "http://localhost:3000",
        "https://mocky.com",
    ]


def test_log_level_predeterminado(
    configurar_entorno: None,
) -> None:
    settings = get_settings()

    assert settings.log_level == "INFO"


@pytest.mark.parametrize(
    "nivel",
    ["DEBUG", "INFO", "WARNING", "ERROR"],
)
def test_log_level_permitido(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
    nivel: str,
) -> None:
    monkeypatch.setenv("LOG_LEVEL", nivel)

    settings = get_settings()

    assert settings.log_level == nivel


@pytest.mark.parametrize(
    "nivel",
    ["INVALIDO", "", "TRACE"],
)
def test_log_level_invalido_no_expone_valor(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
    nivel: str,
) -> None:
    monkeypatch.setenv("LOG_LEVEL", nivel)

    with pytest.raises(ValueError) as error:
        get_settings()

    mensaje = str(error.value)

    assert "LOG_LEVEL" in mensaje
    assert "DEBUG, INFO, WARNING, ERROR" in mensaje

    if nivel:
        assert nivel not in mensaje


def test_backend_no_exige_timeout_publico(
    configurar_entorno: None,
) -> None:
    settings = get_settings()

    assert settings.log_level == "INFO"

    assert not hasattr(
        settings,
        "next_public_integration_timeout_ms",
    )


def test_error_no_expone_secreto(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
) -> None:
    monkeypatch.setenv(
        "BACKEND_ALLOWED_ORIGINS",
        "origen-invalido",
    )

    with pytest.raises(ValueError) as error:
        get_settings()

    mensaje = str(error.value)

    assert "CLAVE_SECRETA" not in mensaje
    assert "DATABASE_URL" in mensaje
    assert "BACKEND_ALLOWED_ORIGINS" in mensaje


def test_database_url_invalida_no_expone_contrasena(
    monkeypatch: pytest.MonkeyPatch,
    configurar_entorno: None,
) -> None:
    password = "PASSWORD_PRIVADA_DE_PRUEBA"

    database_url = (
        f"mysql://usuario:{password}@localhost:5432/mocky"
    )

    monkeypatch.setenv("DATABASE_URL", database_url)

    with pytest.raises(ValueError) as error:
        get_settings()

    mensaje = str(error.value)

    assert "DATABASE_URL" in mensaje
    assert password not in mensaje
    assert database_url not in mensaje
