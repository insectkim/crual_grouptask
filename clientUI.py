import tkinter as tk
from tkinter import ttk
import subprocess
import time
from threading import Thread
# 함수 정의

def play_music():
    global process, is_playing, elapsed_time
    if process is None or process.poll() is not None:
        process = subprocess.Popen(["python", "client_act.py"])
        total_time_label.config(text="03:30")  # 노래시간, 프로세스간 통신을 구현하지 않아서 상수로 표기
        is_playing = True
        elapsed_time = 0
        update_time()

def stop_music():
    global process, is_playing
    if process is not None:
        process.terminate()
        process = None
        is_playing = False
        current_time_label.config(text="00:00")
        total_time_label.config(text="00:00")

def update_time():
    global elapsed_time
    if is_playing:
        elapsed_time += 1
        current_time_label.config(text=time.strftime('%M:%S', time.gmtime(elapsed_time)))
        root.after(1000, update_time)  # Update every second

        
def add_entry():
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

    remove_button = ttk.Button(frame, text="삭제", command=lambda: remove_entry(frame))
    remove_button.pack(side='right')

    entries_list.append(frame)

def remove_entry(frame):
    frame.pack_forget()
    frame.destroy()
    entries_list.remove(frame)

#초기변수들 정리
process = None
is_playing = False
elapsed_time = 0

# 메인 윈도우 생성 및 UI 구성
root = tk.Tk()
root.title("스마트 창문 시스템")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='상태정보')
tabControl.add(tab2, text='알람관리')
tabControl.add(tab3, text='수동실행')
tabControl.add(tab4, text='설정관리')
tabControl.pack(expand=1, fill="both")

ttk.Label(tab1, text="PM 2.5 센서정보").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(tab1, text="창문 상태").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(tab1, text="모터 통신 상태 : ").grid(column=0, row=2, padx=10, pady=10)

review_frame = ttk.LabelFrame(tab2, text="알람 리스트")
review_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

entries_frame = ttk.Frame(review_frame)
entries_frame.pack(fill='x', padx=5, pady=5)

entries_list = []

add_button = ttk.Button(review_frame, text="추가", command=add_entry)
add_button.pack(fill='x', padx=5, pady=5)

add_entry()  # 최초 한 번 입력 세트 추가

ttk.Button(tab3, text="창문 열기").grid(column=0, row=0, padx=10, pady=10)
ttk.Button(tab3, text="창문 닫기").grid(column=0, row=1, padx=10, pady=10)
ttk.Button(tab3, text="노래 재생", command=play_music).grid(column=0, row=2, padx=10, pady=10)
current_time_label = ttk.Label(tab3, text="00:00")
current_time_label.grid(column=2, row=2, padx=10, pady=5)
total_time_label = ttk.Label(tab3, text="00:00")
total_time_label.grid(column=3, row=2, padx=10, pady=5)
ttk.Button(tab3, text="노래 중지", command=stop_music).grid(column=4, row=2, padx=10, pady=10)

ttk.Label(tab4, text="기상 플래그").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(tab4, text="먼지 플래그").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(tab4, text="모터 위치 : ").grid(column=0, row=2, padx=10, pady=10)

root.mainloop()
