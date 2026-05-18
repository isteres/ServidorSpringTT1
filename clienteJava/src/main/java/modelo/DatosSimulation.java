package modelo;

import java.util.List;
import java.util.Map;

public class DatosSimulation {
	public DatosSimulation() {}
	
	private int maxSegundos;
	private int anchoTablero;
	private Map<Integer,List<Punto>> puntos;
	
	public int getMaxSegundos() {
		return maxSegundos;
	}
	
	public void setMaxSegundos(int s) {
		this.maxSegundos = s;
	}
	
	public int getAnchoTablero() {
		return anchoTablero;
	}
	
	public void setAnchoTablero(int s) {
		this.anchoTablero = s;
	}
	
	public Map<Integer,List<Punto>> getPuntos(){
		return puntos;
	}
	
	public void setPuntos(Map<Integer,List<Punto>> s) {
		this.puntos = s;
	}
}
