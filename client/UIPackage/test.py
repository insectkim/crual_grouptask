from ConPackage.connect import send_request
from tkinter import ttk
import tkinter as tk
import time
from threading import Thread

# 전역 변수 초기화
is_playing = False
elapsed_time = 0

def play_music_handler(current_time_label, total_time_label, root):
    """
    서버에 음악 재생 명령을 전송하고 재생 시간을 업데이트합니다.

    Parameters:
        current_time_label (Label): 현재 재생 시간을 표시하는 라벨
        total_time_label (Label): 총 재생 시간을 표시하는 라벨
        root (Tk): 메인 윈도우 객체
    """
    global is_playing, elapsed_time
    is_playing = True
    elapsed_time = 0

    # 서버로 재생 명령 전송
    response = send_request('play_music', method='POST')
    if response['status'] != 'success':
        print("Failed to start music playback on server.")
        is_playing = False
        return

    def track_playback():
        """
        음악 재생 시간을 추적하여 UI를 업데이트합니다.
        """
        global is_playing, elapsed_time
        while is_playing:
            time.sleep(1)
            elapsed_time += 1
            root.after(0, lambda: current_time_label.config(text=time.strftime('%M:%S', time.gmtime(elapsed_time))))

    # 백그라운드에서 재생 시간 추적
    Thread(target=track_playback).start()
    total_time_label.config(text="03:30")  # 예시로 고정된 노래 길이

def stop_music_handler(current_time_label, total_time_label):
    """
    서버에 음악 중지 명령을 전송하고 UI를 업데이트합니다.

    Parameters:
        current_time_label (Label): 현재 재생 시간을 표시하는 라벨
        total_time_label (Label): 총 재생 시간을 표시하는 라벨
    """
    global is_playing
    is_playing = False

    # 서버로 정지 명령 전송
    response = send_request('stop_music', method='POST')
    if response['status'] != 'success':
        print("Failed to stop music playback on server.")

    current_time_label.config(text="00:00")
    total_time_label.config(text="00:00")

def initialize_test_tab(tab):
    """
    수동실행 탭을 초기화합니다.

    Parameters:
        tab (Frame): 수동실행 탭의 프레임
    """
    current_time_label = ttk.Label(tab, text="00:00")
    current_time_label.grid(column=2, row=2, padx=10, pady=5)
    total_time_label = ttk.Label(tab, text="00:00")
    total_time_label.grid(column=3, row=2, padx=10, pady=5)

    ttk.Button(tab, text="노래 재생", command=lambda: play_music_handler(current_time_label, total_time_label, tab)).grid(column=0, row=2, padx=10, pady=10)
    ttk.Button(tab, text="노래 중지", command=lambda: stop_music_handler(current_time_label, total_time_label)).grid(column=4, row=2, padx=10, pady=10)

    ttk.Button(tab, text="창문 열기").grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(tab, text="창문 닫기").grid(column=0, row=1, padx=10, pady=10)
