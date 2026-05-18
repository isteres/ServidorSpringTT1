package servicios;

import static org.junit.jupiter.api.Assertions.*;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

import interfaces.InterfazContactoSim;
import modelo.DatosSimulation;
import modelo.DatosSolicitud;
import modelo.Entidad;
import modelo.Punto;

public class ContactoSimTest {

    private InterfazContactoSim contactoSim;
    private final int ANCHO_ESPERADO = 10;
    private final int TIEMPO_ESPERADO = 5;

    @BeforeEach
    void setUp() {
        // Usamos el constructor real con un logger de test
        contactoSim = new ContactoSim(LoggerFactory.getLogger("TestLogger"));
    }

    @Test
    @DisplayName("Debe inicializar las 3 entidades por defecto correctamente")
    void testEntitiesInitialization() {
        List<Entidad> entities = contactoSim.getEntities();
        assertNotNull(entities, "La lista de entidades no debe ser nula");
        assertEquals(3, entities.size(), "Debe haber exactamente 3 entidades");
        
        assertTrue(contactoSim.isValidEntityId(1));
        assertTrue(contactoSim.isValidEntityId(2));
        assertTrue(contactoSim.isValidEntityId(3));
        assertFalse(contactoSim.isValidEntityId(99), "Un ID no registrado debe ser inválido");
    }

    @Test
    @DisplayName("Debe generar un token válido y permitir la descarga de datos consistente")
    void testFullSimulationFlow() {
        // 1. Solicitar simulación
        Map<Integer, Integer> config = new HashMap<>();
        config.put(1, 10);
        DatosSolicitud sol = new DatosSolicitud(config);
        
        int token = contactoSim.solicitarSimulation(sol);
        
        // Verificación de token (rango 1000-9999 según implementación)
        assertTrue(token >= 1000 && token <= 9999, "El token debe estar en el rango esperado");

        // 2. Descargar datos
        DatosSimulation data = contactoSim.descargarDatos(token);
        
        assertNotNull(data);
        assertEquals(ANCHO_ESPERADO, data.getAnchoTablero());
        assertEquals(TIEMPO_ESPERADO, data.getMaxSegundos());
        
        Map<Integer, List<Punto>> puntosPorSegundo = data.getPuntos();
        assertNotNull(puntosPorSegundo);
        assertEquals(TIEMPO_ESPERADO, puntosPorSegundo.size(), "Debe haber datos para cada segundo");

        // 3. Validar integridad de los puntos generados
        for (int t = 0; t < TIEMPO_ESPERADO; t++) {
            List<Punto> puntos = puntosPorSegundo.get(t);
            assertNotNull(puntos, "La lista de puntos para el segundo " + t + " no debe ser nula");
            assertFalse(puntos.isEmpty(), "Debe haber al menos un punto en el segundo " + t);
            
            for (Punto p : puntos) {
                // Validar límites del tablero
                assertTrue(p.getX() >= 0 && p.getX() < ANCHO_ESPERADO, "X fuera de límites: " + p.getX());
                assertTrue(p.getY() >= 0 && p.getY() < ANCHO_ESPERADO, "Y fuera de límites: " + p.getY());
                assertNotNull(p.getColor(), "El punto debe tener un color asignado");
            }
        }
    }

    @Test
    @DisplayName("Debe manejar correctamente tickets inexistentes")
    void testInvalidTicket() {
        int ticketInexistente = 123; // Token que no ha sido generado
        DatosSimulation data = contactoSim.descargarDatos(ticketInexistente);
        
        assertNotNull(data, "Incluso con ticket inválido, debería devolver un objeto (aunque vacío)");
        assertNull(data.getPuntos(), "Los puntos deben ser nulos para un ticket inválido");
    }

    @Test
    @DisplayName("Validación de IDs de entidad negativos o fuera de rango")
    void testBoundaryEntityIds() {
        assertFalse(contactoSim.isValidEntityId(-1));
        assertFalse(contactoSim.isValidEntityId(0));
        assertFalse(contactoSim.isValidEntityId(4));
    }
}
