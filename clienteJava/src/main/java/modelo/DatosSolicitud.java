package modelo;

import java.util.Map;

public class DatosSolicitud {
	private Map<Integer, Integer> nums;
	
	public DatosSolicitud(Map<Integer,Integer> nums) {
		this.nums = nums;
	}
	
	public Map<Integer, Integer> getNums(){
		return nums;
	}
}
