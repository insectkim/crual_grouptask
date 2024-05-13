from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/crontab_list')
def crontab_list():
    result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split('\n')
    cron_jobs = [line.split('#')[0].strip() for line in lines if '#' in line and line.split('#')[0].strip() != '']
    return jsonify(cron_jobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
