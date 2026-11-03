
# Mocky Backend

Backend técnico de Mocky, desarrollado con Python 3.13 y FastAPI.

## Responsabilidades

- Exponer una API HTTP mediante FastAPI.
- Mantener una arquitectura modular.
- Proporcionar endpoints técnicos de diagnóstico en las tareas correspondientes.
- Integrarse con PostgreSQL en futuras tareas de la fundación.

## Estructura

- `app/main.py`: creación y configuración de la aplicación FastAPI.
- `app/api/`: organización de routers y endpoints.
- `app/core/`: configuración y componentes técnicos compartidos.

## Desarrollo local

Desde la carpeta `backend`, con el entorno virtual y las dependencias instaladas:

```cmd
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Documentación interactiva:

http://127.0.0.1:8000/docs

## Estado actual

La aplicación FastAPI arranca correctamente.

El endpoint de integración con PostgreSQL está planificado, pero todavía no está implementado.

## Límites de esta etapa

No incluye autenticación, entrevistas, inteligencia artificial, avatares ni procesamiento multimedia.


## Documentación de referencia

- [Contrato de integración](../specs/001-project-foundation/contracts/integration-health.openapi.yaml)
- [Guía de inicio rápido](../specs/001-project-foundation/quickstart.md)