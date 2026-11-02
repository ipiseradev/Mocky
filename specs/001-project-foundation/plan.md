# Plan de implementación: Fundamentos del proyecto Mocky

**Feature**: `001-project-foundation` | **Fecha**: 2026-11-02 | **Spec**: [spec.md](spec.md)
**Rama de trabajo**: `main` (contexto de feature: `001-project-foundation`)

## Resumen

Establecer una base local reproducible para una aplicación web modular: `frontend/` con Next.js App Router y `backend/` con FastAPI, más PostgreSQL en Docker Compose. La primera implementación sólo contendrá comprobaciones técnicas: el frontend solicitará una ruta de diagnóstico del backend real, con tiempo de espera finito y estados distinguibles; el backend verificará su configuración y su dependencia de PostgreSQL. No se implementan capacidades de entrevista, autenticación, IA, audio/video ni 3D.

## Contexto técnico

| Área | Decisión de diseño |
| --- | --- |
| Lenguajes | TypeScript con `strict: true`; Python 3.13. |
| Frontend | Next.js 16.4.4 con React 19 y App Router; Tailwind CSS 4; ESLint 9 y Prettier 3; Vitest 4; Playwright 1.64.1. |
| Backend | FastAPI 0.162.0; Pydantic 2; SQLAlchemy 2.1.6; Alembic 1.20.1; `psycopg[binary]` 3; Ruff; Pyright; pytest. |
| Persistencia | PostgreSQL 18, contenedor oficial y volumen nombrado de Docker. El puerto de PostgreSQL no se publica en el host. |
| Orquestación | Docker Compose v2, invocado mediante `docker compose`; configuración desde `.env` local y variables de entorno. |
| Plataforma objetivo | Desarrollo local en Windows 11 con Docker Desktop/WSL2; CI en runners Linux alojados por GitHub. |
| Tipo | Monorepositorio web modular, un frontend, un backend monolítico y una base de datos; sin microservicios. |
| Integración | HTTP/JSON entre navegador/servidor de Next y FastAPI. Contrato en `contracts/integration-health.openapi.yaml`. CORS restringido a los orígenes configurados. |
| Límite de espera | `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` en el cliente frontend, con valor predeterminado 3.000 ms y rango válido 1–10.000 ms. El backend no valida ni consume este timeout. |
| Observabilidad | JSON estructurado en backend; `X-Request-ID` validado o generado y propagado en solicitudes/respuestas. `LOG_LEVEL` acepta `DEBUG`, `INFO`, `WARNING` y `ERROR` (predeterminado `INFO`). Métricas mínimas derivadas de logs/healthchecks: disponibilidad, errores y latencia (`duration_ms`), sin endpoint `/metrics`, proveedor externo ni almacén separado. Retención local: logs disponibles mientras exista el contenedor y descartados al eliminarlo, sin archivo propio; artefactos CI sanitizados con `retention-days: 7`. Sin cuerpos, secretos ni datos personales en logs. |
| Versionado | Las revisiones puntuales verificadas documentalmente están en `research.md`. El lockfile exacto y el digest de la imagen se resolverán durante Implement; Vitest, ESLint, Prettier, Ruff, Pyright y pytest quedan pendientes de la resolución conjunta del lockfile. Pyright se fijará en versión exacta en el lockfile del backend y usará `backend/pyrightconfig.json` con modo `standard`. |

## Verificación de Clarify

No existe un artefacto de Clarify con preguntas abiertas. El checklist de requisitos confirma que no hay marcadores `NEEDS CLARIFICATION`; las decisiones delegadas por `spec.md` quedaron resueltas en este plan, `research.md` y los ADRs. Por tanto, no bloquean el diseño.

## Constitution Check

### Antes de investigación — APROBADO

| Principio | Evidencia / puerta |
| --- | --- |
| I, XI | El plan deriva de `spec.md`, mantiene enlaces a todos los artefactos y no cambia la constitución. |
| II | Un frontend, un backend y PostgreSQL satisfacen el alcance. No se agregan colas, cachés, microservicios ni infraestructura de producción. ADR-001 registra el límite. |
| III | El contrato HTTP explícito define rutas, esquemas, errores y no autentica porque no hay recursos de usuario en el alcance. Tipado estricto y validación en los límites quedan como controles obligatorios. |
| IV, XII | Se planifican controles separados para formato, lint, tipos, unitarias, integración y E2E; CI no ocultará controles omitidos o bloqueados. |
| V, X | `.env.example` no tendrá secretos; configuración validada, listas de campos permitidos para logs, correlación sin PII, métricas mínimas derivadas de logs/healthchecks y retención local/CI definida. |
| VI–IX | IA, 3D, audio/video y accesibilidad de esos flujos quedan fuera de alcance; el plan no adelanta su implementación. |

