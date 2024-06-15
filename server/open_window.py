from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
import threading
import time 
import signal
import sys
import os

# GPIO 핀 설정(리드 스위치)
sensor_pin = 4
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
    finalize_and_exit()  # 여기에서 함수 호출


# SIGINT (Ctrl+C) 시그널을 처리하기 위해 핸들러를 설정
signal.signal(signal.SIGINT, signal_handler)

def setup():
    # 서보 초기화
    my_servo.value = 0  # 정지
    time.sleep(1)

def read_flag_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()  # 파일에서 읽은 값을 문자열로 반환
    except IOError:
        print(f"Error reading {filename}")
        return None


def check_run_condition():
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
    dust_flag = read_flag_file(os.path.join(config_path, 'dust_flag.dat'))
    wea_flag = read_flag_file(os.path.join(config_path, 'wea_flag.dat'))
    window_stat = read_flag_file(os.path.join(config_path, 'window_stat.dat'))

    try:
        dust_flag = int(dust_flag) if dust_flag is not None else None
        wea_flag = int(wea_flag) if wea_flag is not None else None
    except ValueError:
        print("dust_flag 또는 wea_flag 파일에 유효하지 않은 값이 있습니다.")
        return False

    if window_stat == "open":
        return False

    return (dust_flag == 0 and wea_flag == 0) if (dust_flag is not None and wea_flag is not None) else False


def write_window_stat():
    # window_stat.dat 파일 작성
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config')
    window_stat_path = os.path.join(config_path, 'window_stat.dat')
    with open(window_stat_path, 'w') as file:
        file.write("open")
        
def finalize_and_exit():
    write_window_stat()  # window_stat.dat 파일 작성
    print("Operation completed. Exiting program.")
    my_servo.close()  # 서보모터 연결 해제
    GPIO.cleanup()  # GPIO 설정 정리
    sys.exit(0)  # 프로그램 종료


def sensor_monitor():
    while not motor_stop_event.is_set():
        if GPIO.input(sensor_pin) == False:
            print("문이 전부 열렸습니다! 모터 정지.")
            motor_stop_event.set()
            time.sleep(0.2)
            my_servo.value = 0
            finalize_and_exit() # 프로그램을 즉시 종료

def loop(run_condition):
    if run_condition:
        start_time = time.time()  # 시작 시간 기록
        my_servo.value = 0.7  # 최대 속도로 한쪽 방향으로 회전

        while not motor_stop_event.is_set() and (time.time() - start_time) <= 15:
            if GPIO.input(sensor_pin) == False:
                print("문이 전부 열렸습니다! 모터 정지.")
                motor_stop_event.set()
                time.sleep(0.2)
                my_servo.value = 0
                break  # 루프 종료

            time.sleep(0.1)  # 센서 상태를 체크하는 간격

    finalize_and_exit()


if __name__ == "__main__":
    setup()
    run_condition = False
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_condition = True
    else:
        run_condition = check_run_condition()

    loop(run_condition)
