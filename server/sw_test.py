import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
sensor_pin = 6

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
# 내부 풀업 저항 활성화
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(sensor_pin):
            print("문이 닫혔습니다!")
        else:
            print("문이 열렸습니다!")
        time.sleep(1)

except KeyboardInterrupt:
    print("종료합니다.")
    GPIO.cleanup()
