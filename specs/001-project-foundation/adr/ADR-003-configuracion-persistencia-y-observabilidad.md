# ADR-003: Configuración segura, PostgreSQL persistente y observabilidad mínima

- **Estado**: Aceptada para planificación
- **Fecha**: 2026-11-02
- **Contexto**: FR-003, FR-005, FR-009 y FR-010 requieren inicio seguro, persistencia local y diagnósticos trazables.

## Decisión

Usar `.env.example` sin secretos y `.env` excluido; validar valores al inicio. El inventario de `data-model.md` es la fuente canónica: `.env.example` raíz contiene todas las claves y `frontend/.env.example` sólo deriva el subconjunto público. `LOG_LEVEL` acepta `DEBUG`, `INFO`, `WARNING` y `ERROR` (predeterminado `INFO`) y falla de forma segura ante un valor inválido. `NEXT_PUBLIC_BACKEND_BASE_URL` contiene sólo `http://localhost:8000`; `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` se valida y consume sólo en frontend (predeterminado 3.000 ms, rango 1–10.000 ms). El backend usa `postgresql+psycopg://…@postgres:5432/…` y CORS permite únicamente el origen local explícito, con `GET`/`OPTIONS`, `X-Request-ID` y sin credenciales. Ejecutar `postgres:18.6` mediante Docker Compose v2 con healthchecks, `depends_on` y volumen nombrado; PostgreSQL no publica su puerto en el host. Una migración Alembic crea `development_persistence_markers`; la prueba de integración SQLAlchemy escribe y verifica el marcador sin endpoint público, y la limpieza es un comando explícito filtrado por prefijo. Emitir logs JSON sólo con campos permitidos y `X-Request-ID`; derivar de logs/healthchecks las métricas mínimas de disponibilidad, errores y latencia, sin endpoint `/metrics`, proveedor externo ni almacén separado. Retención local: logs mientras exista el contenedor; artefactos CI sanitizados con `retention-days: 7`. No introducir secretos de integración.

## Alternativas

- Secretos o constantes versionadas: exponen valores y dificultan cambios locales.
- Sin volumen/healthcheck: no prueba persistencia ni disponibilidad real.
- Logs libres o plataforma de telemetría ahora: elevan riesgo de filtración o añaden servicio no solicitado.

## Consecuencias y verificación

La configuración se mantiene en sincronía con documentación y validadores. `docker compose restart postgres` debe preservar el marcador; pruebas de configuración y logs comprueban mensajes seguros, lista de campos y correlación. La limpieza local de marcadores usa `scripts/cleanup-persistence-markers.ps1`, con confirmación, prefijo y conteo; volúmenes requieren una operación explícita, limitada y documentada. CI puede borrar su volumen efímero como paso visible de fin de job.
