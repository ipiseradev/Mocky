# Tasks: Fundamentos del proyecto Mocky

**Input**: Artefactos de diseño de `specs/001-project-foundation/`
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/` y `adr/`
**Tests**: Obligatorios por `spec.md` y Constitución IV. Las tareas de prueba se implementan antes o junto con la capacidad que verifican y se ejecutan sólo durante Implement/Verify.

**Formato**: Cada ítem usa `- [ ] T### [P?] [US?]`; `Deps` identifica prerequisitos, `Done` es el criterio de finalización verificable y `Refs` mantiene trazabilidad. `[P]` sólo aparece cuando no hay archivo compartido ni dependencia pendiente.

## Fase A — Preparación compartida

**Propósito**: crear el esqueleto reproducible y la configuración no secreta. Bloquea las historias de usuario.

- [x] T001 Crear los directorios vacíos `frontend/`, `backend/`, `infra/` y `.github/workflows/`, con archivos de mantenimiento mínimos donde sean necesarios. Deps: ninguna. Done: el árbol coincide con `plan.md` y no contiene funcionalidad de producto. Refs: FR-001, FR-011, NFR-005.
- [x] T002 [P] Preservar y extender el `.gitignore` existente, y crear/actualizar `.env.example` en la raíz como fuente canónica sin secretos: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL`, `BACKEND_ALLOWED_ORIGINS`, `LOG_LEVEL`, `NEXT_PUBLIC_BACKEND_BASE_URL`, `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` y `BACKEND_INTERNAL_URL` opcional/futuro; documentar que `.env` queda excluido y que `frontend/.env.example` sólo deriva el subconjunto público de este inventario. Deps: ninguna; ningún otro trabajo de esta fase modifica `.gitignore`. Done: se conservan las reglas existentes, no se versionan valores reales y las claves permiten derivar la configuración local sin contradicciones. Refs: FR-003, FR-010, NFR-003; Historia 1.2.
- [x] T003 Crear `infra/compose.yaml` con servicios planificados `postgres`, `backend` y `frontend`, volumen nombrado, red por defecto, healthchecks de PostgreSQL (`pg_isready`) y backend, y `depends_on` con `condition: service_healthy`; publicar sólo frontend y backend, sin publicar PostgreSQL en el host. Deps: T001, T002. Done: `docker compose --env-file .env -f infra/compose.yaml config` es válido, PostgreSQL no tiene puerto de host, el volumen no se elimina por `stop` o `restart` y el orden de arranque respeta healthchecks. Refs: FR-002, FR-005, FR-012, NFR-001, NFR-002.
- [x] T004 [P] Crear `infra/backend.Dockerfile` y `infra/frontend.Dockerfile` con rutas de trabajo entre comillas/relativas aptas para Windows y sin secretos embebidos. Deps: T001. Done: cada Dockerfile define sólo su runtime y dependencias declaradas, sin servicios extra. Refs: FR-002, FR-011, FR-012, NFR-002, NFR-005.
- [x] T005 [P] Crear `backend/pyproject.toml` con Python 3.13, versiones aprobadas y no flotantes de FastAPI, Pydantic, SQLAlchemy 2.1.6, Alembic 1.20.1, `psycopg[binary]`, Ruff, Pyright, pytest y `backend/pyrightconfig.json` en modo `standard`; resolver y validar el lockfile al inicio de Implement, antes de T007. Deps: T001. Done: manifiesto y lockfile efectivo declaran restricciones de runtime/desarrollo, Pyright queda fijado en versión exacta con comando `pyright --project backend/pyrightconfig.json`, y la resolución compatible queda verificada antes de construir backend. Refs: FR-006, FR-011, NFR-004; pendiente de compatibilidad de `research.md`.
- [ ] T006 [P] Crear `frontend/package.json`, `frontend/tsconfig.json`, `frontend/next.config.*`, `frontend/tailwind` config y lockfile con Next.js 16.4.4, React 19, TypeScript estricto, Tailwind, ESLint, Prettier, Vitest y Playwright; resolver y validar el lockfile al inicio de Implement, antes de T018. Deps: T001. Done: TypeScript tiene `strict: true`; la resolución compatible de Next/React y herramientas queda verificada antes de construir frontend y no hay dependencias 3D/IA. Refs: FR-001, FR-006, FR-011, NFR-005.

**Checkpoint A**: infraestructura declarada, sin contenedores iniciados ni dependencias instaladas durante Tasks.

---

## Fase B — Backend y persistencia fundacionales

**Propósito**: proveer backend técnico, configuración segura y persistencia para las historias P1.

- [ ] T007 Crear el paquete FastAPI en `backend/app/main.py`, `backend/app/api/` y `backend/app/core/` con factory de aplicación y rutas técnicas separadas del dominio, y crear `backend/README.md` con responsabilidad, límites y comandos previstos del backend. Deps: T005. Done: la aplicación expone sólo la base necesaria para el contrato de infraestructura, sin entrevistas, autenticación, IA ni multimedia; `backend/README.md` describe sólo capacidades técnicas y enlaza al contrato/Quickstart. Refs: FR-001, FR-008, FR-011, NFR-001, NFR-005.
- [ ] T008 Implementar en `backend/app/core/settings.py` validación fail-fast de `DATABASE_URL`, `BACKEND_ALLOWED_ORIGINS` y `LOG_LEVEL`, sin registrar valores. El backend no valida ni consume `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS`. `LOG_LEVEL` acepta `DEBUG`, `INFO`, `WARNING` y `ERROR`, con predeterminado `INFO`. Deps: T007, T002. Done: ausencia, vacío, formato URI/origen inválido o nivel fuera del conjunto permitido producen diagnóstico seguro con clave, valores permitidos y acción correctiva, sin imprimir el valor recibido. Refs: FR-003, FR-010, FR-012, NFR-003; Historia 1.3.
- [ ] T009 Crear pruebas unitarias de configuración en `backend/tests/unit/test_settings.py` para claves ausentes, vacías, malformadas y válidas, incluidos `LOG_LEVEL` predeterminado `INFO` y cada valor permitido. Deps: T005, T008. Done: cubre las reglas de `data-model.md`, confirma que el backend no exige el timeout público, que un `LOG_LEVEL` inválido falla sin imprimir el valor y que nunca se expone un secreto real. Refs: FR-003, FR-006, FR-010, NFR-003.
- [ ] T010 Implementar `backend/app/core/logging.py` y middleware de correlación en `backend/app/core/request_id.py` para validar/generar `X-Request-ID` y emitir sólo los campos permitidos. Deps: T007, T008. Done: cada respuesta técnica lleva UUID válido y los logs JSON contienen únicamente `timestamp`, `level`, `service`, `event`, `request_id`, `method`, `route`, `status_code`, `duration_ms` y `error_code`; esos campos permiten derivar disponibilidad, errores y latencia sin endpoint de métricas ni almacén externo. Refs: FR-009, FR-010; NFR-004.
- [ ] T011 Crear pruebas unitarias de logs/correlación en `backend/tests/unit/test_request_id.py` y `backend/tests/unit/test_logging.py`. Deps: T005, T010. Done: verifica propagación/generación de UUID y ausencia de URL con credenciales, cuerpos, secretos y PII en salida. Refs: FR-009, FR-010; Historia 3.5.
- [ ] T012 Implementar conexión SQLAlchemy en `backend/app/db/session.py` y modelo técnico en `backend/app/db/models/development_persistence_marker.py` usando exclusivamente `DATABASE_URL` ya validada por `backend/app/core/settings.py`. Deps: T008. Done: Python no hardcodea hostname; Compose aporta `postgres` dentro de `DATABASE_URL`, nunca `localhost` entre contenedores, y el modelo contiene `id` UUID, `label` con prefijo `persistence-test` y `created_at` UTC. Refs: FR-005, FR-011, FR-012; NFR-002.
- [ ] T013 Configurar Alembic en `backend/alembic.ini`, `backend/alembic/env.py` y crear la migración inicial en `backend/alembic/versions/` para `development_persistence_markers`. Deps: T012. Done: `alembic upgrade head` crea sólo la tabla técnica versionada; no ejecutarla en esta etapa Tasks. Refs: FR-005, FR-006, FR-011.
- [ ] T014 Implementar `GET /api/v1/integration/health` en `backend/app/api/integration.py` conforme a `contracts/integration-health.openapi.yaml`, incluyendo `200`, `503`, error seguro y `X-Request-ID`; configurar `CORSMiddleware` con orígenes de `BACKEND_ALLOWED_ORIGINS`, métodos `GET`/`OPTIONS`, cabecera `X-Request-ID` y credenciales deshabilitadas. Deps: T010, T012, T013. Done: la ruta declara/valida modelos FastAPI de respuesta, verifica PostgreSQL, no expone escritura pública y el preflight CORS acepta sólo el origen configurado. Refs: FR-004, FR-005, FR-009, FR-010; Historia 2.1, 2.4.
- [ ] T015 Crear pruebas de contrato/backend en `backend/tests/integration/test_integration_health.py` para `200`, `503`, esquema OpenAPI, correlación, preflight CORS válido y origen no permitido. Deps: T014. Done: prueba contra FastAPI y PostgreSQL reales durante Implement, no mediante mocks para el caso exitoso; verifica `OPTIONS`/`X-Request-ID` y rechazo de origen no listado. Refs: FR-004, FR-005, FR-009, FR-010; Historia 2.1, 2.4.
- [ ] T016 Crear en `backend/tests/integration/conftest.py` y `backend/tests/integration/test_persistence_marker.py` la prueba marcada `serial_postgres`: migra, inserta/commitea un UUID y usa su fixture exclusiva como único controlador de `docker compose restart postgres`, para leerlo después por nueva sesión SQLAlchemy. Deps: T003, T012, T013. Done: se ejecuta aislada, sin otras pruebas concurrentes que usen PostgreSQL; no usa endpoint HTTP de escritura, no ejecuta `down -v` ni limpieza automática y conserva el marcador/volumen si falla para diagnóstico. Refs: FR-005, FR-012; Historia 2.5.
- [ ] T017 Configurar Ruff, Pyright y pytest en `backend/pyproject.toml`, `backend/pyrightconfig.json` y `backend/tests/conftest.py`, con marcadores separados `unit`, `integration` y `serial_postgres`. Deps: T005, T009, T011, T015, T016. Done: comandos documentados distinguen tipo de prueba, `pyright --project backend/pyrightconfig.json` queda disponible, `pytest -m serial_postgres` recolecta exactamente la prueba de persistencia y no ejecuta integración sin su dependencia PostgreSQL. Refs: FR-006, FR-007, NFR-004.

**Checkpoint B**: backend técnico, migración y pruebas de persistencia listos para la integración, sin API de negocio.

---

## Fase C — Frontend y entorno local reproducible (Historia 1, P1)

**Objetivo**: permitir preparar el entorno local sin secretos, con UI mínima y configuración explícita.
**Prueba independiente**: desde un checkout limpio de Windows, crear `.env` desde el ejemplo y preparar/iniciar/detener sin pasos tácitos ni rutas rotas.

- [ ] T018 [US1] Crear App Router y UI mínima de diagnóstico en `frontend/src/app/layout.tsx`, `frontend/src/app/page.tsx` y `frontend/src/app/globals.css`. Deps: T006. Done: sólo presenta el estado técnico de integración; no agrega flujos de entrevista ni datos de usuario. Refs: FR-001, FR-011, NFR-005; Historia 1.1.
- [ ] T019 [US1] Implementar validación de configuración pública en `frontend/src/lib/config.ts` para `NEXT_PUBLIC_BACKEND_BASE_URL` y `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` (predeterminado 3.000 ms, rango 1–10.000 ms). Deps: T006, T002. Done: la URL pública predeterminada es `http://localhost:8000`, no contiene credenciales ni secretos, el timeout validado se expone al cliente y todo valor inválido genera error accionable seguro. Refs: FR-003, FR-004, FR-010, FR-012, NFR-003.
- [ ] T020 [US1] Crear scripts de desarrollo, formato, lint, typecheck, Vitest y Playwright en `frontend/package.json`, `frontend/eslint.config.*`, `frontend/prettier.config.*`, `frontend/vitest.config.*` y `frontend/playwright.config.*`. Deps: T006. Done: cada control tiene comando identificable y configuración compatible con TypeScript estricto. Refs: FR-006, FR-007, NFR-004; Historia 3.1.
- [ ] T021 [US1] Actualizar `infra/compose.yaml` y `frontend/.env.example` para montar la configuración pública de navegador, publicar sólo frontend/backend, no publicar PostgreSQL en el host y mantener los nombres internos `backend`/`postgres` fuera del bundle público. `frontend/.env.example` deriva sólo el subconjunto público del inventario canónico de `data-model.md`, sin contradecirlo. Deps: T003, T018, T019. Done: el navegador utiliza `localhost:8000`, un eventual servidor Next usa `BACKEND_INTERNAL_URL=http://backend:8000`, ningún contenedor usa `localhost` para otro servicio, el preflight CORS queda alineado con el origen publicado y no hay variables públicas contradictorias. Refs: FR-002, FR-003, FR-012, NFR-001, NFR-002, NFR-003; Historia 1.1–1.4.
- [ ] T022 [US1] Crear pruebas unitarias de configuración frontend en `frontend/src/lib/config.test.ts`. Deps: T019, T020. Done: cubre variable ausente, vacía, URL inválida o con credenciales, timeout inválido, valor por defecto 3.000 ms, rango 1–10.000 ms y configuración válida sin revelar valores. Refs: FR-003, FR-006, FR-010; Historia 1.2–1.3.
- [ ] T023 [US1] Crear `frontend/README.md` que delimite responsabilidad, variables públicas y comandos de desarrollo previstos. Deps: T018, T020, T021. Done: describe sólo capacidades técnicas existentes y enlaza al contrato/quickstart. Refs: FR-001, FR-008, FR-011, NFR-001.

