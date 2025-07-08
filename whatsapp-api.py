import requests
TOKEN = "EAASYQK9zPaQBPOUdNWJ4HBZCdLyBvdHE1RaH5UyMruM313HdFXJea2JmTFXOIMHCI0IrCnhZBLupx1107zqZAbZCqQCSNbjoyGYQ0wh07jdY1a3oTnsM1cedsvl6KyY97uOR3f7lcSqgedTHLrvd4LfOxVKJGNCqEklqwoHgStCZBbPytODU7En5XpsjWUZCBq2yZAhmH74gvmytUyUDDz7EfM474a8JrEgLufClXyMvF5ZAZBAZDZD"
url = "https://graph.facebook.com/v22.0/673983239136751/messages"
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

