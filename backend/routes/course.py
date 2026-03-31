"""课程相关路由"""
from flask import Blueprint, request, jsonify, session
from database import get_db
from llm.xiaomi_client import XiaoMiLLMClient
import json

course_bp = Blueprint('course', __name__)

@course_bp.route('/api/courses', methods=['GET'])
def get_courses():
    """获取课程列表"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    db = get_db()
    
    # 获取所有已解锁的课程
    courses = db.execute(
        'SELECT * FROM courses WHERE is_unlocked = 1 ORDER BY week_number, day_number'
    ).fetchall()
    
    course_list = []
    for course in courses:
        # 检查学生是否已完成该课程
        progress = db.execute(
            'SELECT * FROM progress WHERE student_id = ? AND course_id = ?',
            (session['user_id'], course['id'])
        ).fetchone()
        
        course_dict = dict(course)
        course_dict['is_completed'] = progress['is_completed'] if progress else False
        course_list.append(course_dict)
    
    return jsonify({'courses': course_list})

@course_bp.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    """获取课程详情"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    db = get_db()
    
    # 获取课程内容
    course = db.execute(
        'SELECT * FROM courses WHERE id = ?',
        (course_id,)
    ).fetchone()
    
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    if not course['is_unlocked']:
        return jsonify({'error': '课程未解锁'}), 403
    
    # 获取课程的练习题
    exercises = db.execute(
        'SELECT * FROM exercises WHERE course_id = ?',
        (course_id,)
    ).fetchall()
    
    exercise_list = []
    for ex in exercises:
        ex_dict = dict(ex)
        if ex_dict['options']:
            ex_dict['options'] = json.loads(ex_dict['options'])
        # 隐藏正确答案
        ex_dict['correct_answer'] = None
        exercise_list.append(ex_dict)
    
    # 检查学习进度
    progress = db.execute(
        'SELECT * FROM progress WHERE student_id = ? AND course_id = ?',
        (session['user_id'], course_id)
    ).fetchone()
    
    return jsonify({
        'course': dict(course),
        'exercises': exercise_list,
        'progress': dict(progress) if progress else None
    })

@course_bp.route('/api/courses/generate', methods=['POST'])
def generate_course():
    """生成课程内容（教师功能）"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    data = request.json
    week_number = data.get('week_number')
    day_number = data.get('day_number')
    title = data.get('title')
    topic = data.get('topic', '自我介绍')
    
    if not all([week_number, day_number, title]):
        return jsonify({'error': '参数不完整'}), 400
    
    try:
        # 使用LLM生成课文内容
        llm_client = XiaoMiLLMClient()
        content = llm_client.generate_content(topic, level='A1')
        
        # 保存到数据库
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO courses (title, description, week_number, day_number, content, is_unlocked)
               VALUES (?, ?, ?, ?, ?, 1)''',
            (title, f'{topic}主题课文', week_number, day_number, content)
        )
        db.commit()
        course_id = cursor.lastrowid
        
        # 生成练习题
        exercise_types = ['choice', 'choice', 'true_false']  # 2道选择+1道判断
        exercises = []
        for ex_type in exercise_types:
            exercise_content = llm_client.generate_exercise(content, ex_type)
            # 尝试解析JSON（实际使用时需要更好的错误处理）
            try:
                exercise = json.loads(exercise_content)
                cursor = db.execute(
                    '''INSERT INTO exercises (course_id, question_type, question_text, options, correct_answer, explanation)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (course_id, ex_type, exercise['question'],
                     json.dumps(exercise.get('options', [])),
                     exercise['correct_answer'], exercise['explanation'])
                )
                db.commit()
                exercises.append(cursor.lastrowid)
            except json.JSONDecodeError:
                continue
        
        return jsonify({
            'success': True,
            'course_id': course_id,
            'exercise_count': len(exercises)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@course_bp.route('/api/courses/<int:course_id>/exercises/<int:exercise_id>/submit', methods=['POST'])
def submit_exercise(course_id, exercise_id):
    """提交练习答案"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    data = request.json
    student_answer = data.get('answer')
    
    if not student_answer:
        return jsonify({'error': '答案不能为空'}), 400
    
    db = get_db()
    
    # 获取练习题
    exercise = db.execute(
        'SELECT * FROM exercises WHERE id = ?',
        (exercise_id,)
    ).fetchone()
    
    if not exercise:
        return jsonify({'error': '练习题不存在'}), 404
    
    # 判断答案是否正确
    is_correct = (student_answer.lower() == exercise['correct_answer'].lower())
    feedback = exercise['explanation']
    
    # 保存提交记录
    db.execute(
        '''INSERT INTO submissions (student_id, exercise_id, student_answer, is_correct, feedback)
           VALUES (?, ?, ?, ?, ?)''',
        (session['user_id'], exercise_id, student_answer, is_correct, feedback)
    )
    
    # 如果回答错误，添加到错题本
    if not is_correct:
        db.execute(
            '''INSERT INTO wrong_answers (student_id, exercise_id, wrong_answer, correct_answer, feedback)
               VALUES (?, ?, ?, ?, ?)''',
            (session['user_id'], exercise_id, student_answer, exercise['correct_answer'], feedback)
        )
    
    db.commit()
    
    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'feedback': feedback,
        'correct_answer': exercise['correct_answer']
    })

