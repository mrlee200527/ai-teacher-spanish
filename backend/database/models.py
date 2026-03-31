"""数据模型定义"""
from datetime import datetime

class Student:
    def __init__(self, id=None, username=None, nickname=None, created_at=None, last_login=None):
        self.id = id
        self.username = username
        self.nickname = nickname
        self.created_at = created_at
        self.last_login = last_login
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

class Course:
    def __init__(self, id=None, title=None, description=None, week_number=None, 
                 day_number=None, content=None, is_unlocked=False, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.week_number = week_number
        self.day_number = day_number
        self.content = content
        self.is_unlocked = is_unlocked
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'week_number': self.week_number,
            'day_number': self.day_number,
            'content': self.content,
            'is_unlocked': self.is_unlocked,
            'created_at': self.created_at
        }

class Exercise:
    def __init__(self, id=None, course_id=None, question_type=None, question_text=None,
                 options=None, correct_answer=None, explanation=None, created_at=None):
        self.id = id
        self.course_id = course_id
        self.question_type = question_type  # 'choice', 'true_false', 'fill', 'writing'
        self.question_text = question_text
        self.options = options  # JSON字符串
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'question_type': self.question_type,
            'question_text': self.question_text,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'created_at': self.created_at
        }

class Submission:
    def __init__(self, id=None, student_id=None, exercise_id=None, student_answer=None,
                 is_correct=None, feedback=None, created_at=None):
        self.id = id
        self.student_id = student_id
        self.exercise_id = exercise_id
        self.student_answer = student_answer
        self.is_correct = is_correct
        self.feedback = feedback
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exercise_id': self.exercise_id,
            'student_answer': self.student_answer,
            'is_correct': self.is_correct,
            'feedback': self.feedback,
            'created_at': self.created_at
        }

class Progress:
    def __init__(self, id=None, student_id=None, course_id=None, is_completed=False,
                 completed_at=None, created_at=None):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.is_completed = is_completed
        self.completed_at = completed_at
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at,
            'created_at': self.created_at
        }
