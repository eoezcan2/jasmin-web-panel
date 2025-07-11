import pika
import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Consume MO messages from Jasmin and forward to HTTP provider"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RabbitMQ consumer...")

        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASS
        )

        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host="/",
            credentials=credentials,
            heartbeat=60,  # Optional: helps with stability
            blocked_connection_timeout=30
        )

        connection = pika.BlockingConnection(
            parameters=parameters
        )

        self.stdout.write("Connected to RabbitMQ")

        channel = connection.channel()
        #channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                self.stdout.write(f"Received message: {message}")
                if message['type'] == 'deliver_sm':
                    print("Received MO:", message['content'])
                    self.forward_to_provider(message['content'])
            except Exception as e:
                print("Error:", str(e))

        channel.basic_consume(
            queue=settings.RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True
        )

        channel.start_consuming()

    def forward_to_provider(self, mo_message):
        self.stdout.write(f"Forwarding MO message: {mo_message}")
        # url = settings.PROVIDER_URL
        # try:
        #     r = requests.post(url, json=mo_message)
        #     print(f"Forwarded: {r.status_code}")
        # except Exception as e:
        #     print(f"Forwarding error: {e}")
