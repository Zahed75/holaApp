import requests

def send_sms(phone_number, message, api_key):
    url = "https://sysadmin.muthobarta.com/api/v1/send-sms"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "receiver": phone_number,
        "message": message,
        "remove_duplicate": True
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
