import pika
import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Consume MO messages from Jasmin and forward to HTTP provider"

    def handle(self, *args, **kwargs):
        self.stdout.write("| Starting RabbitMQ consumer...")

        # Connect to RabbitMQ
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

        channel.queue_declare(queue=settings.RABBITMQ_QUEUE)

        def callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                self.stdout.write(f"| Received message: {message}")

                if message.get('type') == 'deliver_sm':
                    self.stdout.write("| MO message matched")
                    self.forward_to_provider(message['content'])
                else:
                    self.stdout.write(f"| Skipped non-MO message type: {message.get('type')}")

            except Exception as e:
                self.stderr.write(f"| Error handling message: {str(e)}")

        channel.basic_consume(
            queue=settings.RABBITMQ_QUEUE,
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()

    def forward_to_provider(self, mo_message):
        self.stdout.write(f"| Forwarding to HTTP provider: {mo_message}")

        # Placeholder URL
        url = "http://httpbin.org/post"

        try:
            response = requests.post(url, json=mo_message)
            self.stdout.write(f"| Forwarded with status {response.status_code}")
        except Exception as e:
            self.stderr.write(f"| Forwarding failed: {e}")
