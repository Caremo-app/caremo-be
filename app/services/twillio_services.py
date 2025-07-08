# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import urllib.parse

def call_hospital(phone_number: str, persona: str, location: str):
    account_sid = "AC99948e06b4e66c6faf0cdd33300ffc19"
    auth_token = "3b75bda6c60f91965b2367b0f5e373cb"
    client = Client(account_sid, auth_token)

    base_url = "https://yourdomain.com/v1/ai/twiml"
    query_params = urllib.parse.urlencode({
        "persona": persona,
        "location": location
    })
    twiml_url = f"{base_url}?{query_params}"

    call = client.calls.create(
        url=twiml_url,
        to=phone_number,
        from_="+12295149385"
    )

    print("📞 Call initiated with SID:", call.sid)
    return call.sid
