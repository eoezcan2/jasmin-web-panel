from django.core.management.base import BaseCommand
import smpplib.client
import smpplib.consts

def random_string(length=10):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

class Command(BaseCommand):
    help = "Simulate MO message via SMPP to Jasmin"

    def handle(self, *args, **kwargs):
        client = smpplib.client.Client('localhost', 2775)

        # Optional: enable debug output
        client.set_message_received_handler(lambda pdu: print("Received PDU:", pdu))
        client.connect()
        client.bind_transceiver(system_id='test', password='test')

        pdu = client.send_message(
            source_addr_ton=1,
            source_addr_npi=1,
            source_addr="TestSender",

            dest_addr_ton=5,
            dest_addr_npi=0,
            destination_addr="",

            short_message=random_string(10).encode('latin1'),
            data_coding=3,
            esm_class=0x00,
        )

        self.stdout.write(self.style.SUCCESS(f"Message sent (sequence #{pdu.sequence})"))
        client.unbind()
