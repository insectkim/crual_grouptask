import tkinter as tk
from tkinter import ttk #tkinter 모듈 중 ttk 모듈도 추가로 불러옴

# 메인 윈도우 생성
root = tk.Tk()
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

# 상태 탭 내용
ttk.Label(tab1, text="PM 2.5 센서정보").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(tab1, text="창문 상태").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(tab1, text="모터 통신 상태 : ").grid(column=0, row=2, padx=10, pady=10)

# 일정관리 탭 내용
review_frame = ttk.LabelFrame(tab2, text="알람 리스트")
review_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

# 입력 세트를 담을 프레임
entries_frame = ttk.Frame(review_frame)
entries_frame.pack(fill='x', padx=5, pady=5)

# 입력 세트 관리를 위한 리스트
entries_list = []

def add_entry():
    frame = ttk.Frame(entries_frame)
    frame.pack(fill='x', padx=5, pady=5)

    # 시간 및 분 입력
    hour_entry = ttk.Entry(frame, width=5)
    hour_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="시").pack(side='left')

    minute_entry = ttk.Entry(frame, width=5)
    minute_entry.pack(side='left', padx=5)
    ttk.Label(frame, text="분").pack(side='left')

    # 요일 라벨과 체크박스
    days_frame = ttk.Frame(frame)
    days_frame.pack(side='left', fill='x', expand=True, padx=10)
    
    days = ['월', '화', '수', '목', '금', '토', '일']
    day_vars = {day: tk.BooleanVar() for day in days}
    
    labels_frame = ttk.Frame(days_frame)
    labels_frame.pack(side='top', fill='x')
    checkboxes_frame = ttk.Frame(days_frame)
    checkboxes_frame.pack(side='top', fill='x')
    
    for day in days:
        ttk.Label(labels_frame, text=day).pack(side='left', padx=4)
    
    for day in days:
        ttk.Checkbutton(checkboxes_frame, variable=day_vars[day], onvalue=True, offvalue=False).pack(side='left', padx=1)

    # 창문 열기 체크박스
    window_open_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(frame, text="창문 열기", variable=window_open_var, onvalue=True, offvalue=False).pack(side='left', padx=10)

    # 삭제 버튼
    def remove_entry():
        frame.pack_forget()
        frame.destroy()
        entries_list.remove(frame)

    remove_button = ttk.Button(frame, text="삭제", command=remove_entry)
    remove_button.pack(side='right')

    entries_list.append(frame)

# 추가 버튼
add_button = ttk.Button(review_frame, text="추가", command=add_entry)
add_button.pack(fill='x', padx=5, pady=5)

# 최초 한 번 입력 세트 추가
add_entry()

# 시뮬레이션 탭 내용
ttk.Button(tab3, text="창문 열기").grid(column=0, row=0, padx=10, pady=10)
ttk.Button(tab3, text="창문 닫기").grid(column=0, row=1, padx=10, pady=10)
ttk.Button(tab3, text="노래 재생").grid(column=0, row=2, padx=10, pady=10)
# 설정관리 탭 내용
ttk.Label(tab4, text="기상 플래그").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(tab4, text="먼지 플래그").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(tab4, text="모터 위치 : ").grid(column=0, row=2, padx=10, pady=10)
# 메인 루프
root.mainloop()
