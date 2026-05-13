# Servidor de Simulación Hexagonal (TT1)

[![Python Tests](https://github.com/isteres/ServidorSpringTT1/actions/workflows/python-tests.yml/badge.svg)](https://github.com/isteres/ServidorSpringTT1/actions/workflows/python-tests.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

Este proyecto es un motor de simulación para la evolución de entidades en un tablero bidimensional. Está desarrollado siguiendo los principios de Clean Architecture y Arquitectura Hexagonal para garantizar un sistema desacoplado y fácil de testear.

## Arquitectura del Proyecto

La estructura se divide en capas según el patrón de Puertos y Adaptadores:

*   **Domain**: Define los modelos de datos y las entidades base.
*   **Application**: Contiene el servicio de simulación y las interfaces (puertos) necesarias para la comunicación entre capas.
*   **Infrastructure**: Implementa los detalles técnicos, como la API con FastAPI, la persistencia en base de datos (SQLModel/MySQL) y la integración con RabbitMQ para el procesamiento asíncrono.

## Lógica de Simulación y Procesamiento

El sistema gestiona las peticiones de forma desacoplada:
1.  **API (FastAPI)**: Recibe la solicitud, genera un ticket y encola la tarea en **RabbitMQ**.
2.  **Worker**: Un proceso independiente consume la cola, ejecuta el motor de simulación y guarda el resultado en la base de datos.
3.  **Persistencia**: Se utiliza **SQLModel** con soporte para SQLite y MySQL.

### Gestión de Colisiones (FCFS)
Para evitar que dos entidades ocupen el mismo lugar, se aplica una lógica de reserva de posiciones:
*   En cada segundo de la simulación, el orden en el que las entidades deciden su movimiento es aleatorio.
*   La primera entidad en procesarse reserva su casilla de destino, marcándola como ocupada para las demás.
*   Esto garantiza de forma estricta que nunca existan dos puntos en la misma coordenada.

## Tecnologías Utilizadas

*   **Lenguaje**: Python 3.11+
*   **Framework API**: FastAPI
*   **Validación**: Pydantic
*   **Pruebas**: Pytest
*   **CI/CD**: GitHub Actions para la ejecución automática de tests.

## Instalación y Uso

### Preparación del entorno
```bash
git clone https://github.com/isteres/ServidorSpringTT1.git
cd ServidorSpringTT1
pip install -r requirements.txt
```

### Ejecución del servidor
```bash
python src/main.py
```
El servidor arrancará en `http://localhost:8000`. Se puede acceder a la documentación interactiva en `/docs`.

## Pruebas de Sistema
Se han implementado tests de integración para validar la lógica de movimiento y la ausencia de colisiones en escenarios de alta densidad.

Para ejecutar los tests manualmente:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python -m pytest tests/
```

## Endpoints Principales

| Método | Endpoint | Función |
| :--- | :--- | :--- |
| `POST` | `/simulation/solicitar` | Crea una nueva simulación y devuelve un ticket. |
| `GET` | `/simulation/descargar/{ticket}` | Obtiene los resultados de la simulación. |
| `GET` | `/entities` | Lista los tipos de entidades disponibles. |
| `GET` | `/entities/validate/{id}` | Comprueba si un ID de entidad es válido. |

---
*Proyecto desarrollado para el Trabajo TT1 de Simulación de Sistemas.*
