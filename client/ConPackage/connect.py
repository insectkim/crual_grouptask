import requests

SERVER_URL = 'http://192.168.200.113:5000'

def send_request(endpoint, method='GET', data=None):
    url = f"{SERVER_URL}/{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "fail"}