@course_bp.route('/api/courses/<int:course_id>/complete', methods=['POST'])
def complete_course(course_id):
    """标记课程为已完成"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    db = get_db()
    
    # 检查是否所有练习都已完成
    exercise_count = db.execute(
        'SELECT COUNT(*) FROM exercises WHERE course_id = ?',
        (course_id,)
    ).fetchone()[0]
    
    submission_count = db.execute(
        '''SELECT COUNT(DISTINCT exercise_id) FROM submissions
           WHERE student_id = ? AND exercise_id IN (
               SELECT id FROM exercises WHERE course_id = ?
           )''',
        (session['user_id'], course_id)
    ).fetchone()[0]
    
    if submission_count < exercise_count:
        return jsonify({'error': '请完成所有练习后再标记完成'}), 400
    
    # 标记课程完成
    db.execute(
        '''INSERT OR REPLACE INTO progress (student_id, course_id, is_completed, completed_at)
           VALUES (?, ?, 1, CURRENT_TIMESTAMP)''',
        (session['user_id'], course_id)
    )
    db.commit()
    
    # 检查是否达到60%完成率，如果是则解锁下一环节
    check_completion_rate(session['user_id'])
    
    return jsonify({'success': True})

@course_bp.route('/api/progress', methods=['GET'])
def get_progress():
    """获取学习进度"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    db = get_db()
    
    # 获取总体进度
    total_courses = db.execute(
        'SELECT COUNT(*) FROM courses WHERE is_unlocked = 1'
    ).fetchone()[0]
    
    completed_courses = db.execute(
        'SELECT COUNT(*) FROM progress WHERE student_id = ? AND is_completed = 1',
        (session['user_id'],)
    ).fetchone()[0]
    
    completion_rate = (completed_courses / total_courses * 100) if total_courses > 0 else 0
    
    # 获取错题本
    wrong_answers = db.execute(
        '''SELECT wa.*, e.question_text, e.question_type
           FROM wrong_answers wa
           JOIN exercises e ON wa.exercise_id = e.id
           WHERE wa.student_id = ?
           ORDER BY wa.created_at DESC LIMIT 20''',
        (session['user_id'],)
    ).fetchall()
    
    wrong_list = []
    for wa in wrong_answers:
        wrong_dict = dict(wa)
        wrong_dict['question_text'] = wa['question_text']
        wrong_dict['question_type'] = wa['question_type']
        wrong_list.append(wrong_dict)
    
    return jsonify({
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'completion_rate': round(completion_rate, 2),
        'wrong_answers': wrong_list
    })

def check_completion_rate(student_id):
    """检查完成率并解锁下一环节"""
    db = get_db()
    
    # 获取所有已解锁的课程
    all_courses = db.execute(
        'SELECT id FROM courses WHERE is_unlocked = 1'
    ).fetchall()
    
    # 获取该学生已完成的课程
    completed_courses = db.execute(
        'SELECT course_id FROM progress WHERE student_id = ? AND is_completed = 1',
        (student_id,)
    ).fetchall()
    
    if not all_courses:
        return
    
    completion_rate = len(completed_courses) / len(all_courses)
    
    # 如果达到60%，解锁下一环节（这里简化处理，实际可能需要更复杂的逻辑）
    if completion_rate >= 0.6:
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
