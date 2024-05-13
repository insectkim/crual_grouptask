import tkinter as tk
from tkinter import ttk
import pygame
import time
import subprocess
from threading import Thread

# 초기 변수 설정
process = None
is_playing = False
elapsed_time = 0

# 함수 정의
import pygame
import time
import tkinter as tk
from threading import Thread

# 초기 변수 설정
is_playing = False
elapsed_time = 0

def play_music(current_time_label, total_time_label, root):
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\pofwe\Music\alarm.mp3")
    pygame.mixer.music.play()
    
    # 노래 재생 상태와 시간 업데이트 관리
    global is_playing, elapsed_time
    is_playing = True
    elapsed_time = 0

    def track_playback():
        global is_playing, elapsed_time
        while pygame.mixer.music.get_busy() and is_playing:
            time.sleep(1)
            elapsed_time += 1
            root.after(0, lambda: current_time_label.config(text=time.strftime('%M:%S', time.gmtime(elapsed_time))))

    Thread(target=track_playback).start()
    total_time_label.config(text="03:30")  # 예시로 고정된 노래 길이

def stop_music(current_time_label, total_time_label):
    global is_playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    is_playing = False
    current_time_label.config(text="00:00")
    total_time_label.config(text="00:00")

if __name__ == "__main__":
    root = tk.Tk()  # 테스트를 위해 임시로 Tk 객체 생성
    play_music(tk.Label(root, text="00:00"), tk.Label(root, text="03:30"), root)

def add_entry(entries_frame, entries_list):
    frame = ttk.Frame(entries_frame)
    frame.pack(fill='x', padx=5, pady=5)

    hour_entry = ttk.Entry(frame, width=5)
    hour_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="시").pack(side='left')

    minute_entry = ttk.Entry(frame, width=5)
    minute_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="분").pack(side='left')

    days_frame = ttk.Frame(frame)
    days_frame.pack(side='left', fill='x', expand=True, padx=10)

    days = ['월', '화', '수', '목', '금', '토', '일']
    day_vars = {day: tk.BooleanVar() for day in days}

    labels_frame = ttk.Frame(days_frame)
    labels_frame.pack(side='top', fill='x')
    checkboxes_frame = ttk.Frame(days_frame)
    checkboxes_frame.pack(side='top', fill='x')

    for day in days:
        ttk.Label(labels_frame, text=day).pack(side='left', padx=4)
        ttk.Checkbutton(checkboxes_frame, variable=day_vars[day], onvalue=True, offvalue=False).pack(side='left', padx=1)

    window_open_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, text="창문 열기", variable=window_open_var, onvalue=True, offvalue=False).pack(side='left', padx=10)

    remove_button = ttk.Button(frame, text="삭제", command=lambda: remove_entry(frame, entries_list))
    remove_button.pack(side='right')

    entries_list.append(frame)

def remove_entry(frame, entries_list):
    frame.pack_forget()
    frame.destroy()
    entries_list.remove(frame)