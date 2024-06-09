import tkinter as tk
from tkinter import ttk
from UIPackage.test import initialize_test_tab
from UIPackage.alarm import initialize_alarm_tab
from UIPackage.status import initialize_status_tab
from UIPackage.config import initialize_config_tab
from ConPackage.connect import ServerConnection

# 서버 연결 설정
server_connection = ServerConnection()

# 메인 윈도우 생성 및 UI 구성
def show_main_ui():
    root = tk.Tk()
    root.title("스마트 창문 시스템")

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

    initialize_status_tab(tab1, server_connection)
    initialize_alarm_tab(tab2, server_connection)
    initialize_test_tab(tab3, server_connection)
    initialize_config_tab(tab4)

    root.mainloop()

# 초기 서버 연결 설정 UI
def show_initial_ui():
    initial_root = tk.Tk()
    initial_root.title("서버 설정")

    tk.Label(initial_root, text="서버 IP:").pack(padx=10, pady=10)
    server_ip_entry = tk.Entry(initial_root)
    server_ip_entry.pack(padx=10, pady=10)
    server_ip_entry.insert(0, server_connection.server_ip.get())

    status_label = tk.Label(initial_root, text="")
    status_label.pack(padx=10, pady=10)

    def attempt_connection():
        server_ip = server_ip_entry.get()
        if server_connection.check_server_connection(server_ip):
            server_connection.server_ip.set(server_ip)
            status_label.config(text="접속 성공", fg="green")
            initial_root.destroy()
            show_main_ui()
        else:
            status_label.config(text="접속 실패, 다시 시도하세요.", fg="red")

    connect_button = tk.Button(initial_root, text="접속", command=attempt_connection)
    connect_button.pack(padx=10, pady=10)

    initial_root.mainloop()

# 초기 UI 실행
show_initial_ui()