**Checkpoint US1**: el entorno y la UI de diagnóstico pueden prepararse sin secretos; la integración aún se completa en Fase D.

---

## Fase D — Integración real y persistencia (Historia 2, P1)

**Objetivo**: demostrar frontend → backend real y supervivencia de datos técnicos tras reinicio.
**Prueba independiente**: con Compose iniciado, el navegador recibe una respuesta FastAPI verificable y clasifica conexión, timeout y error HTTP; el marcador persiste tras `restart postgres`.

- [ ] T024 [US2] Revisar/validar `specs/001-project-foundation/contracts/integration-health.openapi.yaml` frente a modelos FastAPI y añadir validación automatizada en `backend/tests/contract/test_openapi_contract.py`. Deps: T014, T015. Done: contrato es fuente verificable de ruta, cabecera, CORS operativo, campos `checked_at`/`error.code`, esquemas `200`/`503`/default y no define endpoint de escritura. Refs: FR-004, FR-006, FR-011; Historia 2.1, 2.4.
- [ ] T025 [US2] Implementar el cliente HTTP real en `frontend/src/lib/integration-client.ts` con `AbortController` usando el valor validado de `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` (predeterminado 3.000 ms) y propagación/generación de `X-Request-ID`. Deps: T019, T014. Done: solicita `NEXT_PUBLIC_BACKEND_BASE_URL/api/v1/integration/health` desde el navegador, no fija el timeout de forma independiente y nunca usa mocks/interceptores para éxito. Refs: FR-004, FR-009, FR-012; Historia 2.1.
- [ ] T026 [US2] Implementar clasificación de `success`, `connection_error`, `timeout` y `backend_error` en `frontend/src/lib/integration-result.ts` y mostrarla en `frontend/src/app/page.tsx`. Deps: T025, T018. Done: red, abort propio y HTTP no-2xx resultan distinguibles; sólo `200` con `source: mocky-backend` es éxito. Refs: FR-004, FR-012; Historia 2.1–2.4.
- [ ] T027 [US2] Crear pruebas unitarias del cliente/clasificador en `frontend/src/lib/integration-client.test.ts` y `frontend/src/lib/integration-result.test.ts`, usando dobles sólo unitarios. Deps: T020, T025, T026. Done: cubre URL correcta, timeout configurado/finito, error de transporte y respuesta HTTP de error; los mocks se limitan a unitarias y ningún éxito de integración se prueba con interceptores. Refs: FR-004, FR-006, FR-012; Historia 2.2–2.4.
- [ ] T028 [US2] Crear prueba E2E sin interceptores en `frontend/tests/e2e/integration-health.spec.ts` contra frontend y FastAPI reales. Deps: T021, T024, T026. Done: verifica respuesta `200` producida por backend, preflight CORS, `source`, `X-Request-ID` y UI de éxito. Refs: FR-004, FR-006, FR-009; Historia 2.1.
- [ ] T029 [US2] Crear escenarios E2E/integración de conexión, timeout y error backend en `frontend/tests/e2e/integration-errors.spec.ts` y `backend/tests/integration/test_error_modes.py`. Deps: T026, T015. Done: cada escenario informa clase distinta y termina en el límite configurado por `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS`; no expone secretos. Refs: FR-004, FR-010, FR-012; Historia 2.2–2.4.
- [ ] T030 [US2] Integrar la ejecución aislada del marcador persistente en `infra/compose.yaml`, `scripts/run-persistence-test.ps1`, `scripts/cleanup-persistence-markers.ps1` y `backend/tests/integration/test_persistence_marker.py`, invocando exclusivamente `pytest -m serial_postgres` en un proceso/job dedicado y sin pruebas concurrentes que dependan de PostgreSQL. Deps: T003, T016, T021. Done: el fixture de T016 controla el único `restart postgres`, el runner espera healthcheck, falla si no recolecta exactamente la prueba marcada y verifica el mismo UUID; el cleanup exige confirmación, filtra por prefijo `persistence-test`, muestra el conteo y no ejecuta `down -v`, truncate ni limpieza silenciosa. El volumen nombrado preserva los datos hasta una limpieza manual explícita. Refs: FR-005, FR-012; Historia 2.5.
- [ ] T031 [US2] Documentar y probar recuperación técnica en `backend/tests/integration/test_readiness.py` y `infra/compose.yaml`: PostgreSQL pendiente/no disponible produce `503` recuperable y no fallo confuso. Deps: T014, T021, T030. Done: estado `healthy` y respuesta de dependencia no disponible se distinguen en pruebas/salida segura. Refs: FR-005, FR-009, FR-012; Casos límite PostgreSQL.