### Después de diseño — APROBADO

`research.md`, el contrato y los ADRs conservan las fronteras y criterios verificables. No hay excepciones constitucionales ni complejidad que justificar.

## Arquitectura y responsabilidades

```text
Navegador
  │ solicitud de comprobación y X-Request-ID
  ▼
frontend/ (Next.js App Router)
  │ HTTP JSON, AbortController (timeout público)
  ▼
backend/ (FastAPI monolítico)
  │ SQLAlchemy / Alembic
  ▼
PostgreSQL 18 (Docker Compose + volumen nombrado)
```

- **Frontend**: interfaz mínima de diagnóstico y cliente de integración. Clasifica fallos de red, timeout y respuesta HTTP no exitosa; nunca simula respuesta del backend para declarar éxito.
- **Backend**: API técnica, validación de configuración y health/readiness. Conserva la lógica de infraestructura; no contiene dominio de entrevistas.
- **Persistencia**: PostgreSQL local para desarrollo. Compose espera healthcheck antes de dependientes y el volumen sobrevive `restart`, `stop` y `start` normales. El puerto de PostgreSQL no se publica en el host; sólo se publican el frontend y el backend en los puertos locales documentados.
- **Futuro 3D/IA**: se incorporarán como módulos internos detrás de interfaces de aplicación cuando una especificación aprobada defina su contrato, permisos, privacidad y presupuestos. No se reserva servicio ni proveedor ahora.

### Direccionamiento y configuración de red

La comprobación la inicia un componente cliente de Next.js que se ejecuta en el **navegador**. No se crea proxy ni Route Handler: el navegador realiza `GET http://localhost:8000/api/v1/integration/health` usando `NEXT_PUBLIC_BACKEND_BASE_URL=http://localhost:8000`. Esta variable es pública, queda incorporada al bundle de Next.js y por ello sólo puede contener la URL HTTP local, nunca credenciales ni la URL de PostgreSQL.

Cuando el frontend se ejecute en Compose, el valor anterior **no cambia para el navegador**: `localhost` se resuelve en la máquina Windows del usuario y alcanza el puerto publicado del backend. Si, en una evolución futura aprobada, código que se ejecuta dentro del servidor Next.js necesitara llamar al backend, usará exclusivamente `BACKEND_INTERNAL_URL=http://backend:8000`; es una variable privada y el nombre `backend` es el nombre del servicio de Compose. La comprobación actual no hace una segunda llamada desde el servidor Next.js.

El backend usará `DATABASE_URL=postgresql+psycopg://<usuario>:<contraseña-local>@postgres:5432/<base>`; `postgres` es el servicio Compose, no `localhost`. FastAPI configurará `CORSMiddleware` con `allow_origins` derivado exclusivamente de `BACKEND_ALLOWED_ORIGINS` (`http://localhost:3000` en desarrollo), `allow_methods=["GET", "OPTIONS"]`, `allow_headers=["X-Request-ID"]` y `allow_credentials=False`; no usará `*`. El preflight `OPTIONS` forma parte del contrato operativo porque el navegador envía `X-Request-ID`. Para usar otro host o puerto se cambian de forma coordinada el origen público y la lista permitida, sin exponer la URL interna. Estas reglas evitan los dos errores de espacio de nombres: un contenedor no usa `localhost` para otro contenedor y el navegador no intenta resolver `backend`.

## Decisiones y restricciones

Las decisiones con problema, alternativas, consecuencias y verificación están concentradas en [research.md](research.md) para evitar duplicación. Las decisiones difíciles de revertir están en [ADR-001](adr/ADR-001-monorepo-modular-y-fronteras.md), [ADR-002](adr/ADR-002-contrato-http-de-integracion.md) y [ADR-003](adr/ADR-003-configuracion-persistencia-y-observabilidad.md).

Restricciones invariables para Implement:

