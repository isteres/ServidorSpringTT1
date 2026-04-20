# Servidor de Simulación Hexagonal (TT1)

Este proyecto es un motor de simulación para la evolución de entidades en un tablero bidimensional. Está desarrollado siguiendo los principios de Clean Architecture y Arquitectura Hexagonal para garantizar un sistema desacoplado y fácil de testear.

## Arquitectura del Proyecto

La estructura se divide en capas según el patrón de Puertos y Adaptadores:

*   **Domain**: Define los modelos de datos y las entidades base.
*   **Application**: Contiene el servicio de simulación y las interfaces (puertos) necesarias para la comunicación entre capas.
*   **Infrastructure**: Implementa los detalles técnicos, como la API con FastAPI y la persistencia en memoria mediante repositorios.

## Lógica de Simulación

El motor calcula 10 pasos de evolución por cada petición. Se gestionan tres comportamientos distintos:

1.  **Entidad Estática**: No realiza ningún movimiento y mantiene su posición inicial.
2.  **Movimiento Adyacente**: Se desplaza a casillas contiguas (Norte, Sur, Este u Oeste). No se permiten movimientos diagonales.
3.  **Entidad Estática Clon**: Se mantiene en su sitio pero tiene una probabilidad del 80% de generar un nuevo clon en una casilla vacía del tablero.

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
