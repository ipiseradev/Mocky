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

> Como persona que desarrolla frontend o backend, quiero verificar una comunicación real entre aplicaciones mínimas ejecutables y la disponibilidad de la persistencia local, para detectar fallos de integración antes de trabajar en funcionalidades de producto.

**Por qué es P1**: Las fronteras entre componentes y la preparación de persistencia son parte central de la base Full Stack solicitada.

**Prueba independiente**: Con las aplicaciones mínimas del entorno local iniciadas, una comprobación realiza una comunicación efectiva desde el frontend hasta el backend, verifica la respuesta emitida por el backend y prueba los resultados de conexión, timeout y respuesta de error. Por separado, verifica que la persistencia local conserva datos de prueba tras reiniciar el servicio de base de datos.

**Escenarios de aceptación**:

1. **Dado** que las aplicaciones mínimas locales están ejecutándose, **cuando** el frontend realiza una solicitud al backend real, **entonces** recibe y verifica una respuesta producida por ese backend; una respuesta simulada o interceptada no cuenta como integración exitosa.
2. **Dado** que no se puede establecer la conexión con el backend, **cuando** el frontend ejecuta la comprobación, **entonces** informa un error de conexión distinto de un timeout y de una respuesta de error del backend.
3. **Dado** que el backend no responde dentro del límite finito configurado, **cuando** vence ese límite, **entonces** el frontend termina la espera e informa un timeout distinguible de un error de conexión y de una respuesta de error. El valor del límite se decidirá en Plan.
4. **Dado** que el backend responde con un resultado de error, **cuando** el frontend ejecuta la comprobación, **entonces** informa una respuesta de error distinguible de un error de conexión y de un timeout.
5. **Dado** un dato de prueba guardado en la persistencia local, **cuando** se reinicia el servicio de base de datos, **entonces** el dato sigue disponible mediante la comprobación documentada.

### Historia 3: Verificar cambios antes de integrarlos (Prioridad: P2)

> Como persona que revisa cambios, quiero que las verificaciones de calidad y seguridad disponibles se puedan ejecutar localmente y en CI, para recibir resultados consistentes y corregir fallos antes de integrar cambios.

**Por qué es P2**: La automatización reduce regresiones y mantiene una señal de calidad común para el equipo.

**Prueba independiente**: Se ejecutan los controles documentados localmente y se revisa que la CI informe resultados por control y falle si uno requerido falla.

**Escenarios de aceptación**:

1. **Dado** un cambio que satisface los controles configurados, **cuando** se ejecutan las verificaciones locales, **entonces** cada control informa su resultado de forma identificable.
2. **Dado** un cambio para el que las herramientas obligatorias están disponibles, **cuando** se ejecuta la CI, **entonces** cada control obligatorio se ejecuta realmente y presenta un resultado identificable.
3. **Dado** un control obligatorio que detecta incumplimientos, **cuando** se ejecuta la CI para un cambio, **entonces** el estado del control y el resultado global indican fallo y permiten identificar el control responsable.
4. **Dado** que un control obligatorio está bloqueado o no se ejecutó, **cuando** finaliza la CI, **entonces** ese estado queda informado explícitamente y no se presenta como aprobado ni como una ejecución exitosa.
5. **Dado** un error ocurrido durante una verificación, **cuando** se consulta su salida o los registros asociados, **entonces** se dispone de un identificador de correlación cuando aplique y no se exponen secretos ni contenido personal innecesario.

## Casos límite

- Docker no está instalado, no está iniciado o no tiene recursos disponibles: la guía informa el prerrequisito ausente y cómo comprobarlo.
- Un puerto local requerido ya está ocupado: el fallo identifica el servicio afectado y orienta a resolver el conflicto sin borrar datos.
- Una variable obligatoria está ausente, vacía o mal formada: el inicio falla con un diagnóstico seguro y accionable.
- El backend inicia antes de que PostgreSQL esté listo, o PostgreSQL no puede aceptar conexiones: el estado y la salida distinguen disponibilidad pendiente de fallo definitivo y permiten recuperación documentada.
- El frontend no puede alcanzar al backend por una dirección o configuración incorrecta: la comprobación identifica un error de conexión, distinto de timeout o respuesta de error.
- El backend no responde dentro del límite configurado: la comprobación termina en tiempo finito e informa un timeout; el valor del límite se define en Plan.
- El backend responde con error: la comprobación informa la respuesta como error y no la confunde con una conexión fallida ni con un timeout.
- Una respuesta de prueba simulada o interceptada reemplaza accidentalmente al backend local: esa respuesta no puede satisfacer el criterio de integración exitosa.
- Se ejecuta el flujo en una ruta de Windows con espacios o separadores propios de Windows: los pasos documentados siguen funcionando.
- La CI no puede acceder a un secreto o servicio opcional: el control afectado informa la dependencia; no registra el valor ni simula un resultado satisfactorio.
- Se reinicia el servicio local de persistencia: los datos de desarrollo que deban persistir se conservan; ningún paso de recuperación elimina datos silenciosamente.

