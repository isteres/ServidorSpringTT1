# Interfaz Web (TT1)

Este proyecto es una interfaz web desarrollada con **Spring Boot** para gestionar y visualizar simulaciones. Permite a los usuarios configurar parámetros de simulación, enviar solicitudes a un servicio externo y visualizar los resultados de forma interactiva en una rejilla temporal.

## 🚀 Características

- **Configuración Dinámica**: Formulario para definir la cantidad de diferentes entidades para la simulación.
- **Visualización Interactiva**: Visualización de resultados en una rejilla (Grid) con control deslizante para navegar a través del tiempo de simulación.
- **Estilo Moderno**: Interfaz limpia y profesional utilizando CSS moderno y diseño responsivo.
- **Documentación de API**: Integración completa con Swagger UI para explorar los endpoints disponibles.
- **Monitorización**: Implementación de Spring Boot Actuator para el seguimiento del estado de la aplicación.
- **Contenerización**: Preparado para desplegarse fácilmente mediante Docker y Docker Compose.

## 🛠️ Stack Tecnológico

- **Backend**: Java 17 con Spring Boot 3.3.4.
- **Frontend**: Thymeleaf (Motor de plantillas) y Vanilla CSS/JS.
- **API**: SpringDoc OpenAPI (Swagger).
- **Herramientas**: Maven para la gestión de dependencias y construcción.
- **Despliegue**: Docker y Docker Compose.

## 📁 Estructura del Proyecto

- `src/main/java/com/tt1/trabajo`: Controladores principales de la aplicación.
- `src/main/java/modelo`: Clases de dominio (Entidad, Punto, DatosSolicitud, etc.).
- `src/main/java/servicios`: Lógica de negocio y comunicación con servicios externos.
- `src/main/resources/templates`: Vistas HTML (Thymeleaf).
- `src/main/resources/static`: Archivos estáticos (CSS, JS).

## ⚙️ Instalación y Ejecución

### Requisitos Previos

- Java 17 o superior.
- Maven 3.8+.
- Docker (opcional, para despliegue en contenedores).

### Opción 1: Ejecución Local (Maven)

1. Clona el repositorio.
2. Compila el proyecto:
   ```bash
   ./mvnw clean package
   ```
3. Ejecuta la aplicación:
   ```bash
   ./mvnw spring-boot:run
   ```
4. Accede a `http://localhost:8080/solicitud`.

### Opción 2: Ejecución con Docker Compose

Este método levanta tanto la aplicación web como el servicio de simulación necesario:

```bash
docker-compose up --build
```

## 📍 Endpoints Principales

- **Formulario de Solicitud**: `GET /solicitud`
- **Visualización de Resultados**: `GET /grid?tok={token}` (Sustituye `{token}` por el código recibido tras la solicitud).
- **Documentación Swagger**: `GET /swagger/index.html`
- **Health Check**: `GET /actuator/health`

## 🎨 Personalización Visual

El proyecto incluye un sistema de estilos centralizado en `src/main/resources/static/css/style.css` que proporciona una apariencia cohesiva y profesional a todas las páginas, incluyendo estados de carga, manejo de errores y visualización de tokens.

---
*Este proyecto forma parte de la asignatura de Taller Transversal I (TT1).*
