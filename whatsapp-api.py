import requests
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.environ.get("WHATSAPP_TOKEN")
url = f"https://graph.facebook.com/v22.0/{os.environ.get("WHATSAPP_ID")}/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}",  # Replace XXX with your actual token
    "Content-Type": "application/json"
}
payload = {
    "messaging_product": "whatsapp",
    "receiving_type": "individual",
    "to": "6285345871185",
    # "type": "text",
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
    # "text": {
    #     "body": "hello there, this is a testing bot"
    # }
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)

