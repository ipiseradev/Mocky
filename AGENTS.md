# Instrucciones para agentes

## Reglas operativas para agentes

- Consultá `.specify/memory/constitution.md` antes de cualquier cambio y las especificaciones vigentes en `specs/` antes de trabajar en el producto.
- Usá las skills de Spec Kit disponibles en `.agents/skills/speckit-*` y respetá el flujo constitution → specify → clarify → plan → tasks → analyze → implement → verify.
- No implementes funcionalidades sin una especificación aprobada. Si falta o es ambigua, seguí el flujo de la constitución y resolvé la definición antes de implementar.
- No instales dependencias salvo que sean necesarias para un alcance aprobado y estén justificadas.
- Limitá los cambios a los archivos necesarios para la tarea autorizada. No modifiques archivos fuera de alcance.
- No alteres `.specify/memory/constitution.md` sin autorización explícita del usuario.
- Ejecutá las verificaciones disponibles y pertinentes al cambio. No inventes pruebas, resultados, infraestructura ni funcionalidades; informá herramientas no disponibles y verificaciones no ejecutadas.
- Al finalizar, reportá archivos creados o modificados, verificaciones y resultados reales, y limitaciones relevantes.
- No asumas que existen módulos, herramientas o infraestructura que no estén presentes en el repositorio.
