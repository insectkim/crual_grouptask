import pigpio
import time

# ����
PWM_PIN = 21  # PWM ��ȣ�� �޴� �� ��ȣ (BCM 21)

pi = pigpio.pi()

if not pi.connected:
    exit()

# �ݹ� �Լ� ����
def pwm_callback(gpio, level, tick):
    global last_tick, pulse_width, period, duty_cycle, new_data
    if level == 1:  # ��ȣ�� HIGH�� ��
        pulse_width = tick - last_tick
    elif level == 0:  # ��ȣ�� LOW�� ��
        period = tick - last_tick
        if period > 0:
            duty_cycle = (pulse_width / period) * 100
        new_data = True
    last_tick = tick

# �ʱ� �� ����
last_tick = 0
pulse_width = 0
period = 0
duty_cycle = 0
new_data = False

# �ݹ� ����
pi.callback(PWM_PIN, pigpio.EITHER_EDGE, pwm_callback)

try:
    while True:
        if new_data:
            print(f"Pulse Width: {pulse_width} us, Period: {period} us, Duty Cycle: {duty_cycle:.2f}%")
            new_data = False
        else:
            print("No new data")
        time.sleep(1)  # 1�� �������� ���� ����
except KeyboardInterrupt:
    print("Program terminated")
finally:
    pi.stop()
