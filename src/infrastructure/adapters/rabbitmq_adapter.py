import pika
import json
import os
from application.ports.output.message_broker_port import MessageBrokerPort
from domain.entities.models import DatosSolicitud

class RabbitMQAdapter(MessageBrokerPort):
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.queue_name = "simulation_queue"

    def send_simulation_request(self, ticket: int, sol: DatosSolicitud):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        
        message = {
            "ticket": ticket,
            "solicitud": sol.model_dump()
        }
        
        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        connection.close()
