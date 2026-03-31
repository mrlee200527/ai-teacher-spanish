"""微信机器人相关路由"""
from flask import Blueprint, request, jsonify, session
from database import get_db

wechat_bp = Blueprint('wechat', __name__)

@wechat_bp.route('/api/wechat/push/<int:student_id>', methods=['GET'])
def push_course(student_id):
    """推送课程链接给学生（微信机器人调用）"""
    # 检查是否已解锁新课程
    db = get_db()
    
    # 获取学生未完成的已解锁课程
    unlocked_course = db.execute(
        '''SELECT c.* FROM courses c
           WHERE c.is_unlocked = 1
           AND NOT EXISTS (
               SELECT 1 FROM progress p WHERE p.student_id = ? AND p.course_id = c.id AND p.is_completed = 1
           )
           ORDER BY c.week_number, c.day_number LIMIT 1''',
        (student_id,)
    ).fetchone()
    
    if unlocked_course:
        return jsonify({
            'success': True,
            'message': f'新课程已解锁：{unlocked_course["title"]}',
            'course_url': f'http://localhost:5000/course.html?id={unlocked_course["id"]}'
        })
    else:
        return jsonify({
            'success': False,
            'message': '暂无新课程'
        })

@wechat_bp.route('/api/wechat/completion-rate', methods=['GET'])
def get_completion_rate():
    """获取课程完成率（微信机器人调用）"""
    db = get_db()
    
    # 计算整体完成率
    result = db.execute('''
        SELECT
            (SELECT COUNT(*) FROM courses WHERE is_unlocked = 1) as total,
            (SELECT COUNT(*) FROM progress WHERE is_completed = 1) as completed
    ''').fetchone()
    
    total = result['total']
    completed = result['completed']
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return jsonify({
        'total_courses': total,
        'completed_courses': completed,
        'completion_rate': round(completion_rate, 2)
    })

@wechat_bp.route('/api/wechat/unlock-next', methods=['POST'])
def unlock_next_course():
    """解锁下一环节（微信机器人调用，当完成率达到60%时自动调用）"""
    # 这个接口已经在course.py的complete_course中自动实现了
    # 这里保留是为了让微信机器人可以手动触发
    db = get_db()
    
    # 计算完成率
    result = db.execute('''
        SELECT
            (SELECT COUNT(*) FROM courses WHERE is_unlocked = 1) as total,
            (SELECT COUNT(*) FROM progress WHERE is_completed = 1) as completed
    ''').fetchone()
    
    total = result['total']
    completed = result['completed']
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    if completion_rate >= 60:
        # 解锁第一个未解锁的课程
        next_course = db.execute(
            '''SELECT id FROM courses WHERE is_unlocked = 0 ORDER BY week_number, day_number LIMIT 1'''
        ).fetchone()
        
        if next_course:
            db.execute(
                'UPDATE courses SET is_unlocked = 1 WHERE id = ?',
                (next_course['id'],)
            )
            db.commit()
            
            return jsonify({
                'success': True,
                'message': f'已解锁新课程（ID: {next_course["id"]}）',
                'completion_rate': completion_rate
            })
        else:
            return jsonify({
                'success': False,
                'message': '所有课程已解锁完成'
            })
    else:
        return jsonify({
            'success': False,
            'message': f'完成率未达到60%（当前：{completion_rate:.2f}%）'
        })

@wechat_bp.route('/api/wechat/remind', methods=['GET'])
def remind_students():
    """提醒未完成的学生（微信机器人定时调用）"""
    db = get_db()
    
    # 获取所有学生
    students = db.execute('SELECT * FROM students').fetchall()
    
    # 获取需要提醒的学生（有已解锁但未完成的课程）
    students_to_remind = []
    for student in students:
        incomplete_count = db.execute('''
            SELECT COUNT(*)
            FROM courses c
            WHERE c.is_unlocked = 1
            AND NOT EXISTS (
                SELECT 1 FROM progress p WHERE p.student_id = ? AND p.course_id = c.id AND p.is_completed = 1
            )
        ''', (student['id'],)).fetchone()[0]
        
        if incomplete_count > 0:
            students_to_remind.append({
                'student_id': student['id'],
                'username': student['username'],
                'nickname': student['nickname'],
                'incomplete_courses': incomplete_count
            })
    
    return jsonify({
        'success': True,
        'count': len(students_to_remind),
        'students': students_to_remind
    })
