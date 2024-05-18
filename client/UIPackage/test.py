import tkinter as tk
from tkinter import ttk
from ConPackage.connect import send_request
from threading import Thread
import time

class MusicPlayer:
    @staticmethod
    def play_music(current_time_label, total_time_label, root):
        """
        음악을 재생하고 재생 시간을 업데이트합니다.

        Parameters:
            current_time_label (Label): 현재 재생 시간 라벨
            total_time_label (Label): 총 재생 시간 라벨
            root (Tk): Tk 루트 윈도우
        """
        send_request('play_music')

        global is_playing, elapsed_time
        is_playing = True
        elapsed_time = 0

        def track_playback():
            global is_playing, elapsed_time
            while is_playing:
                time.sleep(1)
                elapsed_time += 1
                root.after(0, lambda: current_time_label.config(text=time.strftime('%M:%S', time.gmtime(elapsed_time))))

        Thread(target=track_playback).start()
        total_time_label.config(text="03:30")  # 예시로 고정된 노래 길이

    @staticmethod
    def stop_music(current_time_label, total_time_label):
        """
        음악 재생을 중지하고 시간을 초기화합니다.

        Parameters:
            current_time_label (Label): 현재 재생 시간 라벨
            total_time_label (Label): 총 재생 시간 라벨
        """
        send_request('stop_music')
        global is_playing
        is_playing = False
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

    ttk.Button(tab, text="노래 재생", command=lambda: MusicPlayer.play_music(current_time_label, total_time_label, tab)).grid(column=0, row=2, padx=10, pady=10)
    ttk.Button(tab, text="노래 중지", command=lambda: MusicPlayer.stop_music(current_time_label, total_time_label)).grid(column=4, row=2, padx=10, pady=10)

    ttk.Button(tab, text="창문 열기").grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(tab, text="창문 닫기").grid(column=0, row=1, padx=10, pady=10)
