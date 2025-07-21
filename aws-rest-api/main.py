from fastapi import FastAPI, Request
from pydantic import BaseModel
import boto3
import os

app = FastAPI()

# AWS Pinpoint client
client = boto3.client(
    'pinpoint-sms-voice-v2',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

DEFAULT_SENDER_ID = "MyDefaultSender"  # Hardcoded fallback SenderId

class MOMessage(BaseModel):
    source_addr: str
    destination_addr: str
    short_message: str

@app.post("/inbound")
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

        # Send SMS to AWS Pinpoint
        client.send_text_message(
            DestinationPhoneNumber=destination_number,
            MessageBody=message.short_message,
            SenderId=sender_id
        )

        print(f"SMS forwarded to AWS Pinpoint successfully with SenderId={sender_id}")
        return {"status": "ok", "message": "SMS forwarded successfully"}

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
