from fastapi import FastAPI, Request
from pydantic import BaseModel
import boto3
import os

app = FastAPI()

# Read AWS credentials from environment
client = boto3.client(
    'pinpoint-sms-voice-v2',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
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

        message = MOMessage(**data)

        client.send_text_message(
            DestinationPhoneNumber=message.destination_addr,
            MessageBody=message.short_message,
        )

        print("SMS forwarded to AWS Pinpoint successfully")
        return {"status": "ok", "message": "SMS forwarded successfully"}
    
    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
