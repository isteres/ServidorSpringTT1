package interfaces;

import java.util.List;

import modelo.DatosSimulation;
import modelo.DatosSolicitud;
import modelo.Entidad;

public interface InterfazContactoSim {
	public int solicitarSimulation(DatosSolicitud sol);
	public DatosSimulation descargarDatos(int ticket);
	public List<Entidad> getEntities();
	public boolean isValidEntityId(int id);
}
