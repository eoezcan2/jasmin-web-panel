import boto3

print("Connecting")
client = boto3.client(
    'pinpoint-sms-voice-v2',
    region_name='eu-central-1',
    aws_access_key_id='AKIARMM33EOITXJSFIHS',
    aws_secret_access_key='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'
)

print("Sending")
client.send_text_message(
    DestinationPhoneNumber='+393496146815',
    MessageBody='This is a test message',
)

print("Success")
