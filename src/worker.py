import pika
import json
import os
import sys
import time
from sqlmodel import Session

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from infrastructure.database import engine
from infrastructure.adapters.sql_repository import SQLSimulationRepository
from application.use_cases.simulation_service import SimulationService
from domain.entities.models import DatosSolicitud

def callback(ch, method, properties, body):
    print(f" [x] Recibido mensaje para simulación")
    data = json.loads(body)
    ticket = data["ticket"]
    sol_dict = data["solicitud"]
    sol = DatosSolicitud(**sol_dict)

    with Session(engine) as session:
        repository = SQLSimulationRepository(session)
        service = SimulationService(repository)
        
        print(f" [*] Ejecutando simulación para ticket {ticket}...")
        try:
            resultado = service.ejecutar_simulacion(sol)
            repository.save_simulation(ticket, resultado)
            print(f" [v] Simulación {ticket} completada y guardada.")
        except Exception as e:
            print(f" [x] Error procesando simulación {ticket}: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    host = os.getenv("RABBITMQ_HOST", "localhost")
    print(f" [*] Conectando a RabbitMQ en {host}...")
    
    # Reintento de conexión por si RabbitMQ tarda en arrancar
    connection = None
    for i in range(10):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            break
        except Exception:
            print(f" [!] RabbitMQ no listo, reintentando en 5s... ({i+1}/10)")
            time.sleep(5)
            
    if not connection:
        print(" [x] No se pudo conectar a RabbitMQ. Saliendo.")
        return

    channel = connection.channel()
    channel.queue_declare(queue='simulation_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='simulation_queue', on_message_callback=callback)

    print(' [*] Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido')
        sys.exit(0)
