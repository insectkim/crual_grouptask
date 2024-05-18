import requests
import json
from datetime import datetime, timedelta

class WeatherService:
    @staticmethod
    def call_weather_api():
        """
        기상청 API를 호출하여 날씨 예보 데이터를 가져옵니다.

        현재 시간 기준으로 최근 30분 단위의 예보 데이터를 요청합니다.
        PTY(강수 형태) 데이터를 추출하여 가장 가까운 예보 시간을 찾고,
        이를 weather_data.txt 파일에 추가로 저장합니다.

        Returns:
            int: 가장 가까운 예보 시간의 PTY 값 (강수 형태) 또는 1 (0이 아닌 경우)
        """
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
            pty_items = [item for item in items if item['category'] == 'PTY']
            if pty_items:
                nearest_pty = min(pty_items, key=lambda x: (x['fcstDate'], x['fcstTime']))
                with open("weather_data.txt", "a") as file:
                    line = f"Base Date: {base_date}, Base Time: {base_time}, Forecast Date: {nearest_pty['fcstDate']}, Forecast Time: {nearest_pty['fcstTime']}, Category: {nearest_pty['category']}, Value: {nearest_pty['fcstValue']}\n"
                    file.write(line)
                print("Nearest PTY data has been appended to the file.")
                return 1 if nearest_pty['fcstValue'] != '0' else 0
            else:
                print("No PTY data found, defaulting to 1.")
                return 1
        else:
            print("Failed to retrieve data. Status Code:", response.status_code)
            return 1

    @staticmethod
    def send_value_to_server(value):
        """
        특정 값을 서버에 전송합니다.

        Parameters:
            value (int): 서버에 전송할 값 (예: PTY 값)
        """
        server_url = f"http://localhost:5000/update_weather?value={value}"  # 실제 서버 URL과 엔드포인트로 업데이트
        response = requests.get(server_url)
        if response.status_code == 200:
            print("Value sent successfully")
        else:
            print("Failed to send value")

# 이 블록은 스크립트가 직접 실행될 때만 코드를 실행합니다.
if __name__ == "__main__":
    value = WeatherService.call_weather_api()
    WeatherService.send_value_to_server(value)
