import requests
import logging

def mt_interceptor(smpp, routable, **kwargs):
    try:
        # Extract actual SMPP message details from routable
        data = {
            "source_addr": routable.pdu.params.get('source_addr', b'').decode('utf-8', errors='ignore'),
            "destination_addr": routable.pdu.params.get('destination_addr', b'').decode('utf-8', errors='ignore'),
            "short_message": routable.pdu.params.get('short_message', b'').decode('utf-8', errors='ignore')
        }

        url = 'http://host.docker.internal:8001/inbound'  # ✅ Works in Docker for local service
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers, timeout=3)

        # Logging
        logger = logging.getLogger('jasmin-interceptor')
        if not logger.handlers:
            handler = logging.FileHandler('/var/log/jasmin/mt_interceptor.log')
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        if response.status_code == 200:
            logger.info(f"POST successful: {response.text}")
        else:
            logger.error(f"POST failed [{response.status_code}]: {response.text}")

    except Exception as e:
        logger.error(f"Interceptor error: {str(e)}")

    return routable  # Important: continue routing
