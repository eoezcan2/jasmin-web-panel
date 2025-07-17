import requests
import logging

logger = logging.getLogger('jasmin-interceptor')
# handler = logging.FileHandler('mt_interceptor.log')
handler = logging.FileHandler('/var/log/jasmin/mt_interceptor.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

try:
    logger.debug("Test")
    print("Test")
    # Extract actual SMPP message details from routable
    data = {
        "source_addr": routable.pdu.params.get('source_addr', b'').decode('utf-8', errors='ignore'),
        "destination_addr": routable.pdu.params.get('destination_addr', b'').decode('utf-8', errors='ignore'),
        "short_message": routable.pdu.params.get('short_message', b'').decode('utf-8', errors='ignore')
    }

    ###############
    # data = {
    #     "source_addr": "123456",
    #     "destination_addr": "654321",
    #     "short_message": "This is a test message"
    # }
    ###############

    url = 'http://192.168.0.166:8001/inbound'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers, timeout=3)
    logger.debug("Request")

    if response.status_code == 200:
        print("200")
        logger.debug(f"POST successful: {response.text}")
    else:
        print("Bad")
        logger.error(f"POST failed [{response.status_code}]: {response.text}")

except Exception as e:
    print("Error")
    logger.error(f"Interceptor error: {str(e)}")