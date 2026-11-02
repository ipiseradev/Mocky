# Mocky

Mocky es una plataforma en planificación para practicar entrevistas laborales mediante entrevistas simuladas con inteligencia artificial y un entrevistador virtual 3D.

## Objetivo y alcance previsto

El MVP previsto permitirá realizar entrevistas simuladas con conversación por voz, preguntas y repreguntas adaptativas, subtítulos y control de inicio y finalización. Incluirá un entrevistador virtual 3D y alternativas accesibles cuando no se disponga de cámara, micrófono o WebGL. La evaluación ocurrirá después de la entrevista, separada de la conversación y basada en criterios explícitos y evidencias autorizadas.

La cámara será opcional y no se grabará ni enviará por defecto. Historial persistente, personalización mediante CV, monetización y funciones avanzadas quedan fuera del MVP inicial, salvo decisión posterior documentada en una especificación aprobada.

## Estado del desarrollo

El proyecto está en preparación documental. La constitución de ingeniería versión 1.1.0 y las instrucciones para agentes definen la gobernanza. La feature `001-project-foundation` tiene especificación, plan, investigación, modelo, contrato, ADRs y 45 tareas aprobadas; Analyze fue ejecutado y sus hallazgos documentales, incluido el cierre N-01–N-07, quedaron resueltos. No hay funcionalidades de producto implementadas ni una especificación de producto aprobada todavía.

## Arquitectura propuesta

La arquitectura está prevista, no implementada:

- **Frontend:** Next.js, React, TypeScript, React Three Fiber y Three.js para la experiencia web y el entrevistador 3D.
- **Backend:** Python y FastAPI para las APIs y la lógica de aplicación.
- **Persistencia prevista:** PostgreSQL, sujeta a especificación y decisión de alcance.
- **IA conversacional:** componentes para entrevista adaptativa y evaluación posterior, con responsabilidades separadas.

No se han creado estas aplicaciones, servicios ni dependencias. Las decisiones y límites técnicos se concretarán en especificaciones aprobadas antes de implementar.

## Metodología

Mocky sigue Specification-Driven Development. Los cambios de producto deben recorrer el flujo establecido en [la constitución](.specify/memory/constitution.md): constitution → specify → clarify (cuando aplique) → plan → tasks → analyze → implement → verify. Spec Kit está instalado y sus skills para agentes están disponibles en `.agents/skills/`; los artefactos de la feature `001-project-foundation` están en `specs/001-project-foundation/`.

## Contribuir

Antes de contribuir, consultá [AGENTS.md](AGENTS.md), la constitución y las especificaciones aprobadas. No implementes funcionalidades sin una especificación aprobada. Las instrucciones concretas de instalación, desarrollo y verificación se documentarán cuando existan las herramientas y componentes correspondientes; no hay comandos de producto disponibles en esta etapa.
