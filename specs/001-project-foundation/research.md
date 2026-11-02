# Investigación técnica — Fundamentos del proyecto Mocky

**Alcance de la investigación**: decisiones de Plan. No se instalaron paquetes, no se consultaron lockfiles inexistentes y no se ejecutó infraestructura.

## Fuentes y política de versiones

La evidencia se revisó el 2026-11-02 en fuentes primarias: documentación de [Next.js](https://nextjs.org/docs/app/getting-started/installation), [Node.js](https://nodejs.org/en/about/previous-releases), [FastAPI](https://fastapi.tiangolo.com/release-notes/), [SQLAlchemy](https://docs.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/en/latest/changelog.html), [Psycopg](https://www.psycopg.org/psycopg3/docs/basic/install.html), [PostgreSQL](https://www.postgresql.org/support/versioning/), [Docker Official Images](https://hub.docker.com/_/postgres), [Playwright](https://playwright.dev/docs/intro) y [GitHub Actions](https://docs.github.com/en/actions), además de los registros oficiales de npm y PyPI. Las revisiones verificadas son Next.js 16.4.4, React 19.3.1, Tailwind CSS 4.3.3, FastAPI 0.162.0, Pydantic 2.14.2, SQLAlchemy 2.1.6, Alembic 1.20.1 y Playwright 1.64.1; la imagen oficial publica `postgres:18.6` y la línea 18. PostgreSQL mantiene cada versión mayor por cinco años.

La implementación deberá fijar las dependencias en lockfiles y la imagen `postgres:18.6` a un digest. Node 24 está en LTS y Next.js 16 requiere Node >=20.9, por lo que Node 24 satisface el mínimo; el peer range exacto de Next.js/React se debe comprobar al generar el lockfile. FastAPI, SQLAlchemy, Alembic y Psycopg publican soporte para Python 3.13; Psycopg declara soporte de PostgreSQL 10 a 18 y recomienda su distribución binaria para no exigir toolchain local. Quedan pendientes de comprobación durante Implement la resolución conjunta de React/Next, TypeScript, Tailwind, ESLint, Prettier, Vitest, Ruff, pytest y los navegadores de Playwright. Esta política evita afirmar una instalación o compatibilidad de lockfile que no ocurrió.

## Decisiones

### D-001 — Monorepo modular con Next.js y FastAPI

- **Problema**: separar responsabilidades de interfaz y API sin complejidad operacional prematura.
- **Alternativas**: un único servidor Next.js; microservicios independientes; monorepo con frontend y backend.
- **Solución elegida**: `frontend/` Next.js App Router y `backend/` FastAPI, con PostgreSQL como única dependencia de datos.
- **Justificación**: cumple la separación obligatoria de FR-001, ofrece tipado/validación nativos en cada límite y mantiene sólo un despliegue backend futuro.
- **Riesgos y consecuencias**: dos toolchains y un contrato a mantener. Se mitigan con contrato OpenAPI versionado, CI por componente y una integración real.
- **Verificación**: árbol, contract test y E2E de la ruta técnica. ADR-001.

### D-002 — HTTP/JSON directo con timeout de 3 s y errores clasificados

- **Problema**: demostrar una frontera real, sin confundir red, timeout y errores de aplicación.
- **Alternativas**: mock del backend, RPC/WebSocket, proxy sin clasificación explícita, HTTP/JSON.
- **Solución elegida**: un componente cliente de Next.js ejecutado por el navegador envía `GET http://localhost:8000/api/v1/integration/health`; usa `NEXT_PUBLIC_BACKEND_BASE_URL`, `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` (predeterminado 3.000 ms, rango 1–10.000 ms) con `AbortController` y cuatro resultados del contrato. Sólo código de servidor Next futuro podría usar `http://backend:8000`.
- **Justificación**: HTTP/JSON es interoperable, observable y suficiente para la comprobación. Tres segundos dan un límite visible durante desarrollo sin retener una pantalla indefinidamente; el máximo configurable de 10 s previene una configuración accidentalmente excesiva. La validación y el consumo del timeout pertenecen al cliente frontend, no al backend.
- **Riesgos y consecuencias**: el browser no diferencia de forma nativa algunos fallos de transporte. El cliente clasifica timeout por su propio abort y conexión por `TypeError` de `fetch`; HTTP no-2xx se clasifica por `response.ok`. CORS permite sólo `http://localhost:3000`, métodos `GET`/`OPTIONS` y cabecera `X-Request-ID`, sin credenciales; el preflight debe probarse. `backend` no se expone al browser y `localhost` no se usa entre contenedores.
- **Verificación**: pruebas unitarias de clasificador; integración contra FastAPI real; Playwright sin interceptores en el caso exitoso. ADR-002.

### D-003 — PostgreSQL 18, Compose v2, volumen nombrado y healthcheck

- **Problema**: disponer de persistencia local repetible y conservar datos tras un reinicio.
- **Alternativas**: SQLite, PostgreSQL instalado nativamente, contenedor efímero sin volumen, PostgreSQL en Compose con volumen.
- **Solución elegida**: `postgres:18.6` en Docker Compose v2, healthchecks de PostgreSQL y backend, `depends_on` con `condition: service_healthy`, volumen nombrado y credenciales locales no sensibles configuradas por `.env`. El backend se conecta mediante `postgresql+psycopg://…@postgres:5432/…`. PostgreSQL no publica su puerto en el host; sólo se publican frontend y backend.
- **Justificación**: se alinea con el motor objetivo y aísla dependencias de Windows. El volumen nombrado satisface FR-005 y el healthcheck evita intentar conectarse antes de que el servicio esté listo.
- **Riesgos y consecuencias**: Docker Desktop puede no arrancar, tener WSL2/RAM insuficientes o puertos ocupados. El quickstart ofrece diagnósticos y recuperación no destructiva; borrar volúmenes exige orden explícita y advertencia. La limpieza de marcadores es un comando separado, con prefijo, confirmación y conteo.
- **Verificación**: `docker compose config`, estado healthy, `alembic upgrade head` y test de integración SQLAlchemy que inserta/lee un marcador tras `restart` normal. ADR-003.

### D-004 — Configuración validada y sin secretos versionados

- **Problema**: iniciar de modo seguro y dar diagnósticos accionables sin filtrar valores.
- **Alternativas**: constantes en código, `.env` versionado, variables sin validación, ejemplo público y validadores por componente.
- **Solución elegida**: `.env.example` con nombres/valores seguros de desarrollo, `.env` ignorado y validación fail-fast en backend y frontend para las variables que consuman. El inventario canónico de `data-model.md` es `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL`, `BACKEND_ALLOWED_ORIGINS`, `LOG_LEVEL` (`DEBUG`/`INFO`/`WARNING`/`ERROR`, predeterminado `INFO`), `NEXT_PUBLIC_BACKEND_BASE_URL`, `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` y `BACKEND_INTERNAL_URL` opcional/futuro; `.env.example` raíz contiene todas las claves y `frontend/.env.example` sólo deriva el subconjunto público. Secretos reales sólo se inyectarán desde GitHub Secrets cuando una feature lo requiera.
- **Justificación**: satisface FR-003, FR-010 y NFR-003. La validación temprana evita síntomas confusos de URLs, puertos o timeouts inválidos. El timeout público se valida y consume sólo en frontend.
- **Riesgos y consecuencias**: las variables públicas de Next se exponen al navegador por diseño; nunca contendrán secreto. Cambiar el esquema obliga a actualizar ejemplo, validadores y quickstart.
- **Verificación**: unit tests de ausencia, vacío, URI/formato/rango inválido y revisión/escaneo de secretos. ADR-003.

### D-005 — Observabilidad mínima segura con correlación

- **Problema**: diagnosticar el cruce frontend-backend sin incorporar plataformas de telemetría ni datos sensibles.
- **Alternativas**: logs de texto sin correlación; OpenTelemetry/proveedor externo ahora; logs JSON locales con ID.
- **Solución elegida**: log JSON de backend limitado a `timestamp`, `level`, `service`, `event`, `request_id`, `method`, `route`, `status_code`, `duration_ms` y `error_code`; cabecera `X-Request-ID` UUID opcional, validada o generada. Las métricas mínimas —disponibilidad, errores y latencia— se derivan de healthchecks y de `status_code`/`error_code`/`duration_ms`, sin endpoint `/metrics`, agregador ni proveedor externo. Retención local: logs mientras exista el contenedor, sin archivo propio; artefactos CI sanitizados con `retention-days: 7`.
- **Justificación**: satisface FR-009/010 y el mínimo de Constitución X con una superficie mínima. La correlación puede propagarse a integraciones futuras sin elegir un proveedor.
- **Riesgos y consecuencias**: los logs locales no se agregan ni se conservan como histórico; cualquier exportador o retención productiva futura necesita feature y ADR. La retención definida no debe incluir información sensible.
- **Verificación**: test que propaga/genera ID, revisión de lista permitida, existencia de los campos de métricas mínimas y comprobación de la política de retención. ADR-003.

### D-006 — Calidad y CI sin resultados ambiguos

- **Problema**: controles repetibles que no presenten una omisión como aprobación.
- **Alternativas**: una única tarea de CI, controles opcionales silenciosos, jobs explícitos por dominio.
- **Solución elegida**: jobs nominados para frontend, backend, integración, contrato, E2E y seguridad, ejecutados en PR y `main`, más resumen bloqueante con `always()`. Herramientas: Prettier/ESLint/TypeScript/Vitest/Playwright y Ruff/Pyright/pytest, con escaneo de secretos desde el primer workflow y auditoría de dependencias obligatoria desde cada lockfile; T033 declara todos los jobs, incluidos `secret-scan` y `dependency-audit`, y T035/T036 completan sus reglas sin duplicarlos. Pyright se fija en versión exacta y usa `backend/pyrightconfig.json` con modo `standard`; E2E provisiona navegadores con Playwright y servicios Compose reales en CI.
- **Justificación**: conserva trazabilidad de FR-006/007/NFR-004. GitHub Actions permite jobs y resultados separables. La auditoría no tiene período de no aplicabilidad una vez creado el lockfile.
- **Riesgos y consecuencias**: E2E y Docker aumentan duración de CI; se mantendrán como único escenario técnico y sólo matrices necesarias. Un control sin dependencia disponible informa `blocked` y falla; `cancelled`, `not_run` y `skipped` obligatorio también fallan. `success` sólo se acepta con el artefacto de resultado obligatorio; `skipped` sólo puede tolerarse con una no aplicabilidad explícita y temporal aprobada.
- **Verificación**: revisión del DAG del workflow y cambios intencionalmente inválidos durante Implement. No hay CI creada ni ejecutada en Plan.

### D-007 — Preparación futura sin implementar IA ni 3D

- **Problema**: no cerrar opciones futuras sin violar alcance.
- **Alternativas**: agregar Three.js/proveedor IA ahora; crear microservicios vacíos; documentar puntos de extensión.
- **Solución elegida**: documentar que módulos futuros viven detrás de límites internos de frontend/backend y exigirán especificación propia de permisos, privacidad, accesibilidad, latencia y fallback.
- **Justificación**: deja una dirección evolutiva sin código muerto ni dependencias innecesarias.
- **Riesgos y consecuencias**: no garantiza compatibilidad con proveedores concretos; esa decisión debe hacerse con requisitos aprobados.
- **Verificación**: revisión de alcance y ausencia de dependencias/servicios de IA/3D en esta feature.

### D-008 — Actualización de dependencias y lockfiles

- **Problema**: evitar deriva entre versiones declaradas, lockfiles, auditoría y documentación sin incorporar actualizaciones automáticas inseguras.
- **Alternativas**: rangos flotantes; actualización automática sin revisión; lockfiles y digest fijados con PR de actualización.
- **Solución elegida**: fijar versiones exactas y digests en Implement; toda actualización se hace en un PR dedicado que actualiza lockfiles/digest, ejecuta auditoría, pruebas, Pyright y CI, y registra la decisión en `research.md` y `verification.md`. No se aceptan rangos flotantes ni actualizaciones automáticas sin revisión.
- **Justificación**: mantiene NFR-004 y la trazabilidad de la Constitución XI sin introducir un servicio adicional.
- **Riesgos y consecuencias**: una actualización puede requerir cambios de compatibilidad; se trata como cambio revisable y no se simula su resultado.
- **Verificación**: revisión del PR de actualización, lockfiles/digest efectivos y resultados reales de CI.
