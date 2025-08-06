import http.client
import json
import ssl

# Create an SSL context that does not verify the certificate
context = ssl._create_unverified_context()

# Connect using the context that skips verification
conn = http.client.HTTPSConnection("web.it-decision.com", context=context)

payload = json.dumps({
  "phone": 393277652065,
  "sender": "InfoItd",
  "text": "This is messages DecisionTelecom",
  "validity_period": 300
})

headers = {
  'Authorization': 'Basic ODVhNWYwYjIyNmM4NzM1ZDViNzcyNGNmMGNkOWE2NjI=',  # <-- Replace with actual base64-encoded API key
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