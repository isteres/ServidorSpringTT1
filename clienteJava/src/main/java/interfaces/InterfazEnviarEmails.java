package interfaces;

import modelo.Destinatario;

public interface InterfazEnviarEmails {
	public boolean enviarEmail(Destinatario dest, String email);
}
