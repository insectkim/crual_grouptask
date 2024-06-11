import requests
import tkinter as tk
import platform
import subprocess

class ServerConnection:
    def __init__(self):
        if not tk._default_root:
            root = tk.Tk()
            root.withdraw()
        
        self.server_ip = tk.StringVar(value="192.168.120.113")
        self.server_port = "5000"
        self.is_connected = tk.BooleanVar(value=False)

    def get_server_ip_with_port(self):
        return f"{self.server_ip.get()}:{self.server_port}"

    def send_request(self, endpoint, server_ip_with_port=None, method='GET', data=None, timeout=30):
        if server_ip_with_port is None:
            server_ip_with_port = self.get_server_ip_with_port()
        url = f"http://{server_ip_with_port}/{endpoint}"
        print(f"Request URL: {url}")  # URL 확인용 출력 추가
        print(f"Request Data: {data}")  # 데이터 확인용 출력 추가

        try:
            if method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=timeout)  # 타임아웃 설정 추가
            else:
                response = requests.get(url, timeout=timeout)  # 타임아웃 설정 추가
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None


    def check_server_connection(self, ip):
        # Ping test
        ping_option = '-n' if platform.system().lower() == 'windows' else '-c'
        ping_result = subprocess.run(['ping', ping_option, '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
        
        # HTTP test
        http_result = self.send_request('test_connection')
        
        # Determine and return the connection status
        if ping_result and http_result:
            return "green"  # Both tests passed
        elif ping_result and not http_result:
            return "orange"  # Ping passed, HTTP failed
        else:
            return "red"  # Both tests failed
