from tkinter import Tk, ttk
from UIPackage.test import initialize_test_tab
from UIPackage.alarm import initialize_alarm_tab
from UIPackage.status import initialize_status_tab
from UIPackage.config import initialize_config_tab

# 메인 윈도우 생성
root = Tk()
root.title("스마트 창문 시스템")

# 탭 컨트롤 생성, 탭이 있는 창을 만듬
tabControl = ttk.Notebook(root)

# 각 섹션별 탭 생성
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

# 탭 추가
tabControl.add(tab1, text='상태정보')
tabControl.add(tab2, text='알람관리')
tabControl.add(tab3, text='수동실행')
tabControl.add(tab4, text='설정관리')
tabControl.pack(expand=1, fill="both")

initialize_status_tab(tab1)
initialize_alarm_tab(tab2)
initialize_test_tab(tab3)
initialize_config_tab(tab4)

root.mainloop()
