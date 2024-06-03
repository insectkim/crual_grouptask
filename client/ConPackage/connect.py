import requests
import subprocess
import tkinter as tk
from threading import Thread

server_ip = None
is_server_connected = None

def initialize_server_variables(root):
    """
    서버 접속 변수를 초기화합니다.

    Parameters:
        root (Tk): Tkinter 루트 객체
    """
    global server_ip, is_server_connected
    server_ip = tk.StringVar(root, value="192.168.0.1")  # 기본 서버 IP 설정
    is_server_connected = tk.BooleanVar(root, value=False)

def send_request(endpoint, method='GET', data=None):
    """
    서버에 HTTP 요청을 보내는 함수입니다.

    Parameters:
        endpoint (str): 요청을 보낼 엔드포인트
        method (str): HTTP 메소드 (GET 또는 POST)
        data (dict): POST 요청 시 전송할 데이터

    Returns:
        dict: 서버 응답 데이터
    """
    url = f"http://{server_ip.get()}:5000/{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST' and data is not None:
            response = requests.post(url, json=data)
        else:
            raise ValueError("Invalid method or missing data for POST request")

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail", "message": response.reason}
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def update_server_status(lamp):
    """
    서버 접속 상태를 업데이트합니다.

    Parameters:
        lamp (Label): 서버 접속 상태를 나타내는 램프
    """
    def check_server():
        try:
            response = subprocess.run(['ping', '-c', '1', server_ip.get()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if response.returncode == 0:
                lamp.after(0, lambda: update_lamp(True))
            else:
                lamp.after(0, lambda: update_lamp(False))
        except Exception as e:
            lamp.after(0, lambda: update_lamp(False))

    def update_lamp(success):
        is_server_connected.set(success)
        lamp.config(bg="green" if success else "red")

    # 별도의 스레드에서 서버 상태를 체크합니다.
    Thread(target=check_server).start()

def attempt_connection(initial_root, server_ip_entry, status_label, show_main_ui_callback):
    """
    서버 접속을 시도하고 결과에 따라 UI를 업데이트합니다.

    Parameters:
        initial_root (Tk): 초기 입력 창의 루트 객체
        server_ip_entry (Entry): 서버 IP 입력 필드
        status_label (Label): 상태 표시 라벨
        show_main_ui_callback (function): 메인 UI를 표시하는 함수
    """
    server_ip.set(server_ip_entry.get())

    def check_server():
        try:
            response = subprocess.run(['ping', '-c', '1', server_ip.get()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if response.returncode == 0:
                initial_root.after(0, lambda: initial_root.destroy())  # 초기 입력 창 닫기
                initial_root.after(0, lambda: show_main_ui_callback())  # 메인 UI 표시
            else:
                initial_root.after(0, lambda: status_label.config(text="접속 실패, 다시 시도하세요.", foreground="red"))
        except Exception as e:
            initial_root.after(0, lambda: status_label.config(text=f"오류 발생: {e}", foreground="red"))

    # 비동기 서버 상태 체크
    Thread(target=check_server).start()
