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

def save_crontab_list(crontab_data):
    try:
        response = requests.post('http://192.168.200.113:5000/update_crontab', json=crontab_data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail"}
    except Exception as e:
        print("Failed to save crontab list:", e)
        return {"status": "fail"}

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

    entries_list.append((frame, hour_entry, minute_entry, day_vars, window_open_var, job))

    if job:
        parts = job.split()
        minute, hour, day_of_month, month, day_of_week = parts[:5]
        hour_entry.insert(0, hour)
        minute_entry.insert(0, minute)
        set_day_checkboxes(day_of_week, day_vars)

def set_day_checkboxes(day_of_week_str, day_vars):
    days_map = {
        '0': '일', '1': '월', '2': '화', '3': '수', '4': '목', '5': '금', '6': '토',
        'sun': '일', 'mon': '월', 'tue': '화', 'wed': '수', 'thu': '목', 'fri': '금', 'sat': '토'
    }

    if day_of_week_str == '*':
        for var in day_vars.values():
            var.set(True)
    else:
        days = day_of_week_str.split(',')
        for day in days:
            if day in days_map:
                day_vars[days_map[day]].set(True)

def remove_entry(frame, entries_list):
    for entry in entries_list:
        if entry[0] == frame:
            entries_list.remove(entry)
            break
    frame.pack_forget()
    frame.destroy()

def gather_crontab_data(entries_list, command):
    day_map_reverse = {
        '일': '0', '월': '1', '화': '2', '수': '3', '목': '4', '금': '5', '토': '6'
    }

    crontab_data = []
    for entry in entries_list:
        frame, hour_entry, minute_entry, day_vars, window_open_var, job = entry
        days_selected = [day_map_reverse[day] for day, var in day_vars.items() if var.get()]
        if days_selected:
            day_field = ','.join(days_selected)
        else:
            day_field = '*'

        crontab_line = f"{minute_entry.get()} {hour_entry.get()} * * {day_field} {command}"
        crontab_data.append(crontab_line)
    return crontab_data

def save_crontab(entries_list, command):
    crontab_data = gather_crontab_data(entries_list, command)
    response = save_crontab_list(crontab_data)
    if response['status'] == 'success':
        print("Crontab successfully updated.")
    else:
        print("Failed to update crontab.")

def initialize_alarm_tab(tab):
    review_frame = ttk.LabelFrame(tab, text="알람 리스트")
    review_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

    entries_frame = ttk.Frame(review_frame)
    entries_frame.pack(fill='x', padx=5, pady=5)
    entries_list = []

    crontab_list = fetch_crontab_list()
    if crontab_list:
        first_cron_job = crontab_list[0]
        command = first_cron_job.split(' ', 5)[-1]
        for cron_job in crontab_list:
            add_entry(entries_frame, entries_list, cron_job)
    else:
        command = "명령어 없음"

    add_button = ttk.Button(review_frame, text="추가", command=lambda: add_entry(entries_frame, entries_list))
    add_button.pack(fill='x', padx=5, pady=5)

    save_button = ttk.Button(tab, text="저장", command=lambda: save_crontab(entries_list, command))
    save_button.grid(column=0, row=1, padx=10, pady=10)
