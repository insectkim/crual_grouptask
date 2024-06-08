import tkinter as tk
from tkinter import ttk

def initialize_status_tab(tab, server_connection):
    server_frame = ttk.LabelFrame(tab, text="서버 상태")
    server_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

    status_lamp = tk.Label(server_frame, text=" ", bg="red", width=2, height=1)
    status_lamp.grid(column=0, row=0, padx=5, pady=5)

    server_ip_label = ttk.Label(server_frame, text=f"서버 IP: {server_connection.server_ip.get()}")
    server_ip_label.grid(column=1, row=0, padx=5, pady=5)

    update_button = ttk.Button(server_frame, text="상태 업데이트", command=lambda: update_server_status(status_lamp, server_connection))
    update_button.grid(column=2, row=0, padx=5, pady=5)

def update_server_status(status_lamp, server_connection):
    if server_connection.check_server_connection(server_connection.server_ip.get()):
        status_lamp.config(bg="green")
    else:
        status_lamp.config(bg="red")