- No habrá autenticación ni autorización de producto hasta una feature aprobada; las rutas técnicas no exponen recursos de usuarios.
- No se registrarán valores de configuración, cabeceras de autorización, cuerpos HTTP, CV, transcripciones, audio ni vídeo.
- Los comandos documentados deben usar rutas entre comillas y rutas relativas a la raíz, aptas para Windows con espacios.
- La recuperación no ejecutará `docker compose down -v` ni eliminará volúmenes sin una acción explícita y advertida. La limpieza de marcadores técnicos será un comando separado, limitado por prefijo, con confirmación y conteo visible.
- Toda imagen y dependencia se fijará en lockfiles/digest durante Implement tras comprobar compatibilidad; Plan no instala ni resuelve paquetes. La auditoría de dependencias será obligatoria desde el primer lockfile y no podrá declararse no aplicable después de su creación.
- Las actualizaciones de dependencias se harán mediante PR dedicado, con lockfiles y digest actualizados, auditoría, pruebas, Pyright, CI y registro en `research.md`/`verification.md`; no se usarán rangos flotantes ni actualizaciones automáticas sin revisión.

## Criterios técnicos de aceptación

| Requisito | Criterio de aceptación técnico y evidencia prevista |
| --- | --- |
| FR-001 | Existen `frontend/` y `backend/` con README interno de responsabilidad; su contenido inicial se limita al diagnóstico técnico y no expone funcionalidades de producto. Revisión de árbol y contrato. |
| FR-002 | `quickstart.md` permite preparar, iniciar, detener y recuperar desde checkout limpio mediante Docker Compose, sin pasos tácitos. Prueba manual documentada en Windows. |
| FR-003 | El inventario de `data-model.md` es la fuente canónica: `.env.example` raíz contiene todas las claves y `frontend/.env.example` sólo deriva el subconjunto público, sin contradicciones ni secretos; el cargador valida presencia, formato, rango y `LOG_LEVEL` permitido sin imprimir valores. Pruebas unitarias de configuración inválida. |
| FR-004 | OpenAPI define las respuestas HTTP del backend (`200`, `503`/default) y su esquema; no modela fallos de transporte. El cliente frontend clasifica localmente `success`, `connection_error`, `timeout` configurable mediante `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` (predeterminado 3.000 ms, rango 1–10.000 ms) y `backend_error`. El backend configura CORS para `GET`/`OPTIONS` y `X-Request-ID`. Integración/E2E verifican cada clasificación y el preflight sin mocks para éxito. |
| FR-005 | La migración Alembic versionada crea `development_persistence_markers`; una prueba de integración del backend escribe y lee un marcador por conexión SQLAlchemy tras reinicio normal, sin endpoint público de escritura ni borrado del volumen. La limpieza es un comando explícito, filtrado por prefijo y con confirmación. |
| FR-006 | Documentación y scripts de CI separan format-check, lint, typecheck de frontend y backend (Pyright), pruebas unitarias, integración y E2E; cada comando produce estado identificable. |
| FR-007 | GitHub Actions ejecuta controles obligatorios en PR y `main`; cada job falla ante incumplimiento. `success`, `failure`, `cancelled`, `skipped`, `blocked` y `not_run` se representan de forma explícita; sólo `success` con artefactos completos aprueba el resumen global. |
| FR-008 | `quickstart.md` contiene prerrequisitos, configuración, Docker, persistencia, verificaciones, fallos habituales y límites. Revisión contra escenarios de Historia 1. |
| FR-009 | Backend emite JSON con `event`, `level`, `request_id`, `service` y resultado seguro; frontend reenvía `X-Request-ID`. Prueba de integración inspecciona cabecera, preflight, campos permitidos y correspondencia entre errores internos y contrato. |
| FR-010 | Pruebas de logging/configuración demuestran que los errores sólo nombran claves y acciones correctivas, nunca valores ni cuerpos. Revisión de esquema de log y de salidas sanitizadas de CI. |
| FR-011 | Plan, ADR-001 y árbol describen dependencias unidireccionales; cualquier servicio adicional exige spec/ADR antes de incorporarse. Revisión arquitectónica. |
| FR-012 | Quickstart documenta Docker no disponible, puerto ocupado, configuración inválida, CORS/preflight, PostgreSQL no listo, conexión, timeout, HTTP de error, rutas Windows, recuperación preservando datos y limpieza explícita de marcadores. |
| NFR-001 | Validación manual desde checkout limpio sigue sólo `quickstart.md` y registra cada paso/documentación faltante como defecto. |
| NFR-002 | La misma validación se ejecuta desde una ruta con espacios y otra sin espacios; comandos con comillas y Compose no dependen de separadores Unix. |
| NFR-003 | Inicio local no requiere credenciales externas; scanner de secretos y revisión de `.env.example` rechazan valores reales. PostgreSQL no se publica en el host y la configuración pública no contiene credenciales. |
| NFR-004 | CI expone jobs con nombres estables, artefactos/salidas por control y resumen final; repetir los comandos usa versiones bloqueadas. `ci-summary` falla si un resultado obligatorio falta, está bloqueado, fue cancelado, omitido o no ejecutado. |
| NFR-005 | Revisión confirma tres componentes y comunicación HTTP directa; no hay servicios distribuidos ni abstracciones prematuras. |

