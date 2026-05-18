# Servidor de Simulación Hexagonal (TT1)

[![Python Tests](https://github.com/isteres/ServidorSpringTT1/actions/workflows/python-tests.yml/badge.svg)](https://github.com/isteres/ServidorSpringTT1/actions/workflows/python-tests.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

Este proyecto es un motor de simulación para la evolución de entidades en un tablero bidimensional. Está desarrollado siguiendo los principios de Clean Architecture y Arquitectura Hexagonal para garantizar un sistema desacoplado y fácil de testear.

## Arquitectura del Proyecto

La estructura se divide en capas según el patrón de Puertos y Adaptadores:

*   **Domain**: Define los modelos de datos y las entidades base.
*   **Application**: Contiene el servicio de simulación y las interfaces (puertos) necesarias para la comunicación entre capas.
*   **Infrastructure**: Implementa los detalles técnicos, como la API con FastAPI, la persistencia en base de datos (SQLModel) y el procesamiento asíncrono con RabbitMQ.

## Lógica de Simulación

El motor calcula una evolución temporal dinámica (entre 10 y 60 pasos) por cada petición. Se gestionan tres comportamientos distintos:

1.  **Entidad Estática**: No realiza ningún movimiento y mantiene su posición inicial.
2.  **Movimiento Adyacente**: Se desplaza a casillas contiguas (Norte, Sur, Este u Oeste). No se permiten movimientos diagonales (Von Neumann).
3.  **Entidad Estática Clon**: Se mantiene en su sitio pero tiene una probabilidad del 10% de generar un nuevo clon en una casilla adyacente libre (H/V).

### Gestión de Colisiones (FCFS)
Para evitar que dos entidades ocupen el mismo lugar, se aplica una lógica de reserva de posiciones:
*   En cada segundo de la simulación, el orden en el que las entidades deciden su movimiento es aleatorio.
*   La primera entidad en procesarse reserva su casilla de destino, marcándola como ocupada para las demás.
*   Esto garantiza de forma estricta que nunca existan dos puntos en la misma coordenada.

## Tecnologías Utilizadas

*   **Lenguaje**: Python 3.11+
*   **Framework API**: FastAPI
*   **Validación**: Pydantic
*   **Base de Datos**: SQLModel (SQLite/MySQL)
*   **Broker**: RabbitMQ
*   **Pruebas**: Pytest
*   **CI/CD**: GitHub Actions para la ejecución automática de tests y despliegue de documentación.

## Instalación y Uso

### Preparación del entorno
```bash
git clone https://github.com/isteres/ServidorSpringTT1.git
cd ServidorSpringTT1
pip install -r requirements.txt
```

### Ejecución con Docker (Recomendado)
```bash
docker-compose up --build
```
Esto arrancará la API, el Worker, la Base de Datos y RabbitMQ.

## Endpoints Principales

| Método | Endpoint | Función |
| :--- | :--- | :--- |
| `POST` | `/simulation/solicitar` | Crea una nueva simulación (asíncrona) y devuelve un ticket. |
| `GET` | `/simulation/descargar/{ticket}` | Obtiene los resultados de la simulación. |
| `GET` | `/entities` | Lista los tipos de entidades disponibles. |
| `GET` | `/entities/validate/{id}` | Comprueba si un ID de entidad es válido. |

---
*Proyecto desarrollado para el Trabajo TT1 de Simulación de Sistemas.*
