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
2. El `SimulationService` genera una evolución temporal de 10 pasos.
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
- **[2026-04-20]:** Intento de ejecución del cliente Java mediante `./mvnw` fallido por falta de `maven-wrapper.properties`. Se recomienda usar `mvn` local o Docker.
- **[2026-04-20]:** Modificada la lógica de `EntidadMovimientoAdyacente` en `src/domain/entities/models.py` para restringir el movimiento a solo horizontal y vertical (Von Neumann neighborhood), eliminando los desplazamientos diagonales.
- **[2026-04-20]:** Refactorización arquitectónica: Se ha movido la lógica de movimiento de las entidades desde la capa de **Dominio** (`models.py`) a la capa de **Aplicación** (`simulation_service.py`), siguiendo un modelo de dominio anémico y centralizando la lógica de negocio en los casos de uso.
- **[2026-04-20]:** Documentado el flujo completo de la simulación: Recepción de solicitud -> Orquestación en `SimulationService` -> Cálculo de movimientos H/V y clonaciones -> Persistencia en Repositorio -> Descarga vía Ticket.
- **[2026-04-20]:** Análisis de concurrencia: Se propone el uso de `FastAPI BackgroundTasks` para desacoplar la solicitud de la simulación del cálculo intensivo de la misma, permitiendo respuestas asíncronas al cliente.
- **[2026-04-20]:** Actualizado `requirements.txt` con versiones concretas de las librerías (`fastapi==0.135.3`, `uvicorn[standard]==0.44.0`, `pydantic==2.13.0`, etc.) para asegurar la reproducibilidad del entorno.
- **[2026-04-20]:** Creado un `Dockerfile` optimizado para el backend utilizando **`uv`** como gestor de paquetes para mejorar la velocidad de construcción y la eficiencia de la imagen Docker.
- **[2026-04-20]:** Implementado un archivo `.dockerignore` para optimizar el contexto de construcción de Docker, excluyendo entornos virtuales, código del cliente y metadatos innecesarios.
