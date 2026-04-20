# 🚀 Servidor de Simulación Hexagonal (TT1)

[![Python Tests](https://github.com/isteres/ServidorSpringTT1/actions/workflows/python-tests.yml/badge.svg)](https://github.com/isteres/ServidorSpringTT1/actions/workflows/python-tests.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)

Este proyecto es un motor de simulación evolutiva de entidades en un tablero bidimensional, desarrollado bajo los principios de **Clean Architecture** y **Arquitectura Hexagonal**. Permite gestionar la evolución temporal de diferentes tipos de entidades con comportamientos únicos de movimiento y replicación.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura de **Puertos y Adaptadores** para garantizar el desacoplamiento y la testabilidad:

*   **`Domain`**: Contiene las entidades puras y la definición de los modelos de datos.
*   **`Application`**: Implementa los casos de uso (`SimulationService`) y define los puertos de entrada y salida.
*   **`Infrastructure`**: Detalles de implementación (FastAPI para la Web e `InMemoryRepository` para persistencia volátil).

---

## 🧬 Lógica de Simulación y Entidades

El motor de simulación procesa 10 segundos de evolución por cada solicitud, gestionando tres tipos de comportamientos principales:

1.  **Entidad Estática**: Mantiene su posición original durante toda la simulación.
2.  **Movimiento Adyacente**: Se desplaza a casillas contiguas (Norte, Sur, Este, Oeste) siguiendo una vecindad de *Von Neumann*.
3.  **Entidad Estática Clon**: No se desplaza, pero posee un **80% de probabilidad** de generar un clon en una casilla libre aleatoria del tablero.

### ⚖️ Regla Crítica: FCFS (First-Come, First-Served)
Para evitar colisiones, el sistema implementa una **reserva dinámica de casillas**:
*   En cada turno, el orden de procesamiento de las entidades es aleatorio (*shuffling*).
*   La primera entidad en procesarse tiene prioridad absoluta para "reclamar" una casilla.
*   Si una casilla es reservada, las entidades posteriores deben buscar rutas alternativas o quedarse quietas, garantizando que **nunca existan dos entidades en el mismo punto**.

---

## 🛠️ Stack Tecnológico

*   **Core**: Python 3.11+
*   **Web Framework**: FastAPI & Uvicorn (ASGI)
*   **Validación**: Pydantic v2
*   **Testing**: Pytest (Unitarios e Integración)
*   **CI/CD**: GitHub Actions (Automatización de pruebas en cada Push)

---

## 🚦 Guía de Inicio Rápido

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/isteres/ServidorSpringTT1.git
cd ServidorSpringTT1

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución
```bash
python src/main.py
```
La API estará disponible en `http://localhost:8000`. Puedes explorar la documentación interactiva en `/docs`.

---

## 🧪 Pruebas y Calidad
El proyecto cuenta con una suite de pruebas que garantiza la integridad de la lógica de negocio:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python -m pytest tests/
```
*   **Tests de Integración**: Validan el flujo completo desde la solicitud hasta la generación de puntos sin colisiones.
*   **Validación de Negocio**: Pruebas específicas para el movimiento restringido H/V y la lógica de clonación.

---

## 📬 API Endpoints

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/simulation/solicitar` | Inicia una nueva simulación de 10 segundos. |
| `GET` | `/simulation/descargar/{ticket}` | Recupera los resultados mediante un ticket. |
| `GET` | `/entities` | Lista los tipos de entidades disponibles. |
| `GET` | `/entities/validate/{id}` | Valida la existencia de un ID de entidad. |

---
*Desarrollado para el Trabajo TT1 - Simulación de Sistemas Distribuidos.*
