import requests
TOKEN = "EAAVChHGh8UABPH2qNukbklV8XWnZC7wPtmsgTMT9uMIgx4MOF8vRPnZAXZAzaZB7PvQH8MK6pwPzGkL6Hx8Rfn8qxIBirZBRuwmVWZBZC1fLZCkrZCbpoQZCZAAAkgNSWHEdVJuJ1PKCab9V3nOLmzyGCibxASS50wgBet2Xc7KvSrvE63pgOcH3KA5ptPlbWkNZBZChaDTVj8nOhnZB0vGZCm9ZC1e17YDu3FK3LEcAwuEJ4zgZBOXVBhAZDZD"
url = "https://graph.facebook.com/v22.0/758357087357144/messages"
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

