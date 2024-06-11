import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

class TestManager:
    def __init__(self, server_connection):
        self.server_connection = server_connection
        self.is_playing = False
        self.elapsed_time = 0

    def play_music(self, current_time_label, total_time_label, root):
        response = self.server_connection.send_request('play_music')
        if response and response['status'] == 'success':
            self.is_playing = True
            self.elapsed_time = 0

            def track_playback():
                while self.is_playing:
                    time.sleep(1)
                    self.elapsed_time += 1
                    root.after(0, lambda: current_time_label.config(text=time.strftime('%M:%S', time.gmtime(self.elapsed_time))))

            Thread(target=track_playback).start()
            total_time_label.config(text="03:30")

    def stop_music(self, current_time_label, total_time_label):
        response = self.server_connection.send_request('stop_music')
        if response and response['status'] == 'success':
            self.is_playing = False
            reset_count=0
            while reset_count >=3 :
                current_time_label.config(text="00:00")
                reset_count += 1
                time.sleep(1)
            total_time_label.config(text="00:00")

    def control_window(self, action):
        # 메인 스레드에서 서버 IP와 포트를 가져옵니다.
        server_ip_with_port = self.server_connection.get_server_ip_with_port()
        # 서버에 'open_window' 또는 'close_window' 요청을 비동기적으로 보냅니다.
        if action == 'open':
            thread = Thread(target=self._send_window_request, args=(server_ip_with_port, 'open_window'))
        elif action == 'close':
            thread = Thread(target=self._send_window_request, args=(server_ip_with_port, 'close_window'))
        thread.start()

    def _send_window_request(self, server_ip_with_port, endpoint):
        self.server_connection.send_request(endpoint, server_ip_with_port=server_ip_with_port)

def initialize_test_tab(tab, server_connection):
    test_manager = TestManager(server_connection)

    current_time_label = ttk.Label(tab, text="00:00")
    current_time_label.grid(column=2, row=2, padx=10, pady=5)
    total_time_label = ttk.Label(tab, text="00:00")
    total_time_label.grid(column=3, row=2, padx=10, pady=5)

    ttk.Button(tab, text="노래 재생", command=lambda: test_manager.play_music(current_time_label, total_time_label, tab)).grid(column=0, row=2, padx=10, pady=10)
    ttk.Button(tab, text="노래 중지", command=lambda: test_manager.stop_music(current_time_label, total_time_label)).grid(column=4, row=2, padx=10, pady=10)

    ttk.Button(tab, text="창문 열기", command=lambda: test_manager.control_window('open')).grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(tab, text="창문 닫기", command=lambda: test_manager.control_window('close')).grid(column=0, row=1, padx=10, pady=10)