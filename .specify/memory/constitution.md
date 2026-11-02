# Constitución de ingeniería

**Proyecto:** Plataforma de preparación de entrevistas laborales
**Versión:** 1.1.0
**Estado:** Ratificada para iniciar la definición del producto
**Fecha de ratificación:** 2026-11-02

Esta constitución establece reglas obligatorias para especificar, diseñar, construir, verificar y operar el proyecto. “DEBE” y “NO DEBE” expresan requisitos; “DEBERÍA” expresa una recomendación que puede apartarse con justificación documentada. Las reglas aplican a código, especificaciones, automatizaciones y cambios operativos.

## Principios

### I. Desarrollo guiado por especificaciones

- Todo cambio de producto DEBE estar vinculado a una especificación aprobada antes de implementarse. La especificación DEBE describir necesidad, alcance, comportamiento observable, restricciones, privacidad, criterios de aceptación y riesgos pertinentes.
- Los cambios que alteren contratos o decisiones de producto DEBEN actualizar la especificación correspondiente. No se DEBEN inferir requisitos faltantes como si fueran decisiones aprobadas.
- **Verificación:** cada cambio revisable identifica su especificación y demuestra cómo satisface sus criterios; una revisión sin especificación se devuelve a definición.

### II. Arquitectura modular, responsabilidades claras y prohibición de sobreingeniería

- Cada módulo DEBE tener una responsabilidad explícita y dependencias dirigidas de forma comprensible. Las fronteras entre frontend, backend, persistencia e integraciones DEBEN documentarse cuando afecten contratos o seguridad.
- La solución DEBE ser la más simple que satisfaga requisitos aprobados. NO DEBE introducir microservicios, Kubernetes, Redis, colas, sistemas de pago, análisis facial ni otra infraestructura o capacidad sin necesidad documentada, comparación de alternativas y decisión registrada.
- **Verificación:** el plan y el árbol de cambios permiten identificar responsabilidades, dependencias y justificación de cada componente nuevo; las decisiones arquitectónicas significativas tienen ADR.

### III. Contratos API explícitos, validación de datos y tipado estricto

- Toda API DEBE especificar rutas, métodos, esquemas de solicitud y respuesta, errores, autenticación/autorización y compatibilidad. Los datos externos DEBEN validarse en el límite de confianza.
- El frontend previsto (Next.js, React y TypeScript) DEBE usar tipado estricto; el backend previsto (Python y FastAPI) DEBE declarar y validar modelos de entrada y salida. Los contratos compartidos DEBEN tener una fuente verificable y no duplicarse de forma divergente.
- **Verificación:** contrato documentado o generado, validación de entradas inválidas y typecheck/lint configurados y ejecutados cuando las herramientas estén instaladas. No se exigen herramientas ausentes.

### IV. Pruebas según riesgo y reporte veraz

- Los cambios DEBEN incluir pruebas unitarias para lógica aislable, pruebas de integración para fronteras relevantes y pruebas E2E para recorridos críticos, elegidas según riesgo y alcance. Los criterios y el nivel de prueba DEBEN quedar en la especificación o plan.
- Las pruebas simuladas, omitidas o no ejecutadas NO DEBEN declararse como ejecutadas ni como evidencia de aprobación. Toda limitación de entorno DEBE registrarse con claridad.
- **Verificación:** se informa el comando/herramienta realmente ejecutado, resultado y alcance; la revisión comprueba que las pruebas cubren criterios de aceptación y fallos relevantes.

### V. Seguridad, autorización y privacidad de datos

- Toda lectura o modificación de recursos DEBE autorizarse en el servidor según usuario, recurso y acción; conocer un identificador NO DEBE otorgar acceso. Los secretos DEBEN gestionarse fuera del código y del control de versiones.
- CV, transcripciones y datos personales DEBEN minimizarse, protegerse en tránsito y almacenamiento, limitarse a finalidades declaradas y eliminarse al vencer el propósito o la solicitud aplicable. Su recopilación, conservación y uso DEBEN estar sujetos a consentimiento y autorización explícitos según corresponda.
- El video del candidato NO DEBE grabarse ni enviarse por defecto. Cámara y micrófono requieren permisos claros y una acción informada del usuario. Los registros NO DEBEN contener secretos ni contenido sensible innecesario.
- **Verificación:** revisión de autorización por recurso, flujos de consentimiento/eliminación y límites de retención; análisis de dependencias y secretos proporcional al riesgo, cuando haya herramientas disponibles.

### VI. IA responsable y evaluación trazable