**Checkpoint US2**: comunicación y persistencia se prueban contra servicios reales; no hay simulación que pueda contar como éxito.

---

## Fase E — Calidad y CI (Historia 3, P2)

**Objetivo**: ejecutar controles trazables localmente y en GitHub Actions, sin falsos aprobados.
**Prueba independiente**: cada job de CI informa resultado identificable y el resumen falla ante incumplimiento, cancelación, bloqueo o omisión obligatoria.

- [ ] T032 [US3] Crear scripts de orquestación local en `package.json`, `backend/pyproject.toml` y `scripts/check.ps1` para formato, lint, Pyright, unitarias, integración, contrato y E2E. Deps: T017, T020, T024, T028. Done: cada comando tiene nombre/resultado identificable, incluye `pyright --project backend/pyrightconfig.json` y no oculta controles no ejecutados. Refs: FR-006, FR-007, NFR-004; Historia 3.1.
- [ ] T033 [US3] Crear el primer workflow ejecutable en `.github/workflows/ci.yml` con todos los jobs obligatorios nominados `frontend-quality`, `backend-quality`, `contract`, `integration`, `e2e`, `secret-scan` y `dependency-audit` en pull requests y `main`; provisionar Playwright (`npx playwright install --with-deps`) y los servicios Compose/PostgreSQL reales para los jobs que los requieran. No se aceptan jobs vacíos ni marcadores de éxito. Deps: T032. Done: el primer workflow ejecutable contiene todos los jobs obligatorios, incluidos `secret-scan` y `dependency-audit`, cada uno con comando/punto de invocación real y resultado separable; una dependencia o configuración ausente se reporta `blocked` y falla, sin simular éxito. Refs: FR-006, FR-007, FR-010, NFR-003, NFR-004; Historia 3.2–3.3.
- [ ] T034 [US3] Configurar en `.github/workflows/ci.yml` el job `ci-summary` con `if: always()` y dependencias de todos los jobs obligatorios creados en T033. Deps: T033. Done: sólo acepta `success` con artefactos completos; `failure`, `cancelled`, `skipped` obligatorio, `blocked`, `not_run` o artefacto ausente producen salida y estado global fallido. Refs: FR-007, NFR-004; Historia 3.2–3.4.
- [ ] T035 [US3] Completar y validar el job `secret-scan` ya declarado en T033, con reglas en `.gitleaks.toml` (o herramienta equivalente fijada) para `.env.example`, código y documentación; mantenerlo conectado al resumen sin recrear el job. Deps: T002, T034. Done: el job declarado ejecuta un control real; hallazgos fallan el job, las salidas no muestran secretos y el resumen lo exige. Refs: FR-010, FR-007, NFR-003; Historia 3.5.
- [ ] T036 [US3] Completar y validar la matriz de auditoría del job `dependency-audit` ya declarado en T033 para los lockfiles frontend/backend, sin recrear el job ni declararlo opcional; conectarlo al resumen. Deps: T005, T006, T034. Done: cada lockfile existente tiene auditoría obligatoria desde el primer workflow; no se declara no aplicable después de creado el lockfile; falta de lockfile, herramienta o dependencia se reporta `blocked` y falla. Refs: FR-007, FR-010, NFR-004; Historia 3.2–3.4.
- [ ] T037 [US3] Configurar publicación sanitizada de logs/artefactos de fallo en `.github/workflows/ci.yml`, con `retention-days: 7` para artefactos, y pruebas de salida en `backend/tests/unit/test_logging.py`. Deps: T010, T033. Done: logs conservan `request_id` cuando aplique, excluyen secretos, cuerpos y PII y aplican la retención local/CI documentada; no se exportan a un almacén externo. Refs: FR-009, FR-010, FR-007; Historia 3.5.
- [ ] T038 [US3] Añadir casos de verificación de estados CI en `.github/workflows/ci.yml` y `README.md`: `success`, `failure`, `cancelled`, `skipped`, `blocked`, `not_run` y no aplicable temporal. Deps: T034, T035, T036, T037. Done: cada caso tiene una regla y un artefacto/salida verificable; el resumen nunca queda exitoso si falta un control obligatorio, incluso si otros jobs terminaron correctamente. Refs: FR-007, NFR-004; Historia 3.2–3.4.

