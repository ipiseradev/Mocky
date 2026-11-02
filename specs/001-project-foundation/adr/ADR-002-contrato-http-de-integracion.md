# ADR-002: Comprobación HTTP real, acotada y correlacionada

- **Estado**: Aceptada para planificación
- **Fecha**: 2026-11-02
- **Contexto**: FR-004 exige comprobar frontend-backend con resultados distinguibles y finitos.

## Decisión

Un componente cliente de Next.js que corre en el navegador llamará por HTTP/JSON a `GET http://localhost:8000/api/v1/integration/health`, conforme a `contracts/integration-health.openapi.yaml`, con timeout leído de `NEXT_PUBLIC_INTEGRATION_TIMEOUT_MS` (predeterminado 3.000 ms, rango 1–10.000 ms). Usa `NEXT_PUBLIC_BACKEND_BASE_URL`, que sólo contiene esa URL pública local. Reenviará o generará `X-Request-ID`. El backend configura `CORSMiddleware` con `BACKEND_ALLOWED_ORIGINS`, métodos `GET`/`OPTIONS`, cabecera `X-Request-ID` y sin credenciales. Clasificará éxito real, `connection_error`, `timeout` y `backend_error`; sólo un `200` con `source: mocky-backend` cuenta como éxito. OpenAPI define únicamente las respuestas HTTP del backend (`200`, `503`/default); `connection_error` y `timeout` son clasificaciones locales del frontend, no respuestas modeladas por el contrato. No se incorpora proxy: `http://backend:8000` queda reservado para una eventual llamada de código servidor Next dentro de Compose, no para el navegador.

## Alternativas

- Mocks/interceptores: útiles para unitarias, inválidos como evidencia de integración.
- WebSocket/RPC: agregan protocolo y complejidad no requeridos.
- Sin timeout: puede dejar la comprobación bloqueada indefinidamente.

## Consecuencias y verificación

El contrato debe evolucionar compatiblemente. CORS permite sólo el origen local configurado, `GET`/`OPTIONS` y `X-Request-ID`, sin credenciales. Los tests de éxito deshabilitan interceptores; las pruebas fuerzan cada clase de fallo, verifican preflight/origen rechazado, cabecera/request_id, límite temporal configurado y ausencia de datos sensibles en salida.