- El rol de entrevistador (generar preguntas y repreguntas durante la conversación) DEBE estar separado del rol de evaluador (analizar después de la conversación). El evaluador DEBE usar rúbricas explícitas, asociar conclusiones con evidencia textual autorizada y expresar incertidumbre o falta de evidencia.
- El sistema NO DEBE inferir aptitud laboral ni puntajes por apariencia, acento, emoción, identidad protegida o señales faciales. NO DEBE presentar inferencias como hechos ni emitir decisiones de contratación.
- La evaluación DEBE ser explicable, revisable por el usuario y limitada al propósito de práctica declarado. El uso de CV o transcripción requiere autorización y retención definida.
- **Verificación:** especificación de cada flujo identifica rol, entradas autorizadas, rúbrica, evidencia y manejo de incertidumbre; pruebas/revisión confirman la ausencia de señales prohibidas en criterios de evaluación.

### VII. Audio y tiempo real resilientes

- La sala DEBE modelar estados de sesión y transiciones válidas, incluidos permisos, conexión, escucha/habla, pausa, finalización, error y reconexión cuando apliquen. Las acciones de cancelación y finalización DEBEN detener trabajo asociado de forma predecible.
- Cada especificación de tiempo real DEBE definir métricas y presupuestos de latencia apropiados al flujo, describir cómo medirlos y establecer reconexión, límites de uso, manejo de fallos y recuperación. No se fija un umbral universal antes de medir y decidirlo.
- **Verificación:** pruebas de transiciones, cancelación, desconexión/reconexión y límites; resultados de latencia medidos contra presupuestos definidos para ese alcance.

### VIII. Three.js y rendimiento 3D

- Los recursos de Three.js/React Three Fiber DEBEN liberarse al desmontar o reemplazar escenas. La carga de la experiencia 3D DEBERÍA ser diferida para no bloquear funciones esenciales.
- Cada especificación que incluya 3D DEBE definir dispositivos y condiciones de medición, presupuestos de rendimiento y un fallback funcional. Debe incluir pruebas en dispositivos móviles objetivo; los umbrales se deciden a partir de mediciones, no se presuponen aquí.
- **Verificación:** inspección de ciclo de vida de recursos, mediciones reproducibles contra los presupuestos acordados y comprobación del fallback y recorrido móvil.

### IX. Accesibilidad y alternativas

- La conversación por voz DEBE ofrecer subtítulos legibles y sincronizados. Las acciones principales DEBEN poder usarse con teclado y comunicar foco, estado y errores.
- Los permisos de cámara y micrófono DEBEN explicarse antes de solicitarlos. La experiencia DEBE ofrecer una alternativa accesible cuando la cámara, el micrófono o WebGL no estén disponibles o sean rechazados. La alternativa a WebGL DEBE permitir completar la entrevista sin la escena 3D; la alternativa al micrófono DEBE permitir participar mediante texto. La cámara local no implica grabación ni transmisión.
- **Verificación:** recorrido de teclado y revisión de subtítulos, mensajes de permiso, errores y alternativas con cámara/micrófono denegados y WebGL no disponible.

### X. Observabilidad con minimización de datos

- Los servicios DEBEN producir logs estructurados y usar identificadores de correlación para seguir una operación entre componentes. Las métricas DEBEN cubrir disponibilidad, errores y latencia de flujos relevantes sin registrar contenido sensible.
- Los logs NO DEBEN incluir secretos, CV, transcripciones, audio, video ni identificadores personales innecesarios. Cada especificación DEBE definir qué eventos y métricas hacen falta y su retención.
- **Verificación:** inspección de ejemplos de logs y métricas, propagación de correlación y comprobación de que no se registran cargas sensibles ni credenciales.

### XI. Documentación y trazabilidad

- Cada cambio DEBE conservar trazabilidad entre especificación, plan, tareas, implementación y verificación. Las decisiones técnicas significativas o difíciles de revertir DEBEN registrarse en ADR con contexto, opciones y consecuencias.
- El README DEBE mantenerse alineado con capacidades y procedimientos reales. La documentación NO DEBE afirmar que existen sistemas o funciones aún no implementados.
- **Verificación:** revisión de enlaces entre artefactos, ADR cuando corresponda y exactitud del README respecto del estado del repositorio.

### XII. Git, revisión y CI

- Los commits DEBERÍAN seguir Conventional Commits. Todo cambio de producto DEBE revisarse antes de integrarse y la revisión DEBE considerar requisitos, seguridad, privacidad, accesibilidad, pruebas y documentación pertinentes.
- La CI DEBE ejecutar lint, typecheck y pruebas disponibles, además de controles de seguridad proporcionales al riesgo. Los controles obligatorios y sus herramientas se incorporan cuando estén disponibles; no se exige un comando ni una herramienta que no esté instalada.
- **Verificación:** evidencia de revisión y resultados reales de CI; los controles ausentes o bloqueados se informan, no se simulan.

## Alcance obligatorio del MVP y objetivos futuros

