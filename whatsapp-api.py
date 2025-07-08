import requests
TOKEN = "EAASYQK9zPaQBPAA4vAPjmgkt0cfB2v0i0Oi7hbpLfA1NgeFnIt5arOXZAxvWpjeyqtb19a3ZBDFqUCbs8rC0cHm6j0Q8LftnjZBFZBigFUZBjVsbCDKBo2p9cXtIj4lSeqlbXD5lwzZBABqDyaMQgGeF9gjQay8b5xprhygYASeHRKZA1sv827SQ2z0VnoDFKpdyE42VbR9nYZC6kF7D8r2F5pV6tRgW1bRQmY1oX8IVZB8ldIQZDZD"
url = "https://graph.facebook.com/v22.0/673983239136751/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}",  # Replace XXX with your actual token
    "Content-Type": "application/json"
}
payload = {
    "messaging_product": "whatsapp",
    "receiving_type": "individual",
    "to": "6285186899792",
    "type": "text",
    # "template": {
    #     "name": "hello_world",
    #     "language": {
    #         "code": "en_US"
    #     }
    # }
    "text": {
        "body": "sup nigga"
    }
}

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)

