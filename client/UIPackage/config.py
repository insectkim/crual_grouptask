import tkinter as tk
from tkinter import ttk
from ConPackage.connect import ServerConnection
    
def initialize_config_tab(tab, server_connection):
    """
    설정관리 탭을 초기화합니다.

    Parameters:
        tab (tk.Frame): 설정관리 탭의 프레임
    """


    def update_flags():
        response = server_connection.send_request('get_flags')
        if response['status_code'] == 200:
            result = response['data']
            wea_flag = result.get('wea_flag', 'unknown')
            dust_flag = result.get('dust_flag', 'unknown')
            window_state = result.get('window_state', 'unknown')

            wea_flag_label.config(text=f"Weather Flag: {wea_flag}")
            dust_flag_label.config(text=f"Dust Flag: {dust_flag}")
            window_state_label.config(text=f"Window State: {window_state}")
        else:
            wea_flag_label.config(text="Weather Flag: Error")
            dust_flag_label.config(text="Dust Flag: Error")
            window_state_label.config(text="Window State: Error")

    update_button = ttk.Button(tab, text="플래그 업데이트", command=update_flags)
    update_button.grid(column=0, row=0, padx=10, pady=10)

    wea_flag_label = ttk.Label(tab, text="Weather Flag: unknown")
    wea_flag_label.grid(column=0, row=1, padx=10, pady=5)

    dust_flag_label = ttk.Label(tab, text="Dust Flag: unknown")
    dust_flag_label.grid(column=0, row=2, padx=10, pady=5)

    window_state_label = ttk.Label(tab, text="Window State: unknown")
    window_state_label.grid(column=0, row=3, padx=10, pady=5)

server_connection = ServerConnection()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Configuration")

    tab_control = ttk.Notebook(root)
    config_tab = ttk.Frame(tab_control)
    tab_control.add(config_tab, text='설정관리')
    tab_control.pack(expand=1, fill="both")

    initialize_config_tab(config_tab, server_connection)

    root.mainloop()