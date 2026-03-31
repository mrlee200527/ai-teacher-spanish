"""测试登录API"""
import requests
import json

def test_api():
    """测试后端API"""
    print("测试后端API...")
    print("=" * 60)

    # 测试根路径
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"[根路径] 状态码: {response.status_code}")
        print(f"[根路径] Content-Type: {response.headers.get('Content-Type')}")
        print(f"[根路径] 内容长度: {len(response.text)}")
    except Exception as e:
        print(f"[根路径] 错误: {e}")

    print()

    # 测试登录API
    try:
        response = requests.post(
            'http://localhost:5000/api/login',
            json={'username': 'test_user', 'api_key': 'test_key_123'},
            timeout=5
        )
        print(f"[登录API] 状态码: {response.status_code}")
        print(f"[登录API] Content-Type: {response.headers.get('Content-Type')}")
        print(f"[登录API] 响应内容:")
        print(response.text[:500])
    except Exception as e:
        print(f"[登录API] 错误: {e}")

    print("=" * 60)

if __name__ == '__main__':
    test_api()
