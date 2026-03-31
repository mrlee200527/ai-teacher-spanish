import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置"""
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session配置（使用client-side cookie）
    SESSION_TYPE = 'null'  # 使用Flask默认的client-side session
    SESSION_COOKIE_NAME = 'aiteacher_session'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 7200  # 2小时

    # 如果需要server-side session，使用Redis
    # SESSION_TYPE = 'redis'  # 需要安装Redis
    
    # 数据库配置
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'aiteacher.db')
    
    # 小米大模型API配置（用户登录后设置，不在环境变量中）
    XIAOMI_API_KEY = None  # 存储在Session中
    XIAOMI_API_URL = 'https://api.xiaomi.com/v1/chat/completions'
    
    # 跨域配置
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
