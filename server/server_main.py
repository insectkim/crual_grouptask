from flask import Flask, request, jsonify
import crontab
import os
import subprocess

app = Flask(__name__)

@app.route('/crontab_list', methods=['GET'])
def crontab_list():
    """
    GET 엔드포인트: 현재 크론탭 리스트를 가져옵니다.
    
    Returns:
        json: 현재 사용자 크론탭 리스트
    """
    cron_jobs = crontab.get_crontab_list()
    return jsonify(cron_jobs)

@app.route('/update_crontab', methods=['POST'])
def update_crontab():
    """
    POST 엔드포인트: 크론탭 리스트를 업데이트합니다.
    
    Parameters:
        data (list): 새로운 크론탭 리스트
        
    Returns:
        json: 업데이트 결과
    """
    data = request.json
    success = crontab.update_crontab(data)
    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'}), 500

@app.route('/update_weather', methods=['GET'])
def update_weather():
    """
    GET 엔드포인트: 날씨 정보를 업데이트합니다.
    
    Parameters:
        value (int): 날씨 값 (예: 0 또는 1)
        
    Returns:
        json: 업데이트 결과
    """
    value = request.args.get('value', 0, type=int)
    
    # config 디렉토리와 wea_flag.dat 파일 경로 설정
    config_dir = os.path.join(os.getcwd(), 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'wea_flag.dat')
    
    # wea_flag 값을 파일에 기록
    command = f"echo {value} > {config_path}"
    subprocess.run(command, shell=True, check=True)
    
    return jsonify({"status": "success"}), 200

# 이 블록은 스크립트가 직접 실행될 때만 서버를 시작합니다.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