**Checkpoint US3**: controles locales y CI son trazables y los resultados no aprobatorios quedan visibles.

---

## Fase F — Documentación, compatibilidad y verificación final

**Propósito**: cerrar evidencia reproducible de la feature sin ampliar el producto.

- [ ] T039 Actualizar `specs/001-project-foundation/quickstart.md` con comandos realmente implementados, versiones efectivas de lockfiles/digest y diagnóstico de Docker, puertos, CORS/preflight, configuración, timeout público, backend, PostgreSQL y observabilidad/retención. Deps: T021, T031, T032, T038. Done: ningún comando/documentación afirma existir antes de su implementación, todas las recuperaciones preservan datos salvo operación explícita y la retención local/CI coincide con `data-model.md`. Refs: FR-002, FR-008, FR-012, NFR-001, NFR-002, NFR-003.
- [ ] T040 [P] Actualizar `README.md` y `AGENTS.md` con alcance técnico real, prerrequisitos, enlaces a Quickstart/contrato, exclusiones explícitas de IA, 3D, audio/video, autenticación y negocio, y reglas generales para agentes sin referencias exclusivas a Codex. Deps: T023, T038. Done: README/AGENTS no prometen capacidades no implementadas y conservan trazabilidad a `001-project-foundation`. Refs: FR-008, FR-011, NFR-001, NFR-005.
- [ ] T041 Ejecutar la validación desde checkout limpio en Windows en una ruta con espacios y registrar resultado/limitaciones en `specs/001-project-foundation/quickstart.md`. Deps: T039. Done: se ejercitan preparación, inicio, detención y recuperación sin editar archivos versionados; cualquier bloqueo real se informa sin simular éxito. Refs: FR-002, FR-008, FR-012, NFR-001, NFR-002; Historia 1.1, 1.4.
- [ ] T042 Ejecutar el flujo de persistencia, recuperación y cleanup explícito en `specs/001-project-foundation/quickstart.md` y registrar evidencia de marcador, healthcheck, reinicio normal y limpieza por prefijo. Deps: T030, T039. Done: confirma el marcador tras reinicio, que la limpieza exige confirmación y conteo, y que volumen/datos no se destruyen silenciosamente; informa limitaciones reales. Refs: FR-005, FR-008, FR-012; Historia 2.5.
- [ ] T043 Ejecutar todos los controles locales y CI disponibles, registrar comandos, resultados y controles bloqueados en `specs/001-project-foundation/verification.md`. Deps: T038, T041, T042. Done: el registro incluye Pyright, CORS/preflight, auditoría y separa ejecutado, fallido, cancelado, omitido, bloqueado y no ejecutado; no declara pruebas inexistentes. Refs: FR-006, FR-007, FR-009, FR-010, NFR-004; Historia 3.
- [ ] T044 Auditar y registrar la compatibilidad efectiva de los lockfiles tempranamente resueltos, Node 24/Next/React, Python 3.13/FastAPI/SQLAlchemy/Alembic/Psycopg/Pyright, `postgres:18.6` por digest, Vitest/Playwright y validación OpenAPI en `specs/001-project-foundation/research.md` y `specs/001-project-foundation/verification.md`; registrar la política de actualización de dependencias. Deps: T005, T006, T024, T036, T043. Done: cada compatibilidad pendiente queda verificada contra las versiones efectivas o bloqueada con evidencia y decisión; no se inventan resultados y las actualizaciones siguen el procedimiento documentado. Refs: FR-006, FR-007, FR-011, NFR-004; pendientes de `research.md`.
- [ ] T045 Revisar trazabilidad final entre `spec.md`, `plan.md`, `tasks.md`, ADRs, contrato, Quickstart y `verification.md`; actualizar sólo referencias/documentación necesarias. Deps: T043, T044. Done: FR-001–FR-012, NFR-001–NFR-005 y todos los escenarios tienen evidencia o limitación explícita; no se agregan tareas fuera de alcance. Refs: todos los FR/NFR, Constitución I, XI y XII.

