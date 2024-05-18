import requests

def send_request(endpoint, method='GET', data=None):
    """
    서버에 HTTP 요청을 보내는 함수입니다.

    Parameters:
        endpoint (str): 요청을 보낼 엔드포인트
        method (str): HTTP 메소드 (GET 또는 POST)
        data (dict): POST 요청 시 전송할 데이터

    Returns:
        dict: 서버 응답 데이터
    """
    url = f"http://192.168.200.113:5000/{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST' and data is not None:
            response = requests.post(url, json=data)
        else:
            raise ValueError("Invalid method or missing data for POST request")

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail", "message": response.reason}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
