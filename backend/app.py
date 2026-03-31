"""Flask应用主入口"""
from flask import Flask, session
from flask_cors import CORS
from flask_session import Session
from config import Config
from database import init_db, close_db
from routes import auth, course, wechat

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 启用CORS（跨域支持）
    CORS(app, resources={
        r"/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 初始化Session
    Session(app)
    
    # 初始化数据库
    with app.app_context():
        init_db()
    
    # 注册路由
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(course.course_bp)
    app.register_blueprint(wechat.wechat_bp)
    
    # 注册数据库关闭函数
    app.teardown_appcontext(close_db)
    
    # 静态文件服务
    @app.route('/')
    def index():
        """首页"""
        return app.send_static_file('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print('=' * 50)
    print('AI Teacher 学习系统启动成功！')
    print('=' * 50)
    print(f'访问地址: http://localhost:5000')
    print('按 Ctrl+C 停止服务器')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
