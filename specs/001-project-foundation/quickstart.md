# Guía prevista de preparación y validación local

> Esta guía describe el procedimiento que se implementará. No afirma que los comandos, aplicaciones ni Compose existan todavía.

## Prerrequisitos previstos

- Windows 11 actualizado, PowerShell 7 recomendado y Git.
- Docker Desktop en ejecución con backend WSL2 y `docker compose` v2 disponible.
- Node.js 24 LTS y Python 3.13, con gestores de paquetes que se fijarán junto a los lockfiles de Implement.
- Checkout con permisos de escritura y una ruta que puede contener espacios.

## Preparación prevista

1. Abrir PowerShell en la raíz del checkout con una ruta entre comillas: `Set-Location 'C:\ruta con espacios\Mocky'`.
2. Crear configuración local copiando el ejemplo, sin editar archivos versionados: `Copy-Item .env.example .env`.
3. Completar sólo valores de desarrollo locales. El inventario canónico es el de `data-model.md`: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL`, `BACKEND_ALLOWED_ORIGINS`, `LOG_LEVEL`, `NEXT_PUBLIC_BACKEND_BASE_URL`, `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` y `BACKEND_INTERNAL_URL` opcional/futuro. `.env.example` raíz contiene todas las claves; `frontend/.env.example` sólo deriva el subconjunto público. `LOG_LEVEL` acepta `DEBUG`, `INFO`, `WARNING` y `ERROR`, con `INFO` por defecto; un valor inválido debe fallar al inicio. No añadir secretos reales ni variables de proveedores de IA.
4. Validar la composición antes de iniciar: `docker compose --env-file .env -f infra/compose.yaml config`.
5. Iniciar PostgreSQL y los componentes técnicos previstos: `docker compose --env-file .env -f infra/compose.yaml up --build`. PostgreSQL no publica su puerto en el host.
6. Detener sin borrar datos: `docker compose --env-file .env -f infra/compose.yaml stop`. La limpieza de datos será una orden distinta, explícita y con advertencia.

Los nombres definitivos de archivos y scripts quedan fijados en `tasks.md`; Implement debe conservar esta semántica y las restricciones de `plan.md`.

## Direccionamiento previsto

- El navegador ejecuta la comprobación de integración contra `http://localhost:8000/api/v1/integration/health`, leído de `NEXT_PUBLIC_BACKEND_BASE_URL`. Es una variable pública del bundle de Next.js y no puede contener credenciales ni secretos.
- El límite del cliente se lee de `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS`, con valor predeterminado 3.000 ms y rango válido 1–10.000 ms. La validación y el consumo pertenecen al frontend; el backend no lo usa.
- Aunque Next.js corra en un contenedor, el navegador sigue usando `localhost:8000`, que es el puerto publicado de Windows. El navegador nunca usa `http://backend:8000`.
- Sólo código ejecutado dentro del servidor Next.js podría usar `BACKEND_INTERNAL_URL=http://backend:8000`; la comprobación de esta feature no crea un proxy ni realiza esa llamada.
- El backend usa `DATABASE_URL` con host `postgres:5432` dentro de Compose. Nunca usa `localhost` para alcanzar PostgreSQL desde su contenedor. PostgreSQL no se publica en el host.
- `BACKEND_ALLOWED_ORIGINS` permite de forma explícita `http://localhost:3000`; el backend configura `CORSMiddleware` con métodos `GET`/`OPTIONS`, cabecera `X-Request-ID` y sin credenciales. El navegador realiza preflight por esa cabecera. Cambiar host o puerto requiere actualizar ambas variables y no habilitar `*`.

## Escenarios de validación previstos

| Escenario | Acción prevista | Resultado esperado |
| --- | --- | --- |
| Configuración válida | Iniciar desde checkout limpio con `.env` local | Frontend, backend y PostgreSQL reportan disponibilidad conforme al contrato. |
| Configuración inválida | Quitar, vaciar o malformar una clave obligatoria | Inicio falla antes de operar, nombra la clave y corrección, nunca su valor. |
| Integración real | Ejecutar comprobación desde frontend contra FastAPI iniciado | `200`, `status: ready`, `source: mocky-backend`, `X-Request-ID` y preflight CORS válido; no se usan interceptores/mocks. |
| Conexión | Apuntar a host/puerto sin listener | Resultado `connection_error`, distinto de timeout y HTTP. |
| Timeout | Usar entorno de prueba que demora más que `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` | Resultado `timeout` al límite configurado (predeterminado 3.000 ms), sin espera indefinida. |
| Error backend | Hacer que backend responda error controlado | Resultado `backend_error` con status HTTP/código seguro. |
| CORS | Enviar preflight desde origen permitido y desde uno no listado | El origen permitido recibe CORS para `GET`/`OPTIONS` y `X-Request-ID`; el no listado no recibe cabecera CORS. |
| Persistencia | Aplicar migración inicial, crear marcador mediante prueba de integración del backend, `docker compose restart postgres`, leerlo por nueva sesión SQLAlchemy | El marcador continúa disponible y el volumen no se borra; no existe endpoint HTTP público de escritura. |
| Limpieza | Ejecutar `scripts/cleanup-persistence-markers.ps1` con confirmación | Sólo elimina marcadores `persistence-test`, muestra el conteo y no borra volumen ni usa truncate. |
| Windows | Repetir preparación desde rutas con y sin espacios | Sin errores de resolución de rutas. |
| Calidad | Ejecutar controles por componente, incluido Pyright | Cada resultado es identificable; `success`/`passed` es el único aprobatorio y failure/cancelled/skipped/blocked/not_run no cuentan como aprobado. |

