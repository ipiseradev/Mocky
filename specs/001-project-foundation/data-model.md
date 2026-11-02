# Modelo de datos técnico

Este modelo sólo define datos de infraestructura para la primera implementación; no modela personas, entrevistas, CV, transcripciones ni sesiones de producto.

## Entidades

### Configuración de desarrollo

| Variable | Tipo / regla | Uso |
| --- | --- | --- |
| `DATABASE_URL` | URI `postgresql+psycopg://…@postgres:5432/…` obligatoria, no registrada | Conexión backend → servicio Compose `postgres`. |
| `POSTGRES_USER` | texto local de desarrollo, sin secreto real | Inicialización del contenedor PostgreSQL. |
| `POSTGRES_PASSWORD` | valor local de desarrollo, nunca un secreto real | Inicialización del contenedor PostgreSQL; no se registra. |
| `POSTGRES_DB` | nombre de base local | Inicialización del contenedor PostgreSQL. |
| `NEXT_PUBLIC_BACKEND_BASE_URL` | URL HTTP pública válida, sin credenciales ni secreto; predeterminada `http://localhost:8000` | Destino del navegador para la comprobación. |
| `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` | entero de 1 a 10.000; valor por defecto 3.000 | Límite de solicitud del cliente frontend; validado y consumido sólo en frontend. |
| `BACKEND_INTERNAL_URL` | URL HTTP privada `http://backend:8000`; no pública; opcional/futura | Sólo para código que corra dentro del servidor Next.js en una futura necesidad aprobada. |
| `BACKEND_ALLOWED_ORIGINS` | lista explícita separada por comas; predeterminada `http://localhost:3000` | Orígenes permitidos por `CORSMiddleware`; nunca `*`. |
| `LOG_LEVEL` | uno de `DEBUG`, `INFO`, `WARNING`, `ERROR`; predeterminado `INFO` | Nivel de salida estructurada del backend. Un valor ausente, vacío o fuera del conjunto falla al inicio con un diagnóstico seguro que nombra la clave y los valores permitidos, sin imprimir el valor recibido. |

No se persiste como tabla. Vive en variables de entorno o `.env` local ignorado. Los validadores sólo pueden informar el nombre de la clave y la regla incumplida. `POSTGRES_PASSWORD` es un valor local no sensible de desarrollo; cualquier secreto real queda fuera del repositorio. El backend no valida `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` porque no lo consume. El inventario anterior es la **fuente canónica única**: `.env.example` raíz contiene todas las claves y `frontend/.env.example` sólo deriva el subconjunto público `NEXT_PUBLIC_*`, sin contradecir tipos, valores predeterminados ni reglas. Cualquier alta o cambio se registra primero en este inventario, luego en los ejemplos, validadores y Quickstart.

El contrato operativo de CORS es `allow_origins=BACKEND_ALLOWED_ORIGINS`, `allow_methods=["GET", "OPTIONS"]`, `allow_headers=["X-Request-ID"]` y `allow_credentials=False`. Un origen no listado no debe recibir la cabecera CORS; el preflight `OPTIONS` es obligatorio para la comprobación del navegador.

OpenAPI describe únicamente las respuestas HTTP del backend (`200`, `503`/default) y su esquema. `connection_error` y `timeout` son resultados locales de la clasificación del cliente frontend, no respuestas del backend ni estados modelados por el contrato.

### Observabilidad mínima y retención

La feature satisface el mínimo de la Constitución X sin agregar infraestructura de métricas ni servicios externos:

- **Eventos**: solicitud HTTP técnica, healthcheck de servicio, error de configuración y cambio de disponibilidad de dependencia. Se representan con los campos permitidos de log y `X-Request-ID`.
- **Métricas mínimas**: disponibilidad por estado de healthcheck y `status_code` (200/503), errores por conteo de eventos con `status_code >= 400` o `error_code`, y latencia por `duration_ms`. Se obtienen de los logs estructurados y healthchecks; no hay endpoint `/metrics` ni almacén separado.
- **Retención local**: los logs viven en la salida del contenedor mientras éste exista; se descartan al eliminar/recrear el contenedor y no se archivan ni se envían a un proveedor. El estado de healthcheck es efímero.
- **Retención CI**: los artefactos sanitizados usan `retention-days: 7`; los logs de ejecución no se exportan a almacenamiento propio.

