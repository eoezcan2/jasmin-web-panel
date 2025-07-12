from django.core.management.base import BaseCommand
import smpplib.client
import smpplib.consts

class Command(BaseCommand):
    help = "Test sending SMS via Jasmin"

    def handle(self, *args, **kwargs):

        client = smpplib.client.Client('localhost', 2775)
        client.connect()
        client.bind_transceiver(system_id='test', password='test')

        client.send_message(
            source_addr='491234567890',
            destination_addr='Test',
            short_message='This is an MO message'.encode('latin1'),

            source_addr_ton=1,  # SMPP_TON_INTL
            source_addr_npi=1,  # SMPP_NPI_ISDN

            dest_addr_ton=5,    # SMPP_TON_ALNUM
            dest_addr_npi=0,    # SMPP_NPI_UNKNOWN

            data_coding=3,
            esm_class=0
        )

        client.unbind()
