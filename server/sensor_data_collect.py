import RPi.GPIO as GPIO
import time
from datetime import datetime
import fcntl
import os
import requests

# 스크립트 파일 위치를 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "log")
LOG_FILE = os.path.join(LOG_DIR, "dust_log.dat")

# 로그 디렉토리가 존재하지 않으면 생성
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 핀 번호 설정 (BCM 모드)
PIN = 21
previous_flag = None
# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

# 서버 URL 설정 (localhost로 변경)
SERVER_URL = "http://localhost:5000/check_dust_data"

# 측정값 저장을 위한 리스트 초기화
recent_values = []

def pulseIn(pin, level, timeout):
    start_time = time.time()
    while GPIO.input(pin) != level:
        if time.time() - start_time > timeout:
            return 0
    start_pulse = time.time()
    while GPIO.input(pin) == level:
        if time.time() - start_pulse > timeout:
            return 0
    end_pulse = time.time()
    return (end_pulse - start_pulse) * 1_000_000  # 마이크로초 단위로 반환

def pulse2ugm3(pulse):
    # 최소 펄스 폭 및 최대 펄스 폭 설정
    min_pulse = 6.8
    max_pulse = 7000
    
    # 펄스 폭이 최소 펄스 폭보다 작으면 최소 펄스 폭으로 처리
    if pulse < min_pulse:
        pulse = min_pulse
    
    # 먼지 농도 계산
    value = (pulse - min_pulse) / (max_pulse - min_pulse) * 250
    return int(value)  # 소수점 이하 제외

def log_to_file(log_entry):
    with open(LOG_FILE, "a") as file:
        fcntl.flock(file, fcntl.LOCK_SH)  # 공유 잠금 설정
        file.write(log_entry)
        file.write("\n")
        fcntl.flock(file, fcntl.LOCK_UN)  # 잠금 해제

def send_data_to_server(value):
    global previous_flag
    # 플래그 값이 이전과 다를 경우에만 서버에 데이터 전송
    if value != previous_flag:
        previous_flag = value  # 현재 플래그 값을 이전 플래그로 업데이트
        try:
            response = requests.get(SERVER_URL, params={'value': value})
            if response.status_code == 200:
                print("Data sent to server successfully.")
            else:
                print("Failed to send data to server.")
        except Exception as e:
            print(f"Error sending data to server: {e}")

try:
    while True:
        pulse = pulseIn(PIN, GPIO.LOW, 0.02)  # 20ms 타임아웃
        ugm3 = pulse2ugm3(pulse)
        
        if ugm3 > 1:  # 1 μg/m³ 이하 값은 버림
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}|{ugm3}"
            
            print(log_entry)
            
            # 파일에 로그 기록
            log_to_file(log_entry)
            
            # 최근 5개의 측정값 저장
            recent_values.append(ugm3)
            if len(recent_values) > 5:
                recent_values.pop(0)
            
            # 최근 5개의 측정값 평균 계산
            if len(recent_values) == 5:
                avg_value = sum(recent_values) / len(recent_values)
                print(f"Average of last 5 readings: {avg_value}")
                
                # 기준값(100)과 비교하여 서버에 데이터 전송 조건 변경
                new_flag = 1 if avg_value >= 60 else 0
                send_data_to_server(new_flag)
        
        time.sleep(1)  # 작동 주기 1초

except KeyboardInterrupt:
    print("측정을 중지합니다.")

finally:
    GPIO.cleanup()