### Estado de servicio local

| Campo | Tipo / regla | Uso |
| --- | --- | --- |
| `service` | `frontend`, `backend` o `postgres` | Componente observado. |
| `status` | `ready`, `unavailable`, `error` | Estado técnico, no de producto. |
| `checked_at` | timestamp UTC opcional | Momento de observación; se expone como `checked_at` en el contrato cuando aplica. |
| `request_id` | UUID válido | Correlación de la operación HTTP cuando aplica. |
| `detail_code` | código seguro interno | Diagnóstico sin valores ni cuerpos; se serializa como `error.code` en respuestas de error. |

Es una representación efímera de una respuesta/comprobación, no una tabla de aplicación. El contrato OpenAPI es la fuente de los nombres públicos: `error.code` y `checked_at`; `detail_code` queda como nombre interno y no se expone crudo.

### Marcador de persistencia de desarrollo

| Campo | Tipo / regla | Uso |
| --- | --- | --- |
| `id` | UUID técnico, clave primaria | Identificador creado por la prueba de integración. |
| `label` | texto fijo con prefijo `persistence-test`, sin PII | Confirma lectura/escritura tras reinicio. |
| `created_at` | timestamp UTC | Diagnóstico de la prueba. |

La migración Alembic inicial crea la tabla `development_persistence_markers`. PostgreSQL contiene cero o más marcadores. La prueba de integración del backend, mediante sesión SQLAlchemy y sin ruta HTTP de escritura, ejecuta la migración, inserta/commitea un UUID nuevo, reinicia sólo PostgreSQL y abre otra sesión para leerlo. La eliminación es una acción explícita: el comando `scripts/cleanup-persistence-markers.ps1` selecciona únicamente filas con prefijo `persistence-test`, exige confirmación, muestra el conteo afectado y no ejecuta `truncate`, `down -v` ni limpieza silenciosa. Localmente se conserva el marcador para diagnóstico hasta que la persona ejecute ese comando; en CI el volumen efímero se elimina al final del job con una orden declarada en logs. Ninguna recuperación normal ejecuta limpieza.

### Resultado de verificación

| Campo | Tipo / regla | Uso |
| --- | --- | --- |
| `check_name` | identificador estable | Control local o de CI. |
| `status` | `passed`, `failed`, `blocked`, `not_run` | Resultado interno honesto. |
| `request_id` | UUID opcional | Correlación si el control cruza servicios. |
| `summary` | texto sanitizado | Acción o fallo, sin secretos/PII. |
| `executed_at` | timestamp UTC | Trazabilidad. |

### Representación de estados nativos de CI

| Estado nativo | Estado interno / efecto |
| --- | --- |
| `success` | `passed`; sólo es aprobatorio si existe el artefacto de resultado obligatorio. |
| `failure` | `failed`; falla el resumen. |
| `cancelled` | `failed`; falla el resumen y se registra como cancelado. |
| `skipped` | `failed` si el control es obligatorio; sólo una no aplicabilidad explícita, temporal y aprobada puede tolerarlo. |
| `blocked` | `blocked`; se publica como artefacto/anotación sanitizada, el job falla y el resumen falla. |
| `not_run` | `not_run`; se deriva de un artefacto ausente o de una salida explícita, y el resumen falla. |

El estado global sólo es aprobatorio cuando todos los controles obligatorios reportan `passed` y sus artefactos están presentes. `blocked`, `not_run`, `skipped` obligatorio, `cancelled` y `failure` nunca equivalen a `passed`.

## Transiciones permitidas

- Un servicio puede pasar de `unavailable` a `ready` cuando su healthcheck responde; de `ready` a `error` si falla una dependencia.
- Una comprobación inicia sin resultado y finaliza exactamente en `passed`, `failed`, `blocked` o `not_run`; `blocked` y `not_run` nunca equivalen a `passed` en el resumen de CI.
- El marcador permanece tras un reinicio normal del contenedor de PostgreSQL y sólo desaparece tras una operación explícita de limpieza.
