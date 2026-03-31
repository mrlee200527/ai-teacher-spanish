"""生成示例课程"""
import sqlite3
import json
import sys
from datetime import datetime

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_sample_course():
    """创建示例课程"""
    db_path = '../data/aiteacher.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建课程
    cursor.execute('''
        INSERT INTO courses (title, description, week_number, day_number, content, is_unlocked)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        '自我介绍',
        '学习如何用西班牙语介绍自己',
        1,
        1,
        '''## 自我介绍

今天我们要学习如何用西班牙语介绍自己。

### 核心句型

1. Me llamo... （我叫...）
2. Soy de... （我是...人）
3. Tengo ... años （我...岁）
4. Vivo en... （我住在...）

### 例句

- Me llamo María. （我叫María。）
- Soy de China. （我是中国人。）
- Tengo 25 años. （我25岁。）
- Vivo en Pekín. （我住在北京。）

### 练习
请完成下方的练习题，掌握自我介绍的句型。
''',
        1  # 已解锁
    ))
    course_id = cursor.lastrowid

    # 创建练习题
    exercises = [
        {
            'type': 'choice',
            'question': '"我叫Luis"用西班牙语怎么说？',
            'options': json.dumps(['Me llamo Luis', 'Me nombre Luis', 'Yo soy Luis', 'Me llam Luis']),
            'answer': 'Me llamo Luis',
            'explanation': '"Me llamo" 是"我叫"的意思，后面加名字。'
        },
        {
            'type': 'true_false',
            'question': '"Soy de China"的意思是"我住在中国"。',
            'options': None,
            'answer': 'False',
            'explanation': '"Soy de China"的意思是"我是中国人"。"我住在中国"应该是"Vivo en China"。'
        },
        {
            'type': 'fill',
            'question': '完成句子："Tengo ____ años"（我20岁）',
            'options': None,
            'answer': '20',
            'explanation': '"Tengo"是"我有"的意思，"años"是"岁"。'
        },
        {
            'type': 'choice',
            'question': '"我住在马德里"用西班牙语怎么说？',
            'options': json.dumps(['Vivo en Madrid', 'Soy en Madrid', 'Estoy en Madrid', 'Vivo de Madrid']),
            'answer': 'Vivo en Madrid',
            'explanation': '"Vivo en" 是"我住在"的意思，后面加地名。'
        }
    ]

    for ex in exercises:
        cursor.execute('''
            INSERT INTO exercises (course_id, question_type, question_text, options, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            course_id,
            ex['type'],
            ex['question'],
            ex['options'],
            ex['answer'],
            ex['explanation']
        ))

    conn.commit()
    conn.close()

    print(f"[OK] 课程创建成功！课程ID: {course_id}")
    print(f"[OK] 创建了 {len(exercises)} 道练习题")

if __name__ == '__main__':
    create_sample_course()
