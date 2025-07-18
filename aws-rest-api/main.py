from fastapi import FastAPI, Request
from pydantic import BaseModel
import boto3

app = FastAPI()
client = boto3.client(
    'pinpoint-sms-voice-v2',
    region_name='eu-central-1',
    aws_access_key_id='AKIARMM33EOITXJSFIHS',
    aws_secret_access_key='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'
)

class MOMessage(BaseModel):
    source_addr: str
    destination_addr: str
    short_message: str


@app.post("/inbound")
async def receive_sms(request: Request):
    try:
        data = await request.json()
        print("Received MO from Jasmin:", data)

        # Optionally validate fields manually
        message = MOMessage(**data)

        # Forward to provider (placeholder URL)
        client.send_text_message(
            DestinationPhoneNumber=message.destination_addr,
            # SourcePhoneNumber=message.source_addr,
            MessageBody=message.short_message,
        )

        print("SMS forwarded to provider successfully")
        return {"status": "ok", "message": "SMS forwarded successfully"}
    
    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
