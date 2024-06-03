import tkinter as tk
from tkinter import ttk
from UIPackage.alarm import initialize_alarm_tab, fetch_alarms
from UIPackage.test import initialize_test_tab
from UIPackage.status import initialize_status_tab
from UIPackage.config import initialize_config_tab
from ConPackage.connect import initialize_server_variables, attempt_connection

def show_main_ui():
    """
    메인 UI를 표시합니다.
    """
    # 메인 윈도우 생성 및 UI 구성
    root = tk.Tk()
    root.title("스마트 창문 시스템")

    # 서버 변수 초기화
    initialize_server_variables(root)

    tab_control = ttk.Notebook(root)

    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='상태정보')
    tab_control.add(tab2, text='알람관리')
    tab_control.add(tab3, text='수동실행')
    tab_control.add(tab4, text='설정관리')
    tab_control.pack(expand=1, fill="both")

    # 상태 탭 초기화
    initialize_status_tab(tab1)

    # 알람관리 탭 초기화
    initialize_alarm_tab(tab2)

    # 수동실행 탭 초기화
    initialize_test_tab(tab3)

    # 설정관리 탭 초기화
    initialize_config_tab(tab4)

    # 알람 리스트를 서버에서 받아옴
    fetch_alarms(tab2)

    root.mainloop()

def show_initial_input():
    """
    초기 서버 IP 입력 창을 표시합니다.
    """
    initial_root = tk.Tk()
    initial_root.title("서버 접속 설정")

    # 서버 변수 초기화
    initialize_server_variables(initial_root)

    ttk.Label(initial_root, text="서버 IP:").grid(column=0, row=0, padx=5, pady=5)
    server_ip_entry = ttk.Entry(initial_root)
    server_ip_entry.grid(column=1, row=0, padx=5, pady=5)

    status_label = ttk.Label(initial_root, text="")
    status_label.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

    connect_button = ttk.Button(initial_root, text="접속", command=lambda: attempt_connection(initial_root, server_ip_entry, status_label, show_main_ui))
    connect_button.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

    initial_root.mainloop()

# 초기 입력 창 표시
show_initial_input()
