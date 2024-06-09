import tkinter as tk
from tkinter import ttk
from ConPackage.connect import get_flags

def initialize_config_tab(tab):
    """
    설정관리 탭을 초기화합니다.

    Parameters:
        tab (tk.Frame): 설정관리 탭의 프레임
    """
    ttk.Label(tab, text="기상 플래그").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(tab, text="먼지 플래그").grid(column=0, row=1, padx=10, pady=10)
    ttk.Label(tab, text="모터 위치 : ").grid(column=0, row=2, padx=10, pady=10)

    wea_flag_var = tk.StringVar()
    dust_flag_var = tk.StringVar()

    wea_flag_entry = ttk.Entry(tab, textvariable=wea_flag_var, state='readonly')
    wea_flag_entry.grid(column=1, row=0, padx=10, pady=10)

    dust_flag_entry = ttk.Entry(tab, textvariable=dust_flag_var, state='readonly')
    dust_flag_entry.grid(column=1, row=1, padx=10, pady=10)

    def update_flags():
        wea_flag, dust_flag = get_flags()
        if wea_flag is not None and dust_flag is not None:
            # Temporarily make the entry widget writable
            wea_flag_entry.configure(state='normal')
            dust_flag_entry.configure(state='normal')
            
            wea_flag_entry.delete(0, 'end')
            wea_flag_entry.insert(0, wea_flag)
            dust_flag_entry.delete(0, 'end')
            dust_flag_entry.insert(0, dust_flag)
            
            # Revert back to readonly
            wea_flag_entry.configure(state='readonly')
            dust_flag_entry.configure(state='readonly')
        else:
            wea_flag_var.set("Error")
            dust_flag_var.set("Error")

            


    update_flags_button = ttk.Button(tab, text="플래그 업데이트", command=update_flags)
    update_flags_button.grid(column=0, row=3, padx=10, pady=10, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Config Tab Example")
    
    tab_control = ttk.Notebook(root)
    config_tab = ttk.Frame(tab_control)
    tab_control.add(config_tab, text='설정관리')
    tab_control.pack(expand=1, fill='both')

    initialize_config_tab(config_tab)

    root.mainloop()
