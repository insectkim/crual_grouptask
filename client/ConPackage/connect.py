import requests
import subprocess
import tkinter as tk
import platform

class ServerConnection:
    def __init__(self):
        if not tk._default_root:
            root = tk.Tk()
            root.withdraw()
        
        self.server_ip = tk.StringVar(value="192.168.120.133")
        self.server_ip_with_port = self.server_ip.get() + ":5000"
        self.is_connected = tk.BooleanVar(value=False)

    def update_ip_with_port(self):
        self.server_ip_with_port = self.server_ip.get() + ":5000"

    def send_request(self, endpoint, method='GET', data=None):
        self.update_ip_with_port()
        url = f"http://{self.server_ip_with_port}/{endpoint}"
        print(f"Request URL: {url}")  # URL 확인용 출력 추가
        print(f"Request Data: {data}")  # 데이터 확인용 출력 추가

        try:
            if method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=10)  # 타임아웃 설정 추가
            else:
                response = requests.get(url, timeout=10)  # 타임아웃 설정 추가
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def check_server_connection(self, ip):
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
