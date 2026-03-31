"""诊断登录问题"""
import os
import sys
import sqlite3
from config import Config

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("AI Teacher 登录问题诊断")
print("=" * 60)

# 1. 检查配置
print("\n[1] 检查配置...")
print(f"数据库路径: {Config.DATABASE_PATH}")
print(f"数据库目录: {os.path.dirname(Config.DATABASE_PATH)}")
print(f"Session目录: {Config.SESSION_FILE_DIR}")

# 2. 检查数据库
print("\n[2] 检查数据库...")
if os.path.exists(Config.DATABASE_PATH):
    print(f"[OK] 数据库文件存在")
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"[OK] 数据表: {[t[0] for t in tables]}")
        conn.close()
    except Exception as e:
        print(f"[ERROR] 数据库连接失败: {e}")
else:
    print(f"[ERROR] 数据库文件不存在: {Config.DATABASE_PATH}")
    print(f"需要启动服务器以初始化数据库")

# 3. 检查Session目录
print("\n[3] 检查Session目录...")
if os.path.exists(Config.SESSION_FILE_DIR):
    print(f"[OK] Session目录存在")
    files = os.listdir(Config.SESSION_FILE_DIR)
    print(f"Session文件数: {len(files)}")
else:
    print(f"[ERROR] Session目录不存在: {Config.SESSION_FILE_DIR}")

# 4. 检查端口占用
print("\n[4] 检查端口占用...")
try:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(('localhost', 5000))
    s.close()
    if result == 0:
        print("[WARNING] 端口5000已被占用")
    else:
        print("[OK] 端口5000可用")
except Exception as e:
    print(f"[ERROR] 端口检查失败: {e}")

# 5. 测试导入
print("\n[5] 测试模块导入...")
try:
    from flask import Flask
    print("[OK] Flask导入成功")
except ImportError as e:
    print(f"[ERROR] Flask导入失败: {e}")

try:
    from flask_cors import CORS
    print("[OK] Flask-CORS导入成功")
except ImportError as e:
    print(f"[ERROR] Flask-CORS导入失败: {e}")

try:
    from flask_session import Session
    print("[OK] Flask-Session导入成功")
except ImportError as e:
    print(f"[ERROR] Flask-Session导入失败: {e}")

try:
    from llm.xiaomi_client import XiaoMiLLMClient
    print("[OK] XiaoMiLLMClient导入成功")
except ImportError as e:
    print(f"[ERROR] XiaoMiLLMClient导入失败: {e}")

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
print("\n建议:")
print("1. 如果数据库不存在，请先启动服务器初始化数据库")
print("2. 如果端口被占用，请关闭占用进程或更换端口")
print("3. 如果模块导入失败，请运行: pip install -r requirements.txt")
