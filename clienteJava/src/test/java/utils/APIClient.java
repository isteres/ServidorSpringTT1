package utils;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;

public class APIClient {

    private final String urlBase = "http://localhost:8080/Solicitud/Solicitar";
    private final HttpClient httpClient = HttpClient.newHttpClient();

    /**
     * Método principal para ejecutar y probar la conexión con la API de la VM.
     */
    public static void main(String[] args) {
        APIClient cliente = new APIClient();

        // Datos de prueba basados en tu ejecución de Swagger
        String usuario = "isaac";
        String jsonInput = "{\n" +
                "  \"cantidadesIniciales\": [10],\n" +
                "  \"nombreEntidades\": [\"entidades\"]\n" +
                "}";

        System.out.println("Enviando petición a la máquina virtual...");
        String resultado = cliente.solicitarServicio(usuario, jsonInput);
        System.out.println(resultado);
    }

    public String solicitarServicio(String nombreUsuario, String jsonBody) {
        try {
            // Construcción de la URL con el parámetro query visto en Swagger
            String urlCompleta = urlBase + "?nombreUsuario=" + nombreUsuario;

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(urlCompleta))
                    .header("Content-Type", "application/json")
                    .header("Accept", "text/json")
                    .POST(BodyPublishers.ofString(jsonBody))
                    .build();

            // Envío síncrono de la petición
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            return "--- Respuesta del Servidor ---\n" +
                    "Estado HTTP: " + response.statusCode() + "\n" +
                    "Cuerpo: " + response.body();

        } catch (Exception e) {
            return "Error crítico: No se pudo contactar con la VM. " +
                    "Verifica que el puerto 8080 esté redirigido al 5000 en VirtualBox.";
        }
    }
}