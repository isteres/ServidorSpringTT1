package servicios;

import static org.junit.jupiter.api.Assertions.assertTrue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import interfaces.InterfazEnviarEmails;
import modelo.Destinatario;
import servicios.EnviarEmails;

public class EnviarEmailsTest {
	private Logger logs;
    private InterfazEnviarEmails enviarEmails;

    @BeforeEach
    void setUp() {
    	Logger testLogger = LoggerFactory.getLogger(EnviarEmailsTest.class);
        enviarEmails = new EnviarEmails(testLogger);
    }

    @Test
    void testEnviarEmail() {
        boolean resultado = enviarEmails.enviarEmail(new Destinatario(), "test@example.com");
        assertTrue(resultado);
    }
}
