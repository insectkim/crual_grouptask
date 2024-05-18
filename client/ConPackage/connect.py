import requests

SERVER_URL = 'http://192.168.200.113:5000'

def send_request(endpoint, method='GET', data=None):
    """
    서버에 HTTP 요청을 보내고 응답을 반환합니다.

    Parameters:
        endpoint (str): 서버의 엔드포인트 (예: 'crontab_list')
        method (str): HTTP 메소드 ('GET' 또는 'POST')
        data (dict, optional): POST 요청에 사용할 데이터

    Returns:
        dict: 서버 응답 데이터
    """
    url = f"{SERVER_URL}/{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "fail"}
