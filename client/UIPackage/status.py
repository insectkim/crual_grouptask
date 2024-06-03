import tkinter as tk
from tkinter import ttk
from ConPackage.connect import server_ip, is_server_connected, update_server_status, initialize_server_variables

def initialize_status_tab(tab):
    """
    상태 정보를 표시하는 탭을 초기화합니다.

    Parameters:
        tab (Frame): 상태 정보 탭의 프레임
    """
    root = tab.master.master  # Tk 루트 객체를 가져옵니다.
    initialize_server_variables(root)  # 서버 변수 초기화

    ttk.Label(tab, text="PM 2.5 센서정보").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(tab, text="창문 상태").grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(tab, text="모터 통신 상태 : ").grid(column=0, row=2, padx=10, pady=10)

    # 서버 설정 영역
    server_frame = ttk.LabelFrame(tab, text="서버 설정")
    server_frame.grid(column=0, row=3, padx=10, pady=10, sticky="ew")

    ttk.Label(server_frame, text="서버 IP:").grid(column=0, row=0, padx=5, pady=5)
    server_ip_entry = ttk.Entry(server_frame, textvariable=server_ip)
    server_ip_entry.grid(column=1, row=0, padx=5, pady=5)

    status_lamp = tk.Label(server_frame, text=" ", bg="red", width=2, height=1)
    status_lamp.grid(column=1, row=1, padx=5, pady=5)

    server_toggle_button = ttk.Button(server_frame, text="서버 접속", command=lambda: update_server_status(status_lamp))
    server_toggle_button.grid(column=0, row=1, padx=5, pady=5)
