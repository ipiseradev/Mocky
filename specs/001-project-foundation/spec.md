# Especificación: Fundamentos del proyecto Mocky

**Feature**: `001-project-foundation`  
**Rama**: `main` (no se creó una rama específica para esta feature)  
**Creada**: 2026-11-02  
**Estado**: Borrador para revisión  
**Entrada**: Definir requisitos verificables para la infraestructura inicial de Mocky.

## Historias de usuario y pruebas

### Historia 1: Preparar un entorno local reproducible (Prioridad: P1)

> Como persona que contribuye a Mocky, quiero preparar el entorno de desarrollo en Windows siguiendo instrucciones documentadas, para poder trabajar desde un checkout limpio sin adivinar pasos ni editar archivos compartidos con secretos.

**Por qué es P1**: El desarrollo de cualquier módulo depende de que el equipo pueda preparar y comprender el entorno de forma repetible.

**Prueba independiente**: En un checkout limpio de Windows con los prerrequisitos documentados disponibles, una persona sigue la guía, prepara la configuración local y verifica que los servicios de desarrollo quedan disponibles. No requiere funcionalidades del producto.

**Escenarios de aceptación**:

1. **Dado** un checkout limpio en Windows y los prerrequisitos documentados instalados, **cuando** una persona sigue la guía de desarrollo, **entonces** puede preparar, iniciar y detener el entorno sin pasos manuales no documentados; el repositorio contiene `frontend/` y `backend/` con sus responsabilidades descritas, la guía cubre prerrequisitos, configuración, verificaciones y solución de errores comunes, y cada servicio adicional propuesto tiene una necesidad y justificación documentadas.
2. **Dado** que la configuración local aún no existe, **cuando** la persona consulta la guía, **entonces** puede crearla a partir de un ejemplo sin introducir secretos en archivos versionados.
3. **Dado** que falta una variable de configuración obligatoria, **cuando** se inicia el entorno, **entonces** el error identifica la configuración faltante y cómo resolverla, sin revelar valores sensibles.
4. **Dado** un checkout ubicado en una ruta de Windows que contiene espacios, **cuando** la persona sigue el flujo documentado, **entonces** puede completar la preparación sin errores de resolución de rutas.

### Historia 2: Verificar la integración local (Prioridad: P1)

> Como persona que desarrolla frontend o backend, quiero verificar la comunicación básica entre ambos y la disponibilidad de la persistencia local, para detectar fallos de integración antes de trabajar en funcionalidades.

**Por qué es P1**: Las fronteras entre componentes y la preparación de persistencia son parte central de la base Full Stack solicitada.

**Prueba independiente**: Con el entorno local iniciado, una comprobación de integración confirma que el frontend puede comunicarse con el backend y que la persistencia PostgreSQL local está disponible y conserva datos de prueba tras reiniciar el servicio de base de datos.

**Escenarios de aceptación**:

1. **Dado** el entorno local disponible, **cuando** se ejecuta la comprobación documentada desde el frontend, **entonces** se recibe una respuesta verificable del backend.
2. **Dado** que el backend no está disponible, **cuando** se ejecuta la comprobación de integración, **entonces** se informa el fallo de conectividad con un mensaje accionable y sin bloquearse indefinidamente.
3. **Dado** un dato de prueba guardado en la persistencia local, **cuando** se reinicia el servicio de base de datos, **entonces** el dato sigue disponible mediante la comprobación documentada.

### Historia 3: Verificar cambios antes de integrarlos (Prioridad: P2)

> Como persona que revisa cambios, quiero que las verificaciones de calidad y seguridad disponibles se puedan ejecutar localmente y en CI, para recibir resultados consistentes y corregir fallos antes de integrar cambios.

**Por qué es P2**: La automatización reduce regresiones y mantiene una señal de calidad común para el equipo.

**Prueba independiente**: Se ejecutan los controles documentados localmente y se revisa que la CI informe resultados por control y falle si uno requerido falla.

**Escenarios de aceptación**:

1. **Dado** un cambio que satisface los controles configurados, **cuando** se ejecutan las verificaciones locales, **entonces** cada control informa su resultado de forma identificable.
2. **Dado** un control requerido que falla, **cuando** se ejecuta la CI para un cambio, **entonces** el estado de CI indica fallo y permite identificar el control responsable.
3. **Dado** un error ocurrido durante una verificación, **cuando** se consulta su salida o los registros asociados, **entonces** se dispone de un identificador de correlación cuando aplique y no se exponen secretos ni contenido personal innecesario.

## Casos límite

