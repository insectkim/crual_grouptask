from flask import Flask, request, jsonify
import crontab

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
