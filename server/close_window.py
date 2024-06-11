from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
import threading
from time import sleep
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
    motor_stop_event.set()  # 모든 스레드 종료 신호 보내기
    my_servo.close()
    GPIO.cleanup()
    sys.exit(0)

# SIGINT (Ctrl+C) 시그널을 처리하기 위해 핸들러를 설정
signal.signal(signal.SIGINT, signal_handler)

def setup():
    # 서보 초기화
    my_servo.value = 0  # 정지
    sleep(1)
    
def read_flag_file(filename):
    try:
        with open(filename, 'r') as file:
            return int(file.read().strip())
    except IOError:
        print(f"Error reading {filename}")
        return None

def check_run_condition():
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
    window_stat = read_flag_file(os.path.join(config_path, 'window_stat.dat'))
    if window_stat == "close" :
        return False
    return True   

def write_window_stat():
    # window_stat.dat 파일 작성
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
    window_stat_path = os.path.join(config_path, 'window_stat.dat')
    with open(window_stat_path, 'w') as file:
        file.write("close")

def sensor_monitor():
    while not motor_stop_event.is_set():
        if GPIO.input(sensor_pin) == False:
            print("문이 전부 닫혔습니다! 모터 정지.")
            motor_stop_event.set()
            sleep(0.2)
            my_servo.value = 0
            write_window_stat()  # window_stat.dat 파일 작성
            sys.exit(0)  # 프로그램을 즉시 종료
        sleep(0.1)

def loop():
    threading.Thread(target=sensor_monitor).start()  # 센서 모니터링 스레드 시작
    my_servo.value = 0.7  # 최대 속도로 반대 방향으로 회전
    sleep(15)
    write_window_stat()  # 항상 실행 후에 window_stat.dat 파일 작성

if __name__ == "__main__":
    run_condition = False
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_condition = True
    else:
        run_condition = check_run_condition()
    setup()
    loop()
    print("Operation completed. Exiting program.")
    my_servo.close()  # Clean up and close the servo connection
    GPIO.cleanup()
    sys.exit(0)
