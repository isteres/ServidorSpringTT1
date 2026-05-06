# Contexto del Proyecto: Servidor de Simulación Hexagonal (TT1)

Este archivo proporciona una visión general del proyecto para facilitar la comprensión y el desarrollo.

## 🚀 Tecnologías y Frameworks
- **Lenguaje:** Python 3.x
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Validación de Datos:** Pydantic
- **Arquitectura:** Hexagonal (Puertos y Adaptadores)

## 🏗️ Estructura del Proyecto
El proyecto sigue una arquitectura limpia dividida en capas:

- **`src/domain/`**: Núcleo del negocio. Contiene las entidades (`models.py`) y lógica pura.
  - `Entidad`: Clase base abstracta para diferentes tipos de entidades (Estática, MovimientoAdyacente, EstáticaClon).
- **`src/application/`**: Casos de uso y puertos.
  - `ports/`: Interfaces (Abstract Base Classes) para entrada (use cases) y salida (repositories).
  - `use_cases/`: Implementación de la lógica de aplicación (`SimulationService`).
- **`src/infrastructure/`**: Detalles de implementación.
  - `adapters/`: Implementaciones concretas de los puertos de salida (ej. `InMemorySimulationRepository`).
  - `web/`: Punto de entrada de la API, controladores y rutas de FastAPI.
- **`src/main.py`**: Script de inicio del servidor.

## 🛠️ Funcionalidad Principal
El servidor gestiona simulaciones de entidades en un tablero bidimensional:
1. Se solicita una simulación enviando un diccionario de IDs de entidades y cantidades.
2. El `SimulationService` genera una evolución temporal con una duración dinámica (entre 10 y 30 pasos) según la cantidad de entidades.
3. Las entidades tienen comportamientos específicos definidos en sus clases (mover, clonar).
4. El resultado se guarda y se puede recuperar mediante un `ticket` numérico.

## 📍 Endpoints de la API
- `POST /simulation/solicitar`: Inicia una nueva simulación.
- `GET /simulation/descargar/{ticket}`: Obtiene los resultados de una simulación.
- `GET /entities`: Lista todas las entidades disponibles.
- `GET /entities/validate/{entity_id}`: Verifica si un ID de entidad es válido.

## 🧪 Pruebas
Las pruebas se encuentran en el directorio `tests/` y cubren tanto la lógica de aplicación como los endpoints de la API.

## 🏃 Cómo ejecutar
```bash
python src/main.py
```
El servidor se iniciará por defecto en `http://0.0.0.0:8000`.

## 📜 Historial de Cambios
- **[2026-04-20]:** Se habilita el registro de cambios en `GEMINI.md`.
- **[2026-04-20]:** Modificada la lógica de `EntidadMovimientoAdyacente` para restringir el movimiento a solo horizontal y vertical (Von Neumann).
- **[2026-04-20]:** **Refactorización Mayor:** La lógica de movimiento y clonación se traslada de las entidades del dominio al `SimulationService` para centralizar la gestión de colisiones y la regla FCFS.
- **[2026-04-20]:** **Implementación de Tests:** Se añaden 12 tests de integración y unitarios (sin mocks) que validan el estado inicial en t=0, la ausencia de colisiones y la preferencia por orden de llegada.
- **[2026-04-20]:** **Automatización CI:** Se crea una GitHub Action (`python-tests.yml`) para ejecutar los tests automáticamente en cada push/PR.
- **[2026-04-20]:** **Documentación:** Se enriquecen los metadatos de FastAPI y los esquemas de Pydantic para una documentación Swagger/ReDoc autodescriptiva.

## 🛠️ Funcionalidad Principal (Detalle Técnico)
1. **Estado Inicial (t=0):** Se garantiza una distribución aleatoria sin colisiones. El primer segundo de la simulación (`t=0`) representa el estado inicial exacto solicitado, sin movimientos ni clones.
2. **Evolución (t=1 a t=9):**
   - **Orden de Turno:** En cada paso, se baraja la lista de entidades (`random.shuffle`) para aplicar una política de FCFS (First-Come, First-Served) justa.
   - **Gestión de Espacio:** Se utiliza un set de `ocupadas_proximas` para reservar casillas en tiempo real, evitando solapamientos.