El MVP deberá especificarse antes de implementarse. Su alcance obligatorio incluye una entrevista simulada con entrevistador virtual 3D, conversación por voz, preguntas y repreguntas adaptativas, subtítulos legibles y sincronizados y controles explícitos para iniciar y finalizar la sesión. La evaluación se realiza después de la conversación, separada del rol entrevistador, y se basa en criterios explícitos y evidencias textuales autorizadas, con incertidumbre cuando la evidencia sea insuficiente. La experiencia DEBE permitir completar la entrevista sin cámara, micrófono o WebGL: la cámara es opcional y no se graba ni envía por defecto, el micrófono puede sustituirse por interacción textual y la escena 3D debe tener una alternativa accesible. El MVP debe respetar consentimiento, minimización, autorización y eliminación para los datos que efectivamente recopile.

Cada especificación del MVP DEBE precisar qué datos usa, el consentimiento requerido, retención y eliminación, estados y recuperación de sesión, criterios de accesibilidad, riesgos y verificación. DEBE definir presupuestos de latencia, rendimiento 3D y costos de uso solo para los flujos que lo requieran, junto con método, entorno y medición. Esta constitución no fija umbrales de latencia, FPS, cobertura ni costos.

Son objetivos futuros, sujetos a especificación y decisión expresa: persistencia de historial, uso de CV para personalización, múltiples idiomas, paneles de progreso, integraciones externas, monetización y funciones avanzadas, así como escalado a infraestructura distribuida. Quedan fuera del MVP inicial y no son prerrequisitos salvo decisión posterior documentada en una especificación aprobada. No se debe recopilar CV si el flujo no lo necesita.

## Flujo obligatorio de trabajo

Todo cambio de producto DEBE seguir, en este orden, el flujo:

1. **constitution:** consultar esta constitución y resolver conflictos antes de avanzar.
2. **specify:** definir alcance, requisitos y criterios de aceptación en una especificación.
3. **clarify (cuando aplique):** resolver ambigüedades que afecten comportamiento, seguridad, privacidad, arquitectura o aceptación; registrar decisiones y supuestos.
4. **plan:** describir diseño, límites, riesgos, datos, pruebas y verificación.
5. **tasks:** desglosar el trabajo en tareas trazables y revisables.
6. **analyze:** revisar consistencia de requisitos, plan y tareas, incluyendo conflictos con esta constitución.
7. **implement:** realizar solo el alcance aprobado y actualizar artefactos afectados.
8. **verify:** ejecutar controles disponibles y reportar evidencia, resultados y limitaciones reales.

Los nombres describen etapas, no comandos. Se DEBE usar Spec Kit si está instalado y sus convenciones locales aplicables; no se DEBEN exigir comandos, plugins o herramientas ausentes. Si Spec Kit no está instalado, se registra como paso de preparación del flujo de trabajo y se sigue el orden documental sin inventar su instalación ni sus archivos.

## Gobernanza y cumplimiento

Esta constitución es la autoridad normativa del proyecto para ingeniería. En caso de conflicto, se detiene el cambio afectado y se resuelve mediante una enmienda o una excepción antes de implementar. Una especificación puede restringir más, pero no relajar esta constitución sin aprobación y registro explícitos.

Una excepción DEBE documentar principio afectado, motivo, alcance, riesgo, mitigaciones, responsable, aprobación y fecha o condición de expiración. Las excepciones temporales DEBEN revisarse al vencer; una excepción no modifica por sí sola la constitución.

Las enmiendas DEBEN proponer texto y motivo, evaluar impacto sobre especificaciones y trabajo en curso, recibir revisión de responsables del proyecto y registrarse en el historial de cambios de este documento. La versión sigue SemVer: **MAJOR** para incompatibilidades normativas, **MINOR** para principios o requisitos nuevos compatibles y **PATCH** para aclaraciones que no cambian obligaciones. La versión y fecha vigentes aparecen al inicio.

La constitución DEBE revisarse al ratificar cambios de alcance del producto, tras incidentes relevantes de seguridad o privacidad y periódicamente durante el desarrollo. Cada revisión registra fecha, versión y resultado, aunque no produzca cambios. La ratificación inicial corresponde a la fecha indicada en el encabezado.

Un cambio cumple cuando sus criterios de aceptación y verificaciones aplicables están satisfechos, la trazabilidad está presente, los controles ejecutados se reportan con veracidad y las excepciones vigentes están documentadas. El responsable de revisión DEBE señalar incumplimientos antes de integrar. No se puede declarar cumplimiento basándose en verificaciones simuladas o no ejecutadas.

## Historial de cambios

- **1.1.0 — 2026-11-02:** precisión de los requisitos obligatorios del MVP y de las alternativas accesibles sin cámara, micrófono o WebGL; se mantiene la fecha de ratificación original.
- **1.0.0 — 2026-11-02:** ratificación inicial de los doce principios, el flujo de trabajo y las reglas de gobernanza.
