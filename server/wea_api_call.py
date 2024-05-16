import requests
import json
from datetime import datetime, timedelta

def call_weather_api():
    now = datetime.now()

    if now.minute < 30:
        base_time = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    else:
        base_time = now.replace(minute=30, second=0, microsecond=0)

    base_date = base_time.strftime("%Y%m%d")
    base_time = base_time.strftime("%H%M")

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params = {
        'serviceKey': 'ShoyixM1ptYZBhBnejvluAoQqSl4MqWlEzNVPtPP+TbRZoI8gQI94ni5RSqKOUIGZjiXvzSyTiI1/t3Zk2aFmQ==',
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': '98',
        'ny': '75'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        items = data['response']['body']['items']['item']
        
        # Extract PTY items
        pty_items = [item for item in items if item['category'] == 'PTY']
        if pty_items:
            nearest_pty = min(pty_items, key=lambda x: (x['fcstDate'], x['fcstTime']))
            with open("weather_data.txt", "a") as file:  
                line = f"Base Date: {base_date}, Base Time: {base_time}, Forecast Date: {nearest_pty['fcstDate']}, Forecast Time: {nearest_pty['fcstTime']}, Category: {nearest_pty['category']}, Value: {nearest_pty['fcstValue']}\n"
                file.write(line)
            print("Nearest PTY data has been appended to the file.")
            return nearest_pty['fcstValue']
        else:
            print("No PTY data found.")
            return None
    else:
        print("Failed to retrieve data. Status Code:", response.status_code)
        return None

def send_value_to_server(value):
    server_url = f"http://localhost:5000/update_weather?value={value}"  # Update with the actual server URL and endpoint
    response = requests.get(server_url)
    
    if response.status_code == 200:
        print("Value sent successfully")
    else:
        print("Failed to send value")

# This block ensures that the following code only runs if the script is executed directly
if __name__ == "__main__":
    value = call_weather_api()
    if value is not None:
        send_value_to_server(value)
    else:
        # Even if no value is obtained, send a default flag (e.g., 0) to the server
        send_value_to_server(0)
