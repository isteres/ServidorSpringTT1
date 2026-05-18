# ETAPA 1: Compilación (Usamos una imagen que YA tiene Maven)
FROM maven:3.8.5-openjdk-17-slim AS build
WORKDIR /app

# Copiamos los archivos de configuración y el código fuente
COPY pom.xml .
COPY src ./src

# Ejecutamos la compilación dentro de Docker (Genera el .jar automáticamente)
RUN mvn clean package -DskipTests

# ETAPA 2: Imagen de ejecución (Ligera)
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app

# Copiamos el .jar generado en la ETAPA 1 a esta nueva imagen
# Nota: Usamos un comodín (*) por si el nombre exacto del versionado cambia
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]