3. **Tipos de Movimiento:**
   - **Adyacente:** Solo casillas H/V libres.
   - **Clonación:** 80% de probabilidad, busca una casilla adyacente libre (H/V). El clon nunca pisa al progenitor.

## 🧪 Verificación
Para ejecutar la suite de pruebas:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python -m pytest tests/
```
- **[2026-04-20]:** Refactorización arquitectónica: Se ha movido la lógica de movimiento de las entidades desde la capa de **Dominio** (`models.py`) a la capa de **Aplicación** (`simulation_service.py`), siguiendo un modelo de dominio anémico y centralizando la lógica de negocio en los casos de uso.
- **[2026-04-20]:** Documentado el flujo completo de la simulación: Recepción de solicitud -> Orquestación en `SimulationService` -> Cálculo de movimientos H/V y clonaciones -> Persistencia en Repositorio -> Descarga vía Ticket.
- **[2026-04-20]:** Análisis de concurrencia: Se propone el uso de `FastAPI BackgroundTasks` para desacoplar la solicitud de la simulación del cálculo intensivo de la misma, permitiendo respuestas asíncronas al cliente.
- **[2026-04-20]:** Actualizado `requirements.txt` con versiones concretas de las librerías (`fastapi==0.135.3`, `uvicorn[standard]==0.44.0`, `pydantic==2.13.0`, etc.) para asegurar la reproducibilidad del entorno.
- **[2026-04-20]:** Creado un `Dockerfile` optimizado para el backend utilizando **`uv`** como gestor de paquetes para mejorar la velocidad de construcción y la eficiencia de la imagen Docker.
- **[2026-04-20]:** Implementado un archivo `.dockerignore` para optimizar el contexto de construcción de Docker, excluyendo entornos virtuales, código del cliente y metadatos innecesarios.
- **[2026-04-27]:** **Implementación de Persistencia SQL:** Se ha sustituido el repositorio en memoria por `SQLSimulationRepository` utilizando **SQLModel**.
- **[2026-04-27]:** **Soporte Multi-DB:** Configurada la infraestructura para soportar SQLite (por defecto) y MySQL mediante variables de entorno (`DATABASE_URL`).
- **[2026-04-27]:** **Orquestación con Docker Compose:** Creado `docker-compose.yml` para gestionar el ciclo de vida de la aplicación y una base de datos MySQL 8.0, incluyendo healthchecks y volúmenes persistentes.
- **[2026-04-27]:** **Gestión Visual de BD:** Añadido **Adminer** al stack de Docker para permitir la visualización y gestión de la base de datos vía web en el puerto 8081.
- **[2026-04-27]:** **Robustez de Conexión:** Implementada lógica de reintento en la inicialización de la base de datos para manejar el tiempo de arranque de contenedores DB en entornos Docker.
- **[2026-05-04]:** **Clonación Adyacente:** Se ha restringido la lógica de las entidades clonadoras para que solo generen clones en casillas adyacentes (H/V), unificando el comportamiento con el movimiento adyacente.
- **[2026-05-04]:** **Tabla de Usuarios:** Añadida tabla `users` y relación de clave foránea en `simulations` para anticipar futuras funcionalidades de gestión de clientes.
- **[2026-05-06]:** **Tiempo Dinámico:** Implementada la duración dinámica de la simulación. El tiempo (`max_t`) ahora se calcula según el número de entidades (1 paso por cada 5 entidades), con un mínimo de 10 y un máximo de 30 segundos.
- **[2026-05-06]:** **Tests de Persistencia:** Creada suite de tests de integración para la capa de infraestructura (`SQLSimulationRepository`) utilizando una base de datos SQLite en memoria, asegurando el correcto guardado y recuperación de datos JSON.
