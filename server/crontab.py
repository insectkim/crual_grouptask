import subprocess

def get_crontab_list():
    try:
        result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, text=True)
        crontab_list = result.stdout.splitlines()
        # 주석 라인 제외
        filtered_list = [line for line in crontab_list if line.strip() and not line.strip().startswith('#')]
        return filtered_list
    except Exception as e:
        print(f"Failed to get crontab list: {e}")
        return []

def update_crontab(crontab_data):
    try:
        crontab_lines = []
        for job in crontab_data:
            # 각 job 항목을 올바른 크론탭 포맷으로 변환합니다.
            crontab_lines.append(job.strip())  # 불필요한 공백 및 탭 문자를 제거합니다.
        
        # crontab_lines 리스트의 각 항목을 새 줄로 연결합니다.
        crontab_content = "\n".join(crontab_lines) + "\n"  # 각 항목 끝에 새 줄을 추가하고, 마지막에도 새 줄을 추가
        
        # subprocess를 사용하여 crontab에 명령을 전달합니다.
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=crontab_content)
        
        # subprocess의 실행 결과를 확인합니다.
        if process.returncode == 0:
            print("Crontab update successful.")
        else:
            print("Crontab update failed.")
            
        return process.returncode == 0
    except Exception as e:
        print(f"Failed to update crontab: {e}")
        return False

if __name__ == "__main__":
    crontab_list = get_crontab_list()
    for line in crontab_list:
        print(line)
