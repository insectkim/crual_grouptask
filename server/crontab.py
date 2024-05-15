import subprocess

def get_crontab_list():
    try:
        result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')
        cron_jobs = [line.split('#')[0].strip() for line in lines if line.strip() and not line.startswith('#')]
        return cron_jobs
    except Exception as e:
        print(f"Error fetching crontab list: {e}")
        return []

def update_crontab(cron_jobs):
    try:
        crontab_content = '\n'.join(cron_jobs) + '\n'
        process = subprocess.Popen(['crontab'], stdin=subprocess.PIPE)
        process.communicate(input=crontab_content.encode('utf-8'))
        return process.returncode == 0
    except Exception as e:
        print(f"Error updating crontab: {e}")
        return False
