import requests
import enum
import datetime
from .ml_services import Location

"""
List Possible PHONE NUMBER RECEIVER
- edbert: 6285345871185
- rafi: 6285186899792
- syarafi: 6281347507393
"""
class PhoneEnum(str, enum.Enum):
    NO_EDBERT = "6285345871185"
    NO_RAFI = "6285186899792"
    NO_AKMAL = "6281347507393"

class WhatsAppService:
    def __init__(self, token: str, phone_number_id: str):
        self.token = token
        self.phone_number_id = phone_number_id
        self.api_url = f"https://graph.facebook.com/v22.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_template_message(self, recipient_number: str, template_name: str, persona_relay: str, persona_receive: str, bpm: int, location: str, language_code: str = "en"):
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "template",
            "receiving_type": "individual",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            { "type": "text", "parameter_name": "user_name", "text": persona_relay },
                            { "type": "text", "parameter_name": "family_member_name", "text": persona_receive },
                            { "type": "text", "parameter_name": "detection_time", "text": datetime.datetime.now().strftime("%d %B %Y, %H.%M WIB") },
                            { "type": "text", "parameter_name": "abnormality_type", "text": "FALL" }, #TODO: AI Infer Result
                            { "type": "text", "parameter_name": "measured_value", "text": "0" }, #TODO: AI Infer Result
                            { "type": "text", "parameter_name": "normal_range", "text": "100" }, #TODO: AI Infer Result
                        ]
                    }
                ]
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.status_code, response.json()
    
    def send_text_message(self, recipient_number: str, msg: str, language_code: str = "en"):
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_number,
            "type": "text",
            "text": {
                "body": msg,
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.status_code, response.json()


