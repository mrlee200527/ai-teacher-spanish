"""测试后端API"""
import requests

def test_login():
    """测试登录API"""
    url = 'http://localhost:5000/api/login'
    data = {
        'username': 'test_user',
        'api_key': 'test_key_123'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text[:500]}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == '__main__':
    test_login()
