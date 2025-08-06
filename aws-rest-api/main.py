from fastapi import FastAPI, Request
from pydantic import BaseModel
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "")  # Fetch API key from environment variable
DEFAULT_SENDER_ID = "MyDefaultSender"  # Hardcoded fallback SenderId

def send_message(source_addr: str, destination_addr: str, short_message: str):
    import http.client
    import json
    import ssl

    # Create an SSL context that does not verify the certificate
    context = ssl._create_unverified_context()

    # Connect using the context that skips verification
    conn = http.client.HTTPSConnection("web.it-decision.com", context=context)

    payload = json.dumps({
        "phone": destination_addr,
        "sender": source_addr,
        "text": short_message,
        "validity_period": 300
    })

    headers = {
        'Authorization': f'Basic {API_KEY}',
        # <-- Replace with actual base64-encoded API key
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/v1/api/send-sms", payload, headers)
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        print("200 OK")
        print(data.decode("utf-8"))
    else:
        print(f"Error: {res.status} - {res.reason}")
        raise Exception(f"Failed to send message: {res.status} - {res.reason}")

class MOMessage(BaseModel):
    source_addr: str
    destination_addr: str
    short_message: str

@app.post("/send")
async def receive_sms(request: Request):
    try:
        data = await request.json()
        print("Received MO from Jasmin:", data)

        message = MOMessage(**data)

        # Ensure destination number starts with "+"
        destination_number = message.destination_addr.strip()
        if not destination_number.startswith("+"):
            destination_number = "+" + destination_number

        # Determine SenderId
        sender_id = message.source_addr.strip() if message.source_addr else DEFAULT_SENDER_ID

        send_message(
            source_addr=sender_id,
            destination_addr=destination_number,
            short_message=message.short_message.strip()
        )

        print(f"SMS forwarded to AWS Pinpoint successfully with SenderId={sender_id}")
        return {"status": "ok", "message": "SMS forwarded successfully"}

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
