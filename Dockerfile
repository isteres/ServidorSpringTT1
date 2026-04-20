# Usamos una imagen ligera de Python como base
FROM python:3.10-slim-bookworm

# Instalamos uv directamente desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos solo los archivos de dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias usando uv
# --system indica que instale en el entorno global del contenedor (seguro en Docker)
# --no-cache evita guardar archivos temporales, reduciendo el tamaño de la imagen
RUN uv pip install --system --no-cache -r requirements.txt

# Copiamos el código fuente del backend
COPY src/ ./src/

# Exponemos el puerto que usa FastAPI
EXPOSE 8000

# Comando para arrancar el servidor
# Usamos el módulo python para ejecutar src.main (ajustado a tu estructura)
CMD ["python", "src/main.py"]
