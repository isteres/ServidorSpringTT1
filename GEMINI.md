# Contexto del Proyecto: Servidor de Simulación Hexagonal (TT1)

Este archivo proporciona una visión general del proyecto para facilitar la comprensión y el desarrollo.

## 🚀 Tecnologías y Frameworks
- **Lenguaje:** Python 3.x / Java 17 (Cliente)
- **Framework Web:** FastAPI (Backend) / Spring Boot (Cliente)
- **Servidor ASGI:** Uvicorn
- **Validación de Datos:** Pydantic
- **Arquitectura:** Hexagonal (Puertos y Adaptadores)

## 🏗️ Estructura del Proyecto
El proyecto sigue una arquitectura limpia dividida en capas:

- **`src/domain/`**: Núcleo del negocio. Contiene las entidades (`models.py`) y lógica pura.
- **`src/application/`**: Casos de uso y puertos.
- **`src/infrastructure/`**: Detalles de implementación (Adapters, Web).
- **`src/worker.py`**: Consumidor de RabbitMQ para procesamiento asíncrono.
- **`clienteJava/`**: Cliente Java/Spring Boot que consume la API del Backend.

## 🛠️ Funcionalidad Principal
El servidor gestiona simulaciones de entidades en un tablero bidimensional:
1. Se solicita una simulación. El sistema responde con un `ticket` y encola la tarea en **RabbitMQ**.
2. Un `worker` procesa la simulación de forma asíncrona.
3. El resultado se guarda en la base de datos SQL y se puede recuperar mediante el `ticket`.


## 📍 Endpoints de la API
- `POST /simulation/solicitar`: Inicia una nueva simulación.
- `GET /simulation/descargar/{ticket}`: Obtiene los resultados de una simulación.
- `GET /entities`: Lista todas las entidades disponibles.
- `GET /entities/validate/{entity_id}`: Verifica si un ID de entidad es válido.

## 🧪 Pruebas
Las pruebas se encuentran en el directorio `tests/` y cubren tanto la lógica de aplicación como los endpoints de la API.

## 📜 Historial de Cambios
- **[2026-05-18]:** **Integración del Cliente:** Se ha integrado el proyecto `proyectoCliente` (Java/Spring Boot) en el `docker-compose.yml` principal. Ahora todo el ecosistema (Frontend + Backend + Worker + DB + Broker) se levanta con un solo comando.
- **[2026-05-18]:** **Configuración Dinámica:** Se modificó `ContactoSim.java` para que la URL del servidor sea configurable mediante la variable de entorno `SIMULATION_SERVER_URL`, permitiendo la conexión interna en la red de Docker (`http://app:8000`).
- **[2026-05-18]:** **Corrección de Esquema:** Se solucionó un error 500 al solicitar simulaciones causado por una columna `status` faltante en la base de datos MySQL. Se resetearon las tablas para aplicar el nuevo esquema.
- **[2026-05-06]:** **Arquitectura Asíncrona con RabbitMQ:** Implementado sistema de procesamiento desacoplado.

## 🏗️ Ejecución Completa (Docker)
Para arrancar el sistema completo incluyendo el broker, el worker y el cliente:
```bash
docker-compose up --build
```
- **Backend API:** `http://localhost:8000`
- **Cliente Java:** `http://localhost:8080`
- **RabbitMQ Management:** `http://localhost:45672` (guest/guest)
- **Adminer (DB):** `http://localhost:8081`
