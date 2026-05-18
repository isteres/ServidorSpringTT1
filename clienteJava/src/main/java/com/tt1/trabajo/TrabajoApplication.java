package com.tt1.trabajo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {"servicios", "com.tt1.trabajo"})
public class TrabajoApplication {

	public static void main(String[] args) {
		SpringApplication.run(TrabajoApplication.class, args);
	}

}
