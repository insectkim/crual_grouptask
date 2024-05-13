import tkinter as tk
from tkinter import ttk
from UIpackage.client_act import add_entry, play_music, stop_music

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

add_button = ttk.Button(review_frame, text="추가", command=lambda: add_entry(entries_frame, entries_list))
add_button.pack(fill='x', padx=5, pady=5)

add_entry(entries_frame, entries_list)

ttk.Button(tab3, text="창문 열기").grid(column=0, row=0, padx=10, pady=10)
ttk.Button(tab3, text="창문 닫기").grid(column=0, row=1, padx=10, pady=10)

# 노래 재생, 중지 버튼과 라벨 연결
current_time_label = ttk.Label(tab3, text="00:00")
current_time_label.grid(column=2, row=2, padx=10, pady=5)
total_time_label = ttk.Label(tab3, text="00:00")
total_time_label.grid(column=3, row=2, padx=10, pady=5)

ttk.Button(tab3, text="노래 재생", command=lambda: play_music(current_time_label, total_time_label, root)).grid(column=0, row=2, padx=10, pady=10)
ttk.Button(tab3, text="노래 중지", command=lambda: stop_music(current_time_label, total_time_label)).grid(column=4, row=2, padx=10, pady=10)

ttk.Label(tab4, text="기상 플래그").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(tab4, text="먼지 플래그").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(tab4, text="모터 위치 : ").grid(column=0, row=2, padx=10, pady=10)

root.mainloop()
