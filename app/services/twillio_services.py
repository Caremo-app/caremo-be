# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC99948e06b4e66c6faf0cdd33300ffc19"
auth_token = "3b75bda6c60f91965b2367b0f5e373cb"
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+6285345871185",
  from_="+12295149385"
)

print(call.sid)