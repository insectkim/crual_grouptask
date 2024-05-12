import pygame
import time

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load(r"C:\Users\pofwe\Music\alarm.mp3")  # 원시 문자열을 사용하는 방법
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(10)  # 10초마다 체크

if __name__ == "__main__":
    play_music()