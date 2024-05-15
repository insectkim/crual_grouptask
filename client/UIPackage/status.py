from tkinter import ttk

def initialize_status_tab(tab):
    ttk.Label(tab, text="PM 2.5 센서정보").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(tab, text="창문 상태").grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(tab, text="모터 통신 상태 : ").grid(column=0, row=2, padx=10, pady=10)
