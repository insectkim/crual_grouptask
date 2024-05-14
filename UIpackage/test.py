import tkinter as tk
from tkinter import ttk
import pygame
from threading import Thread
import time

def play_music(current_time_label, total_time_label, root):
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\pofwe\Music\alarm.mp3")
    pygame.mixer.music.play()
    
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

def initialize_test_tab(tab):
    current_time_label = ttk.Label(tab, text="00:00")
    current_time_label.grid(column=2, row=2, padx=10, pady=5)
    total_time_label = ttk.Label(tab, text="00:00")
    total_time_label.grid(column=3, row=2, padx=10, pady=5)

    ttk.Button(tab, text="노래 재생", command=lambda: play_music(current_time_label, total_time_label, tab)).grid(column=0, row=2, padx=10, pady=10)
    ttk.Button(tab, text="노래 중지", command=lambda: stop_music(current_time_label, total_time_label)).grid(column=4, row=2, padx=10, pady=10)

    ttk.Button(tab, text="창문 열기").grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(tab, text="창문 닫기").grid(column=0, row=1, padx=10, pady=10)