- Docker no está instalado, no está iniciado o no tiene recursos disponibles: la guía informa el prerrequisito ausente y cómo comprobarlo.
- Un puerto local requerido ya está ocupado: el fallo identifica el servicio afectado y orienta a resolver el conflicto sin borrar datos.
- Una variable obligatoria está ausente, vacía o mal formada: el inicio falla con un diagnóstico seguro y accionable.
- El backend inicia antes de que PostgreSQL esté listo, o PostgreSQL no puede aceptar conexiones: el estado y la salida distinguen disponibilidad pendiente de fallo definitivo y permiten recuperación documentada.
- El frontend no puede alcanzar al backend por una dirección o configuración incorrecta: la comprobación distingue el problema de conectividad de una respuesta de aplicación fallida.
- Se ejecuta el flujo en una ruta de Windows con espacios o separadores propios de Windows: los pasos documentados siguen funcionando.
- La CI no puede acceder a un secreto o servicio opcional: el control afectado informa la dependencia; no registra el valor ni simula un resultado satisfactorio.
- Se reinicia el servicio local de persistencia: los datos de desarrollo que deban persistir se conservan; ningún paso de recuperación elimina datos silenciosamente.

## Requisitos

### Requisitos funcionales

- **FR-001**: El repositorio DEBE separar el trabajo de frontend y backend bajo `frontend/` y `backend/`, respectivamente. La especificación de planificación definirá sus límites y responsabilidades internas; esta funcionalidad no requiere crear aplicaciones de producto.
- **FR-002**: El proyecto DEBE documentar un flujo repetible para preparar, iniciar, detener y recuperar el entorno local desde un checkout limpio, compatible con Windows y basado en Docker.
- **FR-003**: La configuración local DEBE obtenerse de archivos locales excluidos del versionado o de variables de entorno, nunca de archivos versionados con valores secretos. El repositorio DEBE proporcionar un ejemplo sin secretos reales; el inicio DEBE detectar configuración obligatoria ausente o inválida y dar instrucciones seguras para corregirla.
- **FR-004**: El entorno DEBE permitir una comprobación explícita de comunicación del frontend con el backend y distinguir una respuesta satisfactoria de fallos de conexión o de servicio. El protocolo, las rutas y los formatos concretos quedan para Plan.
- **FR-005**: El entorno local DEBE preparar PostgreSQL para uso de desarrollo y conservar los datos de desarrollo a través de un reinicio normal del servicio. El modelo de datos, la versión y el mecanismo concreto de persistencia quedan para Plan.
- **FR-006**: El proyecto DEBE documentar cómo ejecutar las herramientas seleccionadas para formato, lint, tipado estricto y pruebas unitarias, de integración y E2E según el riesgo. Las herramientas, comandos y niveles de prueba se eligen en Plan; no se define un umbral universal de cobertura.
- **FR-007**: La CI DEBE ejecutar los controles acordados de lint, tipado, pruebas y seguridad proporcional al riesgo para los cambios revisados, informar el resultado de cada control y fallar cuando falle un control requerido.
- **FR-008**: La documentación de inicio DEBE incluir prerrequisitos, configuración local, pasos de desarrollo en Windows y Docker, instrucciones para persistencia local, verificaciones, solución de errores comunes y límites conocidos.
- **FR-009**: Los componentes de la base DEBEN informar errores operativos de forma estructurada y con contexto suficiente para diagnóstico. Las operaciones que crucen componentes DEBEN propagar un identificador de correlación cuando corresponda.
- **FR-010**: Los logs y salidas de error NO DEBEN exponer secretos, valores de configuración sensibles, CV, transcripciones ni datos personales innecesarios.
- **FR-011**: La estructura inicial DEBE dejar documentadas responsabilidades claras para frontend, backend y persistencia. Todo servicio o infraestructura adicional DEBE vincularse a una necesidad de esta especificación y a una decisión justificada antes de incorporarse.
- **FR-012**: La guía y las verificaciones DEBEN contemplar fallos de Docker, conectividad backend, disponibilidad de PostgreSQL, rutas de Windows y configuración faltante sin eliminar datos de forma silenciosa.

### Requisitos no funcionales

- **NFR-001**: Una persona nueva DEBE poder reproducir el entorno desde un checkout limpio usando solo prerrequisitos y pasos documentados, sin editar archivos versionados ni depender de instrucciones tácitas.
- **NFR-002**: Los pasos de desarrollo DEBEN funcionar en Windows con Docker y manejar correctamente rutas con espacios.
- **NFR-003**: Ningún secreto real DEBE ser requerido para iniciar los componentes locales de base. Los secretos de integraciones opcionales deben limitarse a CI o configuración local protegida.
- **NFR-004**: Las comprobaciones de calidad locales y de CI DEBEN ser trazables, repetibles y producir mensajes que permitan localizar el control que falló.
- **NFR-005**: Los límites entre módulos DEBEN poder describirse y revisarse sin introducir servicios adicionales que no estén justificados por los requisitos aprobados.

