from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
import threading
import time
import signal
import sys
import os

# GPIO 핀 설정(리드 스위치)
sensor_pin = 6
# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
# 내부 풀업 저항 활성화
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# pigpio 핀 팩토리 설정
factory = PiGPIOFactory()

# 서보모터를 연결할 GPIO 핀 설정 (예: GPIO 12) 및 핀 팩토리 설정
my_servo = Servo(12, pin_factory=factory)

motor_stop_event = threading.Event()  # 모터 정지 이벤트

def signal_handler(sig, frame):
    print("Exiting gracefully")
    motor_stop_event.set()
    finalize_and_exit()  # 여기로 변경


# SIGINT (Ctrl+C) 시그널을 처리하기 위해 핸들러를 설정
signal.signal(signal.SIGINT, signal_handler)

def setup():
    # 서보 초기화
    my_servo.value = 0  # 정지
    time.sleep(1)
    
def read_flag_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()  # 문자열을 그대로 반환
    except IOError:
        print(f"Error reading {filename}")
        return None


def check_run_condition():
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
    window_stat = read_flag_file(os.path.join(config_path, 'window_stat.dat'))
    if window_stat == "close":
        return False
    return True

def write_window_stat():
    # window_stat.dat 파일 작성
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
    window_stat_path = os.path.join(config_path, 'window_stat.dat')
    with open(window_stat_path, 'w') as file:
        file.write("close")
        
def finalize_and_exit():
    write_window_stat()  # window_stat.dat 파일 작성
    print("Operation completed. Exiting program.")
    my_servo.close()  # 서보모터 연결 해제
    GPIO.cleanup()  # GPIO 설정 정리
    sys.exit(0)  # 프로그램 종료
        

def sensor_monitor():
    while not motor_stop_event.is_set():
        if GPIO.input(sensor_pin) == False:
            print("문이 전부 닫혔습니다! 모터 정지.")
            motor_stop_event.set()
            time.sleep(0.2)
            my_servo.value = 0
            finalize_and_exit()  # 여기로 변경

def loop():
    start_time = time.time()
    my_servo.value = -0.7  # 최대 속도로 한쪽 방향으로 회전
    
    while (time.time() - start_time) <= 15:  # 15초 동안 실행
        if GPIO.input(sensor_pin) == False:
            print("문이 전부 닫혔습니다! 모터 정지.")
            motor_stop_event.set()
            time.sleep(0.2)
            my_servo.value = 0
            finalize_and_exit()  # 센서가 문이 닫혔음을 감지하면 종료
        time.sleep(0.1)  # 센서 체크 주기
    
    write_window_stat()  # 15초 후에 실행 종료 및 상태 기록


if __name__ == "__main__":
    run_condition = False
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_condition = True
    else:
        run_condition = check_run_condition()
    setup()
    loop()
    finalize_and_exit()  # 여기로 변경
