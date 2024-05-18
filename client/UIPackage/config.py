import tkinter as tk
from tkinter import ttk

def initialize_config_tab(tab):
    """
    설정관리 탭을 초기화합니다.

    Parameters:
        tab (Frame): 설정관리 탭의 프레임
    """
    ttk.Label(tab, text="기상 플래그").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(tab, text="먼지 플래그").grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(tab, text="모터 위치 : ").grid(column=0, row=2, padx=10, pady=10)
