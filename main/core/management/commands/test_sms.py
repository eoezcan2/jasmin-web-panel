from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Test sending SMS via Jasmin"

    def handle(self, *args, **kwargs):
        # send_sms.py
        import smpplib.client
        import smpplib.consts
        import smpplib.gsm

        client = smpplib.client.Client('localhost', 2775)  # Jasmin IP/port

        client.connect()
        client.bind_transmitter(system_id='test', password='test')  # match Jasmin user/pass

        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            source_addr='Test',

            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr='491234567890',

            short_message='Hello from your local test!'.encode('latin-1'),
            data_coding=0x03,  # Latin-1
            esm_class=0x00,
        )

        print("Message sent:", pdu.sequence)
        client.unbind()