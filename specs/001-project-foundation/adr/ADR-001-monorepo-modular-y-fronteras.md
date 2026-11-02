# ADR-001: Monorepo modular con frontend, backend y PostgreSQL

- **Estado**: Aceptada para planificación
- **Fecha**: 2026-11-02
- **Contexto**: FR-001 y FR-011 exigen fronteras claras; el repositorio no tiene código.

## Decisión

Usar un monorepo con `frontend/` (Next.js), `backend/` (FastAPI) e `infra/` (Docker Compose futuro), con PostgreSQL como único servicio de persistencia. El backend será un monolito modular, no una colección de microservicios.

## Alternativas

- Un único proyecto Next.js: reduce toolchains pero no satisface el backend Python previsto ni una frontera API explícita.
- Microservicios: aumentan despliegue, observabilidad y contratos sin requisito que lo justifique.
- PostgreSQL nativo en Windows: impone configuración específica de cada contribuyente.

## Consecuencias y verificación

Se mantienen dos toolchains y un contrato versionado. Se limita cada módulo a una responsabilidad y se verifica mediante árbol, contrato, pruebas de integración reales y revisión de dependencias. Futuras capacidades 3D/IA deberán entrar por especificación y ADR propios.
