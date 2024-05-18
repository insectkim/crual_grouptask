import subprocess

class CrontabManager:
    @staticmethod
    def get_crontab_list():
        """
        현재 사용자 크론탭 리스트를 가져옵니다.

        Returns:
            list: 크론탭 항목 리스트
        """
        result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')
        cron_jobs = [line.split('#')[0].strip() for line in lines if line.strip()]
        return cron_jobs

    @staticmethod
    def update_crontab(crontab_data):
        """
        새로운 크론탭 리스트로 업데이트합니다.

        Parameters:
            crontab_data (list): 크론탭 형식의 문자열 리스트

        Returns:
            bool: 성공 여부
        """
        try:
            new_cron = '\n'.join(crontab_data) + '\n'
            process = subprocess.Popen(['crontab'], stdin=subprocess.PIPE)
            process.communicate(input=new_cron.encode())
            return process.returncode == 0
        except Exception as e:
            print(f"Error: {e}")
            return False
