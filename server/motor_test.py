from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import signal
import sys

# pigpio 핀 팩토리 설정
factory = PiGPIOFactory()

# 서보모터를 연결할 GPIO 핀 설정 (예: GPIO 12) 및 핀 팩토리 설정
my_servo = Servo(12, pin_factory=factory)

def signal_handler(sig, frame):
    print("Exiting gracefully")
    my_servo.close()
    sys.exit(0)

# SIGINT (Ctrl+C) 시그널을 처리하기 위해 핸들러를 설정
signal.signal(signal.SIGINT, signal_handler)

def setup():
    # 서보 초기화
    my_servo.value = 0  # 정지
    sleep(1)

def loop():
    
    my_servo.value = -0.7  # 최대 속도로 한쪽 방향으로 회전
    sleep(3)
    my_servo.value = 0.7  # 최대 속도로 반대 방향으로 회전
    sleep(3)
    my_servo.value = 0  # 정지
    sleep(5)

if __name__ == "__main__":
    setup()
    while True:
        loop()
