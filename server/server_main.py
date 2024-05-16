from flask import Flask, request, jsonify
import crontab
import os
import subprocess

app = Flask(__name__)

@app.route('/crontab_list', methods=['GET'])
def crontab_list():
    cron_jobs = crontab.get_crontab_list()
    return jsonify(cron_jobs)

@app.route('/update_crontab', methods=['POST'])
def update_crontab():
    data = request.json
    success = crontab.update_crontab(data)
    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'}), 500

from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/update_weather', methods=['GET'])
def update_weather():
    value = request.args.get('value', 0, type=int)
    
    # Classify the value as True (1) or False (0)
    # Replace this logic with your actual classification criteria
    wea_flag = 1 if value > 0 else 0
    
    # Path to the config directory and wea_flag.dat file
    config_dir = os.path.join(os.getcwd(), 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'wea_flag.dat')
    
    # Use subprocess to execute the command
    command = f"echo {wea_flag} > {config_path}"
    subprocess.run(command, shell=True, check=True)
    
    return jsonify({"status": "success"}), 200

# This block ensures that the server starts only if the script is executed directly
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