---

## Dependencias y orden de ejecución

```text
Fase A (T001–T006)
  └─> Fase B backend (T007–T017)
        └─> Fase C / US1 frontend-entorno (T018–T023)
              └─> Fase D / US2 integración (T024–T031)
                    └─> Fase E / US3 CI (T032–T038)
                          └─> Fase F verificación documental (T039–T045)
```

- **US1 (P1)** depende de la preparación y de los fundamentos que definen la configuración; se valida independientemente mediante checkout limpio y configuración segura.
- **US2 (P1)** depende de backend, frontend y Compose; se valida contra FastAPI/PostgreSQL reales, no mocks.
- **US3 (P2)** depende de comandos y pruebas reales de US1/US2; valida que CI informa y propaga estados correctamente.

## Oportunidades paralelas

- Tras T001: T002, T004, T005 y T006 pueden iniciar en paralelo; T005 y T006 llevan `[P]` porque usan lockfiles separados.
- T003 espera T002 porque consume el inventario de `.env.example`; no lleva `[P]`.
- T009 requiere T008 y T011 requiere T010 para validar lo que prueban; no llevan `[P]`.
- Tras T020: T022 puede ejecutarse en paralelo con T021; T027 requiere T025/T026 y no lleva `[P]`.
- Tras T033: T034, T035, T036, T037 y T038 se serializan porque comparten `.github/workflows/ci.yml`; ninguna lleva `[P]`.
- T021, T030 y T031 se serializan porque modifican `infra/compose.yaml`; T030 y T031 declaran T021 entre sus dependencias.
- T043 y T044 se serializan porque escriben `verification.md`; T044 declara T043 entre sus dependencias.
- T040 depende de T038 y puede ejecutarse en paralelo con T039 una vez completados T023 y T038, porque no comparten archivos.

