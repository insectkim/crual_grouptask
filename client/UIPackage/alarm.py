import tkinter as tk
from tkinter import ttk
from ConPackage.connect import ServerConnection

class AlarmManager:
    def __init__(self, server_connection):
        self.server_connection = server_connection
        self.entries_list = []

    def fetch_crontab_list(self):
        response = self.server_connection.send_request('crontab_list')
        if isinstance(response, list):
            return response
        return []

    def save_crontab_list(self, crontab_data):
        return self.server_connection.send_request('update_crontab', method='POST', data=crontab_data)

    def add_entry(self, entries_frame, job=None):
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

        remove_button = ttk.Button(frame, text="삭제", command=lambda: self.remove_entry(frame))
        remove_button.pack(side='right')

        self.entries_list.append((frame, hour_entry, minute_entry, day_vars, window_open_var, job))

        if job:
            parts = job.split()
            if len(parts) >= 5:
                minute, hour, _day_of_month, _month, day_of_week = parts[:5]
                hour_entry.insert(0, hour)
                minute_entry.insert(0, minute)
                self.set_day_checkboxes(day_of_week, day_vars)

    def set_day_checkboxes(self, day_of_week_str, day_vars):
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

    def remove_entry(self, frame):
        frame.pack_forget()
        frame.destroy()
        self.entries_list = [entry for entry in self.entries_list if entry[0] != frame]

    def gather_crontab_data(self, command):
        day_map_reverse = {
            '일': '0', '월': '1', '화': '2', '수': '3', '목': '4', '금': '5', '토': '6'
        }

        crontab_data = []
        for entry in self.entries_list:
            frame, hour_entry, minute_entry, day_vars, window_open_var, job = entry
            days_selected = [day_map_reverse[day] for day, var in day_vars.items() if var.get()]
            if days_selected:
                day_field = ','.join(days_selected)
            else:
                day_field = '*'

            crontab_line = f"{minute_entry.get()} {hour_entry.get()} * * {day_field} {command}"
            crontab_data.append(crontab_line)
        return crontab_data

    def save_crontab(self, command):
        crontab_data = self.gather_crontab_data(command)
        response = self.save_crontab_list(crontab_data)
        if response['status'] == 'success':
            print("Crontab successfully updated.")
        else:
            print("Failed to update crontab.")

def initialize_alarm_tab(tab, server_connection):
    review_frame = ttk.LabelFrame(tab, text="알람 리스트")
    review_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

    entries_frame = ttk.Frame(review_frame)
    entries_frame.pack(fill='x', padx=5, pady=5)

    alarm_manager = AlarmManager(server_connection)

    add_button = ttk.Button(review_frame, text="추가", command=lambda: alarm_manager.add_entry(entries_frame))
    add_button.pack(fill='x', padx=5, pady=5)

    save_button = ttk.Button(tab, text="저장", command=lambda: alarm_manager.save_crontab("명령어 없음"))
    save_button.grid(column=0, row=1, padx=10, pady=10)

    tab.master.master.after(1000, lambda: fetch_alarms(tab, alarm_manager))

def fetch_alarms(tab, alarm_manager):
    entries_frame = tab.winfo_children()[0].winfo_children()[0]

    crontab_list = alarm_manager.fetch_crontab_list()
    if crontab_list:
        first_cron_job = crontab_list[0]
        command = first_cron_job.split(' ', 5)[-1]
        for cron_job in crontab_list:
            alarm_manager.add_entry(entries_frame, cron_job)
        save_button = tab.winfo_children()[1]
        save_button.configure(command=lambda: alarm_manager.save_crontab(command))