## Requisitos

### Requisitos funcionales

- **FR-001**: El repositorio DEBE separar frontend y backend bajo `frontend/` y `backend/`, respectivamente. Esta feature PUEDE incluir aplicaciones mínimas ejecutables únicamente para iniciar los componentes y verificar la infraestructura, la comunicación efectiva frontend-backend y la persistencia local. Estas aplicaciones NO DEBEN implementar entrevistas, autenticación de producto, IA conversacional, avatares 3D ni otras funcionalidades de negocio; sus límites y responsabilidades internas se definirán en Plan.
- **FR-002**: El proyecto DEBE documentar un flujo repetible para preparar, iniciar, detener y recuperar el entorno local desde un checkout limpio, compatible con Windows y basado en Docker.
- **FR-003**: La configuración local DEBE obtenerse de archivos locales excluidos del versionado o de variables de entorno, nunca de archivos versionados con valores secretos. El repositorio DEBE proporcionar un ejemplo sin secretos reales; el inicio DEBE detectar configuración obligatoria ausente o inválida y dar instrucciones seguras para corregirla.
- **FR-004**: La comprobación de integración DEBE realizar una comunicación efectiva desde el frontend hasta el backend local en ejecución y verificar una respuesta producida por ese backend. Una respuesta simulada o interceptada NO DEBE contar como integración exitosa. La comprobación DEBE terminar dentro de un tiempo finito y distinguir errores de conexión, timeout y respuestas de error del backend. El protocolo, las rutas, los formatos y el valor del límite de espera se definirán en Plan.
- **FR-005**: El entorno local DEBE preparar PostgreSQL para uso de desarrollo y conservar los datos de desarrollo a través de un reinicio normal del servicio. El modelo de datos, la versión y el mecanismo concreto de persistencia quedan para Plan.
- **FR-006**: El proyecto DEBE documentar cómo ejecutar las herramientas seleccionadas para formato, lint, tipado estricto y pruebas unitarias, de integración y E2E según el riesgo. Las herramientas, comandos y niveles de prueba se eligen en Plan; no se define un umbral universal de cobertura.
- **FR-007**: La CI DEBE ejecutar realmente todos los controles obligatorios acordados para los cambios revisados; NO DEBE omitirlos silenciosamente. DEBE informar un resultado identificable por control. Un control que detecte incumplimientos DEBE informarse como fallido y provocar un resultado fallido para ese control. Los controles bloqueados o no ejecutados DEBEN informarse con ese estado y NO DEBEN presentarse como exitosos. La política de activación, bloqueo y efecto sobre el resultado global se definirá en Plan.
- **FR-008**: La documentación de inicio DEBE incluir prerrequisitos, configuración local, pasos de desarrollo en Windows y Docker, instrucciones para persistencia local, verificaciones, solución de errores comunes y límites conocidos.
- **FR-009**: Los componentes de la base DEBEN informar errores operativos de forma estructurada y con contexto suficiente para diagnóstico. Las operaciones que crucen componentes DEBEN propagar un identificador de correlación cuando corresponda.
- **FR-010**: Los logs y salidas de error NO DEBEN exponer secretos, valores de configuración sensibles, CV, transcripciones ni datos personales innecesarios.
- **FR-011**: La estructura inicial DEBE dejar documentadas responsabilidades claras para frontend, backend y persistencia. Todo servicio o infraestructura adicional DEBE vincularse a una necesidad de esta especificación y a una decisión justificada antes de incorporarse.
- **FR-012**: La guía y las verificaciones DEBEN contemplar fallos de Docker, errores de conexión, timeout y respuestas de error del backend, disponibilidad de PostgreSQL, rutas de Windows y configuración faltante sin eliminar datos de forma silenciosa.

### Requisitos no funcionales