## Cobertura de requisitos

| Requisitos | Tareas principales |
| --- | --- |
| FR-001 | T001, T007, T018, T023 |
| FR-002 | T003, T004, T021, T039, T041 |
| FR-003 | T002, T008, T009, T019, T022 |
| FR-004 | T014, T015, T024–T029 |
| FR-005 | T003, T012–T016, T030, T042 |
| FR-006 | T005, T006, T017, T020, T024, T032, T033, T043 |
| FR-007 | T032–T038, T043 |
| FR-008 | T007, T023, T039–T045 |
| FR-009 | T010, T011, T014, T015, T025, T037, T043 |
| FR-010 | T002, T008–T011, T029, T035, T037 |
| FR-011 | T001, T003–T007, T024, T040, T045 |
| FR-012 | T003, T008, T021, T026, T029–T031, T039, T041–T042 |
| NFR-001 | T002–T004, T007, T021, T039–T041 |
| NFR-002 | T003–T004, T012, T021, T041 |
| NFR-003 | T002, T008–T009, T019, T022, T035 |
| NFR-004 | T005–T006, T017, T020, T032–T038, T043–T044 |
| NFR-005 | T001, T004, T007, T018, T040, T045 |

## Estrategia de entrega

1. Completar Fases A y B para una base técnicamente válida.
2. Completar Fase C y verificar US1 desde checkout limpio.
3. Completar Fase D y verificar US2 contra servicios reales.
4. Completar Fase E y verificar US3 en CI.
5. Cerrar con Fase F y el registro veraz de resultados/limitaciones.

No se incluyen tareas de entrevistas, 3D/Three.js, IA, audio/video, autenticación, historial ni pagos.
