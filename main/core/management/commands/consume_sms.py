import pika
import json
import requests
import pickle
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Consume MO messages from Jasmin and forward to HTTP provider"

    def handle(self, *args, **kwargs):
        self.stdout.write("| Starting RabbitMQ consumer...")

        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER,
            settings.RABBITMQ_PASS
        )

        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host="/",
            credentials=credentials,
            heartbeat=60,
            blocked_connection_timeout=30
        )

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        self.stdout.write("| Connected to RabbitMQ")
        self.stdout.write(f"| Listening on queue: {settings.RABBITMQ_QUEUE}")

        channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=False)

        def callback(ch, method, properties, body):
            try:
                decoded = body.decode('utf-8', errors='ignore').strip()
                if not decoded:
                    self.stderr.write("Skipping empty message body")
                    return

                self.stdout.write(f"Decoded body: {decoded}")
                message = json.loads(decoded)

                if message.get('type') == 'deliver_sm':
                    self.stdout.write("Received MO message")
                    self.forward_to_provider(message['content'])
                else:
                    self.stdout.write(f"Skipped non-MO message: {message.get('type')}")

            except Exception as e:
                self.stderr.write(f"Error handling message: {e}")


        channel.basic_consume(
            queue=settings.RABBITMQ_QUEUE,
            on_message_callback=callback,
            auto_ack=True
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()

    def forward_to_provider(self, mo_message):
        self.stdout.write(f"| Forwarding to HTTP provider: {mo_message}")

        url = "http://placeholder.com/api"

        try:
            response = requests.post(url, json=mo_message)
            self.stdout.write(f"| Forwarded with status {response.status_code}")
        except Exception as e:
            self.stderr.write(f"| Forwarding failed: {e}")