- **NFR-001**: Una persona nueva DEBE poder reproducir el entorno desde un checkout limpio usando solo prerrequisitos y pasos documentados, sin editar archivos versionados ni depender de instrucciones tácitas.
- **NFR-002**: Los pasos de desarrollo DEBEN funcionar en Windows con Docker y manejar correctamente rutas con espacios.
- **NFR-003**: Ningún secreto real DEBE ser requerido para iniciar los componentes locales de base. Los secretos de integraciones opcionales deben limitarse a CI o configuración local protegida.
- **NFR-004**: Las comprobaciones de calidad locales y de CI DEBEN ser trazables, repetibles y producir mensajes que permitan localizar el control que falló.
- **NFR-005**: Los límites entre módulos DEBEN poder describirse y revisarse sin introducir servicios adicionales que no estén justificados por los requisitos aprobados.

### Trazabilidad de requisitos y aceptación

| Requisitos | Escenarios de aceptación | Criterios de éxito |
| --- | --- | --- |
| FR-001, FR-002, FR-008, FR-011, NFR-001, NFR-005 | Historia 1, escenario 1; Historia 2, escenario 1 | SC-001, SC-002 |
| FR-003, FR-010, NFR-003 | Historia 1, escenarios 2 y 3; Historia 3, escenario 5 | SC-001, SC-005 |
| FR-004, FR-009, FR-012 | Historia 2, escenarios 1 a 4; Historia 3, escenario 5 | SC-002, SC-005 |
| FR-005, FR-012 | Historia 2, escenario 5 | SC-003 |
| FR-006, FR-007, NFR-004 | Historia 3, escenarios 1 a 4 | SC-004 |
| NFR-002 | Historia 1, escenario 4 | SC-006 |

### Entidades relevantes

- **Configuración de desarrollo**: valores locales necesarios para iniciar y conectar los componentes; los valores secretos no forman parte del repositorio.
- **Estado de servicio local**: disponibilidad de frontend, backend y persistencia necesaria para verificar la integración.
- **Estado de persistencia de desarrollo**: datos de prueba usados para comprobar que el almacenamiento local sobrevive a un reinicio normal.
- **Resultado de verificación**: estado y salida identificable de un control local o de CI, sin valores sensibles.

## Criterios de éxito

- **SC-001**: En una ejecución desde checkout limpio en Windows, se completan el 100% de los pasos documentados de preparación sin pasos tácitos ni cambios a archivos versionados.
- **SC-002**: La comprobación frontend-backend produce el resultado esperado en sus cuatro escenarios: respuesta verificable del backend real, error de conexión, timeout finito y respuesta de error. Solo el primer escenario cuenta como integración exitosa y una respuesta simulada no puede satisfacerlo.
- **SC-003**: Un dato de prueba escrito en la persistencia local sigue siendo legible tras un reinicio normal del servicio de almacenamiento.
- **SC-004**: El 100% de los controles obligatorios muestra un estado identificable en CI. Cuando sus herramientas están disponibles, los controles se ejecutan realmente. Todo control que detecta incumplimientos se informa como fallido; los bloqueados o no ejecutados se identifican como tales y el conjunto no se presenta como completamente aprobado. La política concreta del estado global y los bloqueos se definirá en Plan.
- **SC-005**: Las salidas de los escenarios de configuración inválida y fallo de servicio contienen cero valores secretos y sí identifican una acción correctiva.
- **SC-006**: El flujo documentado de preparación completa una ejecución desde una ruta de Windows con espacios y otra desde una ruta sin espacios, sin errores de resolución de rutas.

## Supuestos

- El repositorio parte sin código de producto, módulos frontend/backend ni servicios locales ya configurados.
- La persona que desarrolla en Windows puede instalar o iniciar Docker según las instrucciones del equipo; los prerrequisitos definitivos se documentarán en Plan.
- PostgreSQL local se prepara solo para desarrollo. No se requiere un despliegue productivo ni migración de datos de usuarios en esta feature.
- La integración frontend-backend es una comprobación técnica básica y no implementa flujos de entrevista, usuarios ni autenticación de producto.
- Las aplicaciones mínimas permitidas en esta feature se limitan a verificaciones técnicas y no habilitan funcionalidades de producto.
- Los controles se definen según riesgo y disponibilidad real de herramientas. La especificación no exige instalar dependencias de producto durante esta etapa.

## Fuera de alcance

- Implementar aplicaciones frontend o backend de producto, APIs de negocio o interfaces de usuario. Se permiten únicamente las aplicaciones mínimas ejecutables limitadas por FR-001.
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
- Valor finito del límite de espera para la comprobación frontend-backend.
- Política de CI para controles bloqueados o no ejecutados y su efecto sobre el estado global.
- Campos permitidos en logs, esquema del identificador de correlación y retención de logs.
- Versiones soportadas de herramientas y procedimiento de actualización.

## Historial

- **2026-11-02**: primera versión para revisión, creada mediante la etapa Specify.
