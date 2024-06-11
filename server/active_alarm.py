import requests
import subprocess
import sys
import os
import threading

def play_music():
    url = "http://localhost:5000/play_music"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("play_music request sent successfully.")
        else:
            print(f"Failed to send play_music request. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending play_music request: {e}")

def open_window():
    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'open_window.py')
    try:
        subprocess.run(['python', script_path, 'window'], check=True)
        print("open_window script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing open_window script: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'window':
        threading.Thread(target=play_music).start()
        threading.Thread(target=open_window).start()
    else:
        threading.Thread(target=play_music).start()
