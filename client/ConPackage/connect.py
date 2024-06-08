import requests
import subprocess
import tkinter as tk
import platform

class ServerConnection:
    def __init__(self):
        # Tkinter의 기본 루트 윈도우 생성
        if not tk._default_root:
            root = tk.Tk()
            root.withdraw()  # 루트 윈도우 숨기기
        
        self.server_ip = tk.StringVar(value="192.168.0.1")
        self.is_connected = tk.BooleanVar(value=False)

    def send_request(self, endpoint, method='GET', data=None):
        url = f"http://{self.server_ip.get()}/{endpoint}"
        try:
            if method == 'POST':
                response = requests.post(url, json=data)
            else:
                response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def check_server_connection(self, ip):
        # OS 확인 및 적절한 ping 명령 옵션 선택
        ping_option = '-n' if platform.system().lower() == 'windows' else '-c'
        try:
            response = subprocess.run(['ping', ping_option, '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if response.returncode == 0:
                self.is_connected.set(True)
                return True
            else:
                self.is_connected.set(False)
                return False
        except Exception as e:
            print(f"Error checking server connection: {e}")
            self.is_connected.set(False)
            return False
