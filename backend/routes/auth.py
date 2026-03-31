"""认证相关路由"""
from flask import Blueprint, request, jsonify, session
from database import get_db
from llm.xiaomi_client import XiaoMiLLMClient

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """学生登录"""
    data = request.json
    username = data.get('username')
    api_key = data.get('api_key')  # 小米大模型API密钥
    
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    if not api_key:
        return jsonify({'error': 'API密钥不能为空'}), 400
    
    db = get_db()
    
    # 查找或创建学生
    student = db.execute(
        'SELECT * FROM students WHERE username = ?',
        (username,)
    ).fetchone()
    
    if student:
        # 更新最后登录时间
        db.execute(
            'UPDATE students SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
            (student['id'],)
        )
        db.commit()
        student_id = student['id']
    else:
        # 创建新学生
        cursor = db.execute(
            'INSERT INTO students (username, nickname) VALUES (?, ?)',
            (username, f'学员{username}')
        )
        db.commit()
        student_id = cursor.lastrowid
    
    # 设置Session
    session['user_id'] = student_id
    session['username'] = username
    
    # 保存API密钥到Session（不存数据库）
    llm_client = XiaoMiLLMClient()
    llm_client.set_api_key(api_key)
    
    return jsonify({
        'success': True,
        'user_id': student_id,
        'username': username
    })

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """学生登出"""
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/api/check-login', methods=['GET'])
def check_login():
    """检查登录状态"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username')
        })
    else:
        return jsonify({'logged_in': False})
