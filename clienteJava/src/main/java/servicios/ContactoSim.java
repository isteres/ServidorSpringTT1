package servicios;

import java.util.Arrays;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.slf4j.Logger;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import interfaces.InterfazContactoSim;
import modelo.DatosSimulation;
import modelo.DatosSolicitud;
import modelo.Entidad;

@Service
public class ContactoSim implements InterfazContactoSim {

    @Value("${SIMULATION_SERVER_URL:http://localhost:8000}")
    private String baseUrl;

    private final RestTemplate restTemplate;
    private final Logger logger;

    public ContactoSim(Logger logger) {
        this.restTemplate = new RestTemplate();
        this.logger = logger;
    }

    @Override
    public int solicitarSimulation(DatosSolicitud sol) {
        try {
            String url = baseUrl + "/simulation/solicitar";
            Integer ticket = restTemplate.postForObject(url, sol, Integer.class);
            logger.info("Simulation requested, ticket: {}", ticket);
            return ticket != null ? ticket : -1;
        } catch (Exception e) {
            logger.error("Error al solicitar simulación en el servidor: {}", e.getMessage());
            return -1;
        }
    }

    @Override
    public DatosSimulation descargarDatos(int ticket) {
        try {
            String url = baseUrl + "/simulation/descargar/" + ticket;
            DatosSimulation sim = restTemplate.getForObject(url, DatosSimulation.class);
            if (sim != null) {
                logger.info("Datos de simulación descargados para ticket: {}", ticket);
                return sim;
            }
        } catch (Exception e) {
            logger.error("Error al descargar datos de simulación {} del servidor: {}", ticket, e.getMessage());
        }
        return new DatosSimulation();
    }

    @Override
    public List<Entidad> getEntities() {
        try {
            String url = baseUrl + "/entities";
            Entidad[] entities = restTemplate.getForObject(url, Entidad[].class);
            return entities != null ? Arrays.asList(entities) : Arrays.asList();
        } catch (Exception e) {
            logger.error("Error al obtener entidades del servidor: {}", e.getMessage());
            return Arrays.asList();
        }
    }

    @Override
    public boolean isValidEntityId(int id) {
        try {
            String url = baseUrl + "/entities/validate/" + id;
            Boolean isValid = restTemplate.getForObject(url, Boolean.class);
            return isValid != null && isValid;
        } catch (Exception e) {
            logger.error("Error al validar entidad {} en el servidor: {}", id, e.getMessage());
            return false;
        }
    }
}
