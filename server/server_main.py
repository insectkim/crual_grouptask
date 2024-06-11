from flask import Flask, request, jsonify
import os
import subprocess
import sys
import requests
import logging
import crontab
sys.path.append(os.path.dirname(__file__))
current_dir = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/crontab_list', methods=['GET'])
def crontab_list():
    cron_jobs = crontab.get_crontab_list()
    logger.info(f"Returning crontab list: {cron_jobs}")
    return jsonify(cron_jobs), 200

@app.route('/update_crontab', methods=['POST'])
def update_crontab():
    data = request.json
    try:
        crontab_data = data['crontab']
        # 탭 문자를 줄 바꿈 문자로 변환하여 저장
        crontab_data = [job.replace('\t', '') for job in crontab_data]
        success = crontab.update_crontab(crontab_data)
        if success:
            logger.info(f"Crontab updated successfully with data: {data}")
            return jsonify({'status': 'success'}), 200
        else:
            logger.error(f"Failed to update crontab with data: {data}")
            return jsonify({'status': 'fail'}), 500
    except Exception as e:
        logger.error(f"Failed to update crontab: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/play_music', methods=['GET'])
def play_music():
    try:
        command = "cvlc /home/insectkim/program/alarm.mp3 --play-and-exit"
        subprocess.Popen(command, shell=True)
        logger.info("Playing music")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Failed to play music: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/stop_music', methods=['GET'])
def stop_music():
    try:
        command = "pkill vlc"
        subprocess.Popen(command, shell=True)
        logger.info("Stopping music")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Failed to stop music: {e}")
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/update_weather', methods=['GET'])
def update_weather():
    value = request.args.get('value', 0, type=int)
    wea_flag = 1 if value > 0 else 0
    config_dir = os.path.join(os.getcwd(), 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'wea_flag.dat')
    command = f"echo {wea_flag} > {config_path}"
    subprocess.run(command, shell=True, check=True)
    logger.info(f"Weather updated with value: {value}")
    return jsonify({"status": "success"}), 200

@app.route('/check_dust_data', methods=['GET'])
def check_dust_data():
    value = request.args.get('value', 0, type=int)
    config_dir = os.path.join(os.getcwd(), 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'dust_flag.dat')
    command = f"echo {value} > {config_path}"
    subprocess.run(command, shell=True, check=True)
    logger.info(f"Dust data updated with value: {value}")
        
    try:
        response = requests.get('http://localhost:5000/close_window')
        if response.status_code == 200:
            logger.info("Window closed successfully after dust data update.")
            return jsonify({"status": "success", "window": "closed"}), 200
        else:
            logger.error(f"Failed to close window: {response.status_code}")
            return jsonify({"status": "failed", "error": f"Failed to close window: {response.status_code}"}), 500
    except requests.RequestException as e:
        logger.error(f"Error closing window after dust data update: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500
    return jsonify({"status": "success"}), 200

@app.route('/get_flags')
def get_flags():
    try:
        config_path = os.path.join(current_dir, 'config')
        with open(os.path.join(config_path, 'wea_flag.dat'), 'r') as file:
            wea_flag = int(file.read().strip())
        with open(os.path.join(config_path, 'dust_flag.dat'), 'r') as file:
            dust_flag = int(file.read().strip())
        with open(os.path.join(config_path, 'window_stat.dat'), 'r') as file:
            window_state = file.read().strip()
        return jsonify({
            'wea_flag': wea_flag,
            'dust_flag': dust_flag,
            'window_state': window_state
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_connection', methods=['GET'])
def test_connection():
    return jsonify({'status': 'success'}), 200

@app.route('/open_window')
def open_window():
    try:
        subprocess.run(['python', os.path.join(current_dir, 'open_window.py'), 'test'], check=True)
        return '', 200
    except subprocess.CalledProcessError as e:
        return f"Failed to open window: {e}", 500
    
@app.route('/close_window')
def close_window():
    try:
        subprocess.run(['python', os.path.join(current_dir, 'close_window.py'), 'test'], check=True)
        return '', 200
    except subprocess.CalledProcessError as e:
        return f"Failed to close window: {e}", 500 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
