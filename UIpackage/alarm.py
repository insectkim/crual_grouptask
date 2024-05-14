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

    checkboxes = {}
    for day in days:
        checkboxes[day] = tk.Checkbutton(checkboxes_frame, text=day, variable=day_vars[day], onvalue=True, offvalue=False)
        checkboxes[day].pack(side='left', padx=1)

    window_open_var = tk.BooleanVar(value=False)
    tk.Checkbutton(frame, text="창문 열기", variable=window_open_var, onvalue=True, offvalue=False).pack(side='left', padx=10)

    remove_button = ttk.Button(frame, text="삭제", command=lambda: remove_entry(frame, entries_list))
    remove_button.pack(side='right')

    entries_list.append(frame)

    if job:
        parts = job.split()
        minute, hour, day_of_month, month, day_of_week = parts[:5]
        hour_entry.insert(0, hour)
        minute_entry.insert(0, minute)
        set_day_checkboxes(day_of_week, day_vars, checkboxes)

def set_day_checkboxes(day_of_week_str, day_vars, checkboxes):
    days_map = {
        '0': '일', '1': '월', '2': '화', '3': '수', '4': '목', '5': '금', '6': '토',
        'sun': '일', 'mon': '월', 'tue': '화', 'wed': '수', 'thu': '목', 'fri': '금', 'sat': '토'
    }

    # crontab에서 *는 매일을 의미합니다
    if day_of_week_str == '*':
        for var in day_vars.values():
            var.set(True)
    else:
        # 요일 문자열을 쉼표로 분리하여 각각의 요일을 설정합니다
        days = day_of_week_str.split(',')
        for day in days:
            if day in days_map:
                day_vars[days_map[day]].set(True)
    
    # 체크박스 UI 업데이트
    for day, var in day_vars.items():
        checkboxes[day].update()

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