## Diagnóstico y recuperación no destructiva

| Síntoma | Comprobación / acción segura |
| --- | --- |
| Docker ausente o detenido | Ejecutar `docker version`; iniciar Docker Desktop y confirmar WSL2/recursos antes de reintentar. |
| Puerto ocupado | Identificar proceso con `Get-NetTCPConnection -LocalPort <puerto>`; liberar o cambiar sólo el puerto documentado. No borrar volúmenes. |
| PostgreSQL aún no listo | Consultar `docker compose ... ps` y logs sanitizados; esperar healthcheck o corregir configuración. |
| Healthcheck fallido | Revisar recursos de Docker, puerto y URL sin mostrar credenciales; no ejecutar limpieza destructiva. |
| Error de conexión | Confirmar URL/origen configurado, contenedor backend y puerto publicado. |
| CORS/preflight | Confirmar `BACKEND_ALLOWED_ORIGINS`, métodos `GET`/`OPTIONS`, cabecera `X-Request-ID` y que no se habilitaron credenciales ni `*`. |
| Timeout | Confirmar `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` entre 1 y 10.000 ms y logs por `request_id`; investigar disponibilidad backend. |
| Error HTTP del backend | Usar `error.code` y `request_id`, no interpretar como fallo de red. |
| PostgreSQL no accesible desde host | Es el comportamiento esperado: no se publica el puerto; usar `docker compose ... exec` o la red interna. |
| Configuración inválida | Restaurar la clave desde `.env.example`; no copiar secretos desde chats, logs ni repositorio. |

La limpieza local de marcadores es `scripts/cleanup-persistence-markers.ps1`: exige confirmación, selecciona sólo UUIDs con prefijo `persistence-test`, muestra cuántos registros afecta y no se ejecuta durante `stop`, `restart` ni recuperación. No usa `truncate`, no borra el volumen y no requiere endpoint HTTP público de escritura. La limpieza de volúmenes requiere una orden manual distinta, con advertencia de pérdida total de datos. En CI se podrá eliminar el volumen efímero al finalizar el job, dejándolo visible como paso de limpieza.

## Observabilidad y retención local

La feature cubre el mínimo de observabilidad con logs JSON correlacionados por `X-Request-ID` y healthchecks; no agrega endpoint `/metrics`, proveedor externo ni almacén de telemetría. Las métricas mínimas se derivan de esos datos: disponibilidad por healthcheck/`status_code`, errores por `status_code >= 400`/`error_code` y latencia por `duration_ms`.

Los logs locales viven en la salida del contenedor mientras éste exista y se descartan al eliminarlo o recrearlo; no se archivan ni se envían fuera del entorno. El estado de healthcheck es efímero. En CI, los artefactos sanitizados se conservan 7 días (`retention-days: 7`) y no se exportan a almacenamiento propio. No se registran secretos, cuerpos, CV, transcripciones, audio, video ni PII.

## Verificaciones futuras

- Frontend: formato, lint, tipado, Vitest y Playwright.
- Backend: Ruff, Pyright (`pyright --project backend/pyrightconfig.json`), pytest unitario e integración.
- Infraestructura: composición válida, healthchecks, `depends_on`, persistencia, preflight CORS y contrato OpenAPI.
- CI: formato, lint, tipado, pruebas, contrato, integración, E2E, escaneo de secretos y auditoría de dependencias son obligatorios cuando sus componentes existan; el primer workflow ejecutable incluye los jobs `secret-scan` y `dependency-audit`. `success` es el único resultado aprobatorio. `failure`, `cancelled`, `skipped` obligatorio, `blocked` y `not_run` hacen fallar el resumen. La auditoría de dependencias es obligatoria desde que existe cada lockfile; no se declara no aplicable después. Playwright y los servicios Compose/PostgreSQL reales se provisionan explícitamente en CI.

Véanse [el contrato](contracts/integration-health.openapi.yaml), [el modelo técnico](data-model.md) y [las decisiones](research.md). Ninguna verificación fue ejecutada durante Plan.
