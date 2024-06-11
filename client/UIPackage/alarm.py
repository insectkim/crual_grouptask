import tkinter as tk
from tkinter import ttk
from ConPackage.connect import ServerConnection

WINDOW_OPEN = "창문 열기"
WINDOW_CLOSED = "창문 안열기"

def add_entry(entries_frame, entries_list, job=None):
    """
    알람 항목을 추가합니다.
    """
    frame = ttk.Frame(entries_frame)
    frame.pack(fill='x', padx=5, pady=5)

    hour_entry = ttk.Entry(frame, width=5)
    hour_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="시").pack(side='left')

    minute_entry = ttk.Entry(frame, width=5)
    minute_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="분").pack(side='left')

    days_entry = ttk.Entry(frame, width=15)
    days_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="요일").pack(side='left')

    window_status_entry = ttk.Entry(frame, width=15)
    window_status_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="창문 상태").pack(side='left')

    remove_button = ttk.Button(frame, text="삭제", command=lambda: remove_entry(frame, entries_list))
    remove_button.pack(side='right')

    entries_list.append((frame, hour_entry, minute_entry, days_entry, window_status_entry, job))

    if job:
        print(f"Job: {job}")  # 디버깅용 출력문
        parts = job.split()
        minute, hour, _day_of_month, _month, day_of_week = parts[:5]
        hour_entry.insert(0, hour)
        minute_entry.insert(0, minute)
        days_entry.insert(0, get_day_string(day_of_week))
        
        # Check if 'window' is in the job command
        command = parts[5:]
        if 'window' in command:
            window_status_entry.insert(0, WINDOW_OPEN)
            print(f"Set to {WINDOW_OPEN}")  # 디버깅용 출력문
        else:
            window_status_entry.insert(0, WINDOW_CLOSED)
            print(f"Set to {WINDOW_CLOSED}")  # 디버깅용 출력문

def get_day_string(day_of_week_str):
    """
    요일 문자열을 한글자로 변환합니다.
    """
    days_map = {
        '0': '일', '1': '월', '2': '화', '3': '수', '4': '목', '5': '금', '6': '토',
        'sun': '일', 'mon': '월', 'tue': '화', 'wed': '수', 'thu': '목', 'fri': '금', 'sat': '토'
    }

    if day_of_week_str == '*':
        return "일월화수목금토"

    day_str = ""
    days = day_of_week_str.split(',')
    for day in days:
        if day in days_map:
            day_str += days_map[day]

    return day_str

def remove_entry(frame, entries_list):
    """
    알람 항목을 삭제합니다.
    """
    for entry in entries_list:
        if entry[0] == frame:
            entries_list.remove(entry)
            break
    frame.pack_forget()
    frame.destroy()

def gather_crontab_data(entries_list, command):
    """
    크론탭 데이터를 수집합니다.
    """
    day_map_reverse = {
        '일': '0', '월': '1', '화': '2', '수': '3', '목': '4', '금': '5', '토': '6'
    }

    crontab_data = []
    for entry in entries_list:
        frame, hour_entry, minute_entry, days_entry, window_status_entry, _job = entry
        days_selected = [day_map_reverse[char] for char in days_entry.get() if char in day_map_reverse]
        if days_selected:
            day_field = ','.join(days_selected)
        else:
            day_field = '*'

        # Remove any existing 'window' in the command
        command_cleaned = ' '.join([part for part in command.split() if part != 'window'])

        if window_status_entry.get() == WINDOW_OPEN:
            command_with_flag = f"{command_cleaned} window"
        else:
            command_with_flag = command_cleaned

        crontab_line = f"{minute_entry.get()} {hour_entry.get()} * * {day_field} {command_with_flag}"
        crontab_data.append(crontab_line)
    return crontab_data

def save_crontab(entries_list, command, server_connection):
    """
    크론탭 데이터를 서버에 저장합니다.
    """
    crontab_data = gather_crontab_data(entries_list, command)
    response = server_connection.send_request('update_crontab', method='POST', data={'crontab': crontab_data})
    if response.get('status') == 'success':
        print("Crontab successfully updated.")
    else:
        print(f"Failed to update crontab. Response: {response}")

def initialize_alarm_tab(tab, server_connection):
    """
    알람관리 탭을 초기화합니다.
    """
    review_frame = ttk.LabelFrame(tab, text="알람 리스트")
    review_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

    entries_frame = ttk.Frame(review_frame)
    entries_frame.pack(fill='x', padx=5, pady=5)
    entries_list = []

    response = server_connection.send_request('crontab_list')
    crontab_list = response if isinstance(response, list) else response.get('data', [])
    
    if crontab_list:
        first_cron_job = crontab_list[0]
        command = first_cron_job.split(' ', 5)[-1]
        for cron_job in crontab_list:
            add_entry(entries_frame, entries_list, cron_job)
    else:
        command = "명령어 없음"

    add_button = ttk.Button(review_frame, text="추가", command=lambda: add_entry(entries_frame, entries_list))
    add_button.pack(fill='x', padx=5, pady=5)

    save_button = ttk.Button(tab, text="저장", command=lambda: save_crontab(entries_list, command, server_connection))
    save_button.grid(column=0, row=1, padx=10, pady=10)

    refresh_button = ttk.Button(tab, text="새로고침", command=lambda: refresh_alarms(tab, server_connection))
    refresh_button.grid(column=0, row=2, padx=10, pady=10)

def refresh_alarms(tab, server_connection):
    """
    서버에서 알람 리스트를 받아와서 알람 탭을 초기화합니다.
    """
    entries_frame = tab.winfo_children()[0].winfo_children()[0]
    entries_list = []

    response = server_connection.send_request('crontab_list')
    crontab_list = response if isinstance(response, list) else response.get('data', [])

    if crontab_list:
        for cron_job in crontab_list:
            add_entry(entries_frame, entries_list, cron_job)
    
    entries_frame.update_idletasks()  # 강제 UI 업데이트
