import requests
import json
from datetime import datetime, timedelta

# 현재 시간을 구하고, 필요하다면 시간을 조정
now = datetime.now()

# 현재 시각이 30분 미만이면, 이전 시간의 30분을 기준으로 설정
if now.minute < 30:
    base_time = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
else:
    base_time = now.replace(minute=30, second=0, microsecond=0)

# base_date와 base_time을 올바른 포맷으로 설정
base_date = base_time.strftime("%Y%m%d")
base_time = base_time.strftime("%H%M")

# API 요청 URL 및 파라미터 설정
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
params = {
    'serviceKey' : 'ShoyixM1ptYZBhBnejvluAoQqSl4MqWlEzNVPtPP+TbRZoI8gQI94ni5RSqKOUIGZjiXvzSyTiI1/t3Zk2aFmQ==',  # 실제 서비스 키 입력
    'pageNo' : '1',
    'numOfRows' : '100',
    'dataType' : 'JSON',
    'base_date' : base_date,   # 현재 날짜
    'base_time' : base_time,   # 현재 시간 기준 마지막 30분
    'nx' : '98',
    'ny' : '75'
}

# API 호출
response = requests.get(url, params=params)
data = response.json()

# 파일에 추가하기
if response.status_code == 200:
    items = data['response']['body']['items']['item']
    # PTY 카테고리의 가장 가까운 미래 시간 데이터 찾기
    pty_items = [item for item in items if item['category'] == 'PTY']
    if pty_items:
        nearest_pty = min(pty_items, key=lambda x: (x['fcstDate'], x['fcstTime']))
        with open("weather_data.txt", "a") as file:  # 'a' 모드로 파일 열기
            line = f"Base Date: {base_date}, Base Time: {base_time}, Forecast Date: {nearest_pty['fcstDate']}, Forecast Time: {nearest_pty['fcstTime']}, Category: {nearest_pty['category']}, Value: {nearest_pty['fcstValue']}\n"
            file.write(line)
        print("Nearest PTY data has been appended to the file.")
    else:
        print("No PTY data found.")
else:
    print("Failed to retrieve data. Status Code:", response.status_code)