## Estructura propuesta

```text
.
├── frontend/                         # Se crea sólo en Implement
│   ├── src/app/                      # App Router y diagnóstico técnico
│   ├── src/lib/                      # Cliente HTTP, configuración y clasificación; pruebas unitarias co-locadas
│   ├── src/lib/*.test.ts             # Pruebas unitarias co-locadas
│   ├── tests/unit/                   # Pruebas unitarias adicionales
│   ├── tests/e2e/
│   ├── .env.example                  # Subconjunto público derivado del inventario canónico
│   └── README.md                     # Responsabilidad y comandos del frontend
├── backend/                          # Se crea sólo en Implement
│   ├── app/api/                      # Rutas técnicas
│   ├── app/core/                     # Configuración, logging y CORS
│   ├── app/db/                       # Sesión y modelos técnicos
│   ├── alembic/                      # Migraciones
│   ├── pyrightconfig.json            # Verificación estática Pyright
│   ├── README.md                     # Responsabilidad y comandos del backend
│   └── tests/{unit,integration,contract}/
├── infra/                            # Compose, Dockerfiles y ejemplos no secretos
├── scripts/                          # check.ps1, run-persistence-test.ps1 y cleanup-persistence-markers.ps1
├── package.json                      # Scripts raíz de orquestación local
├── .env.example                      # Inventario canónico local de configuración sin secretos
├── .gitleaks.toml                    # Reglas de escaneo de secretos
├── .github/workflows/                # CI futura
└── specs/001-project-foundation/
    ├── adr/
    ├── contracts/
    ├── data-model.md
    ├── plan.md
    ├── quickstart.md
    ├── research.md
    └── verification.md               # Evidencia real de Implement/Verify
```

**Decisión de estructura**: un monorepo con dos aplicaciones y una carpeta de infraestructura. No se crean directorios de código en esta etapa: el árbol es el destino de Implement.

## Estrategia de verificación y CI

| Capa | Controles previstos | Política |
| --- | --- | --- |
| Frontend | Prettier check, ESLint, `tsc --noEmit`, Vitest y Playwright | Obligatorios desde que exista `frontend/`; PR y `main`. |
| Backend | Ruff format check/lint, Pyright (`pyright --project backend/pyrightconfig.json`), pytest unitario e integración | Obligatorios desde que exista `backend/`; PR y `main`. |
| Integración | Validación OpenAPI, Compose, healthcheck PostgreSQL, `alembic upgrade head`, contrato HTTP real, preflight CORS y marcador tras reinicio | Obligatorio; job aislado que conserva sólo logs sanitizados. |
| Seguridad | Escaneo de secretos; auditoría de dependencias para cada lockfile | Escaneo obligatorio desde el primer workflow; auditoría obligatoria desde que exista cada lockfile (T005/T006), sin período de no aplicabilidad posterior. |

El primer workflow ejecutable se crea en T033 con todos los jobs obligatorios, incluidos `secret-scan` y `dependency-audit`; T035/T036 completan sus reglas y matriz de auditoría sin duplicar jobs. Los workflows no se crean aún. Sus jobs mostrarán un nombre por control y un job `ci-summary` ejecutado con `always()` y dependiente de todos. GitHub Actions aporta `success`, `failure`, `cancelled` y `skipped`; `blocked` y `not_run` se representan mediante un artefacto/salida por job con estado explícito y anotación sanitizada. Sólo `success` con todos los artefactos obligatorios presentes aprueba el resumen. `failure` y `cancelled` fallan. `skipped` de un control obligatorio falla; sólo puede aceptarse como no aplicable si el plan identifica previamente control, motivo, condición de activación y fecha/condición de retiro. Un prerrequisito ausente se reporta como `blocked`, el job concluye `failure` y nunca se convierte en `skipped` ni en éxito. Si falta el artefacto de un control obligatorio, el resumen lo trata como `not_run` y falla, incluso si otros jobs terminaron correctamente. No se exigirán umbrales de cobertura durante esta feature.

## Complejidad

No aplica: no hay violaciones de la Constitución que requieran justificación.
