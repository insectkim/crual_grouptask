import tkinter as tk
from tkinter import ttk
import requests

def fetch_crontab_list():
    try:
        response = requests.get('http://192.168.200.113:5000/crontab_list')
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print("Failed to fetch crontab list:", e)
        return []

def add_entry(entries_frame, entries_list, job=None):
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

    if job:
        # job 데이터를 사용하여 입력 필드를 채웁니다
        parts = job.split()
        minute, hour, day_of_month, month, day_of_week = parts[:5]
        hour_entry.insert(0, hour)
        minute_entry.insert(0, minute)
        # 체크박스 설정은 추가 작업이 필요할 수 있습니다

def remove_entry(frame, entries_list):
    frame.pack_forget()
    frame.destroy()
    entries_list.remove(frame)

def initialize_alarm_tab(tab):
    review_frame = ttk.LabelFrame(tab, text="알람 리스트")
    review_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

    entries_frame = ttk.Frame(review_frame)
    entries_frame.pack(fill='x', padx=5, pady=5)
    entries_list = []

    add_button = ttk.Button(review_frame, text="추가", command=lambda: add_entry(entries_frame, entries_list))
    add_button.pack(fill='x', padx=5, pady=5)

    # 초기 알람 엔트리 추가
    crontab_list = fetch_crontab_list()
    for cron_job in crontab_list:
        add_entry(entries_frame, entries_list, cron_job)