### Trazabilidad de requisitos y aceptación

| Requisitos | Escenarios de aceptación |
| --- | --- |
| FR-003, FR-010, NFR-003 | Historia 1, escenarios 2 y 3; Historia 3, escenario 3 |
| FR-004, FR-009, FR-012 | Historia 2, escenarios 1 y 2 |
| FR-005, FR-012 | Historia 2, escenario 3 |
| FR-006, FR-007, NFR-004 | Historia 3, escenarios 1 y 2 |
| FR-009, FR-010 | Historia 3, escenario 3 |
| FR-001, FR-002, FR-008, FR-011, NFR-001, NFR-005 | Historia 1, escenario 1 |
| NFR-002 | Historia 1, escenario 4 |

### Entidades relevantes

- **Configuración de desarrollo**: valores locales necesarios para iniciar y conectar los componentes; los valores secretos no forman parte del repositorio.
- **Estado de servicio local**: disponibilidad de frontend, backend y persistencia necesaria para verificar la integración.
- **Estado de persistencia de desarrollo**: datos de prueba usados para comprobar que el almacenamiento local sobrevive a un reinicio normal.
- **Resultado de verificación**: estado y salida identificable de un control local o de CI, sin valores sensibles.

## Criterios de éxito

- **SC-001**: En una ejecución desde checkout limpio en Windows, se completan el 100% de los pasos documentados de preparación sin pasos tácitos ni cambios a archivos versionados.
- **SC-002**: La comprobación frontend-backend pasa sus dos escenarios definidos: respuesta del backend disponible y diagnóstico accionable cuando no está disponible.
- **SC-003**: Un dato de prueba escrito en la persistencia local sigue siendo legible tras un reinicio normal del servicio de almacenamiento.
- **SC-004**: El 100% de los controles requeridos para un cambio muestra un resultado identificable en CI; al fallar cualquier control requerido, el resultado global es fallido.
- **SC-005**: Las salidas de los escenarios de configuración inválida y fallo de servicio contienen cero valores secretos y sí identifican una acción correctiva.
- **SC-006**: El flujo documentado de preparación completa una ejecución desde una ruta de Windows con espacios y otra desde una ruta sin espacios, sin errores de resolución de rutas.

## Supuestos

- El repositorio parte sin código de producto, módulos frontend/backend ni servicios locales ya configurados.
- La persona que desarrolla en Windows puede instalar o iniciar Docker según las instrucciones del equipo; los prerrequisitos definitivos se documentarán en Plan.
- PostgreSQL local se prepara solo para desarrollo. No se requiere un despliegue productivo ni migración de datos de usuarios en esta feature.
- La integración frontend-backend es una comprobación técnica básica y no implementa flujos de entrevista, usuarios ni autenticación de producto.
- Los controles se definen según riesgo y disponibilidad real de herramientas. La especificación no exige instalar dependencias de producto durante esta etapa.

## Fuera de alcance

- Implementar aplicaciones frontend o backend, APIs de producto o interfaz de usuario.
- Implementar entrevistas, sesiones de audio/video, avatares 3D, Three.js, IA conversacional o evaluación laboral.
- Crear cuentas, autenticación de producto, historiales, personalización con CV, pagos o integraciones con proveedores externos.
- Definir infraestructura de producción, despliegues, escalado distribuido o servicios adicionales no justificados.

## Decisiones pendientes para Plan

Estas decisiones no bloquean la definición de necesidades y no se resuelven en esta etapa:

- Distribución de responsabilidades y límites concretos entre los módulos requeridos.
- Mecanismo de orquestación local con Docker y opciones de compatibilidad con Docker Desktop en Windows.
- Protocolo, rutas, formato de contrato y comportamiento de comprobación frontend-backend.
- Versión de PostgreSQL, gestión de configuración local y mecanismo de persistencia.
- Herramientas y comandos concretos de formato, lint, tipado y pruebas; proveedor y disparadores de CI.
- Campos permitidos en logs, esquema del identificador de correlación y retención de logs.
- Versiones soportadas de herramientas y procedimiento de actualización.

## Historial

- **2026-11-02**: primera versión para revisión, creada mediante la etapa Specify.
