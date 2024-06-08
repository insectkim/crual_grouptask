import pigpio
import time
import numpy as np
import matplotlib.pyplot as plt

# ����
SIGNAL_PIN = 21  # ��ȣ�� �޴� �� ��ȣ (BCM 21)
SAMPLE_DURATION = 5  # ���ø� �Ⱓ (��)
SAMPLE_RATE = 10000  # ���ø� �ӵ� (Hz)

pi = pigpio.pi()

if not pi.connected:
    exit()

# ���ø� ������ ����� ����Ʈ
times = []
levels = []

# �ݹ� �Լ� ����
def signal_callback(gpio, level, tick):
    global times, levels
    times.append(tick)
    levels.append(level)
    print(f"Callback: gpio={gpio}, level={level}, tick={tick}")

# �ʱ� �� ����
pi.set_mode(SIGNAL_PIN, pigpio.INPUT)
cb = pi.callback(SIGNAL_PIN, pigpio.EITHER_EDGE, signal_callback)

# ���ø� ����
start_time = time.time()
while time.time() - start_time < SAMPLE_DURATION:
    time.sleep(1 / SAMPLE_RATE)

# ���ø� �Ϸ�
pi.stop()

# ������ ��ó��
if len(times) == 0:
    print("No data collected.")
else:
    times = np.array(times)
    levels = np.array(levels)

    # �ð� �������� 0���� �����ϵ��� ����
    times = (times - times[0]) / 1e6  # ����ũ���ʸ� �ʷ� ��ȯ

    # ���� �׸���
    plt.figure(figsize=(10, 6))
    plt.plot(times, levels, drawstyle='steps-pre')
    plt.title("Signal Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Level")
    plt.grid(True)
    plt.show()

    # ��ȣ Ư�� �м�
    high_durations = []
    low_durations = []
    last_time = times[0]

    for i in range(1, len(times)):
        duration = times[i] - last_time
        if levels[i-1] == 1:
            high_durations.append(duration)
        else:
            low_durations.append(duration)
        last_time = times[i]

    if high_durations and low_durations:
        avg_high_duration = np.mean(high_durations)
        avg_low_duration = np.mean(low_durations)
        period = avg_high_duration + avg_low_duration
        duty_cycle = (avg_high_duration / period) * 100

        print(f"Average High Duration: {avg_high_duration:.6f} s")
        print(f"Average Low Duration: {avg_low_duration:.6f} s")
        print(f"Period: {period:.6f} s")
        print(f"Duty Cycle: {duty_cycle:.2f} %")
    else:
        print("Insufficient data for analysis.")
