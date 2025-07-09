import requests
from dotenv import load_dotenv
import datetime
import os
load_dotenv()

TOKEN = os.environ.get("WHATSAPP_TOKEN")
ID = os.environ.get("WHATSAPP_ID")
url = f"https://graph.facebook.com/v22.0/{ID}/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}",  # Replace XXX with your actual token
    "Content-Type": "application/json"
}
payload = {
    "messaging_product": "whatsapp",
    "receiving_type": "individual",
    "to": "6285186899792",
    # "type": "text",
    "type": "template",
    "template": {
        "name": "health_warning",
        "language": {
            "code": "en"
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    { "type": "text", "parameter_name": "user_name", "text": "Kakek" },
                    { "type": "text", "parameter_name": "family_member_name", "text": "Edbert" },
                    { "type": "text", "parameter_name": "detection_time", "text": datetime.datetime.now().strftime("%d %B %Y, %H.%M WIB") },
                    { "type": "text", "parameter_name": "abnormality_type", "text": "FALL" }, #TODO: AI Infer Result
                    { "type": "text", "parameter_name": "measured_value", "text": "0" }, #TODO: AI Infer Result
                    { "type": "text", "parameter_name": "normal_range", "text": "100" }, #TODO: AI Infer Result
                ]
            }
        ]
    }
    # "text": {
    #     "body": "hello there, this is a testing bot"
    # }
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)

