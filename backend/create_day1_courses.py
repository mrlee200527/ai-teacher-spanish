"""将教材内容转换为学习系统课程格式"""
import sqlite3
import sys
from datetime import datetime

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

db_path = "d:/2026-03-31_AITeacher/data/aiteacher.db"

# Day 1：语音速成营（分为6个课程）
day1_courses = [
    {
        "week": 1,
        "day": 1,
        "title": "语音速成营-第1段：元音基础",
        "topic": "元音基础",
        "content": """# 元音基础（15分钟）

西语有5个元音，发音规则固定，学会就能读任何单词。

## 发音规则

| 元音 | 发音特点 | 中文类比 |
|------|---------|---------|
| **a** | 张大嘴，短促有力 | 像"啊" |
| **e** | 嘴角向两边拉开 | 像"诶"（微笑时说） |
| **i** | 咧嘴，嘴角向两边拉 | 像"一" |
| **o** | 圆嘴 | 像"喔" |
| **u** | 嘟嘴 | 像"乌" |

## 例词练习

跟读以下单词（每词读3遍）：

1. **mamá**（妈妈）- ma-má
2. **papá**（爸爸）- pa-pá
3. **papá**（爸爸）- pa-pá
4. **mamá**（妈妈）- ma-má
5. **papá**（爸爸）- pa-pá
6. **mamá**（妈妈）- ma-má

## 学习提示

西语有个超级棒的特点：**写什么读什么**，学会了发音规则，你就能读任何单词！""",
        "exercises": [
            {
                "type": "choice",
                "question": "元音 'a' 的发音特点是？",
                "options": ["张嘴，短促有力", "嘴角向两边拉", "圆嘴", "嘟嘴"],
                "answer": "A",
                "explanation": "元音 'a' 要张大嘴，像医生说'啊'。"
            },
            {
                "type": "choice",
                "question": "元音 'e' 的发音类似于中文的？",
                "options": ["啊", "诶", "一", "喔"],
                "answer": "B",
                "explanation": "元音 'e' 嘴角向两边拉开，像微笑时说'诶'。"
            },
            {
                "type": "true_false",
                "question": "西语元音发音规则是固定的",
                "answer": "T",
                "explanation": "正确！西语元音发音规则固定，学会就能读任何单词。"
            }
        ]
    },
    {
        "week": 1,
        "day": 1,
        "title": "语音速成营-第2段：辅音(1)鼻音与流音",
        "topic": "辅音(1)鼻音与流音",
        "content": """# 辅音（1）——鼻音与流音（15分钟）

## 学习内容

### 鼻音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **m** | 双唇闭合，鼻音 | mamá（妈妈） |
| **n** | 舌尖抵上齿龈，鼻音 | no（不） |
| **ñ** | 舌尖抵下齿龈，舌面中部上抬 | niño（孩子） |

### 流音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **l** | 舌尖抵上齿龈 | luna（月亮） |
| **r** | 舌尖轻触上齿龈（颤音） | pera（梨） |

## 例词练习

1. **mamá**（妈妈）
2. **no**（不）
3. **niño**（孩子）
4. **luna**（月亮）
5. **pera**（梨）

## 发音提示

- m/n：与中文类似，注意鼻音要明显
- ñ：类似中文拼音的"ni"（如"你"），但舌面要抬起
- l：与中文类似，舌位稍靠前
- r：西语特色颤音，开始可以只做单颤（类似英语"butter"中的tt）""",
        "exercises": [
            {
                "type": "choice",
                "question": "字母 'ñ' 的发音特点是？",
                "options": [
                    "舌尖抵上齿龈",
                    "舌尖抵下齿龈，舌面中部上抬",
                    "双唇闭合",
                    "舌尖轻触上齿龈"
                ],
                "answer": "B",
                "explanation": "字母 'ñ' 发音时舌尖抵下齿龈，舌面中部上抬。"
            },
            {
                "type": "choice",
                "question": "'luna' 的意思是？",
                "options": ["妈妈", "月亮", "梨", "孩子"],
                "answer": "B",
                "explanation": "'luna' 在西语中是'月亮'的意思。"
            },
            {
                "type": "true_false",
                "question": "西语的 'r' 是颤音",
                "answer": "T",
                "explanation": "正确！西语的 'r' 是颤音，舌尖轻触上齿龈。"
            }
        ]
    },
    {
        "week": 1,
        "day": 1,
        "title": "语音速成营-第3段：辅音(2)塞音",
        "topic": "辅音(2)塞音",
        "content": """# 辅音（2）——塞音（15分钟）

## 学习内容

### 清塞音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **p** | 双唇闭合后突然打开 | pan（面包） |
| **t** | 舌尖抵上齿龈后弹开 | taza（杯子） |
| **k**（c在a/o/u前） | 舌后部抵软腭 | casa（房子） |

### 浊塞音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **b** | 双唇闭合，振动声带 | beso（吻） |
| **d** | 舌尖抵上齿龈，振动声带 | día（日子） |
| **g**（在a/o/u前） | 舌后部抵软腭，振动声带 | gato（猫） |

## 例词练习

1. **pan**（面包）
2. **taza**（杯子）
3. **casa**（房子）
4. **beso**（吻）
5. **día**（日子）
6. **gato**（猫）

## 发音提示

- p/t/k：清音，不振动声带，发音要短促有力
- b/d/g：浊音，振动声带，发音要柔和
- 西语的b/v发音相同""",
        "exercises": [
            {
                "type": "choice",
                "question": "塞音中，哪些是清音？",
                "options": ["b/d/g", "p/t/k", "m/n/l", "ñ/r"],
                "answer": "B",
                "explanation": "p/t/k是清塞音，发音时不振动声带。"
            },
            {
                "type": "choice",
                "question": "'día' 的意思是？",
                "options": ["面包", "杯子", "房子", "日子"],
                "answer": "D",
                "explanation": "'día' 在西语中是'日子'的意思。"
            },
            {
                "type": "true_false",
                "question": "西语的 b 和 v 发音相同",
                "answer": "T",
                "explanation": "正确！西语的 b 和 v 发音相同。"
            }
        ]
    },
    {
        "week": 1,
        "day": 1,
        "title": "语音速成营-第4段：辅音(3)擦音与塞擦音",
        "topic": "辅音(3)擦音与塞擦音",
        "content": """# 辅音（3）——擦音与塞擦音（15分钟）

## 学习内容

### 擦音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **f** | 上齿轻触下唇 | café（咖啡） |
| **s** | 舌尖接近上齿龈 | sal（盐） |
| **z**（在c之前） | 舌尖接近上齿龈，气流从牙缝出 | zapato（鞋子） |

### 塞擦音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **ch** | 先塞后擦，类似中文"吃" | chino（中国人） |
| **ll** | 类似中文"耶"的连读 | llave（钥匙） |

## 例词练习

1. **café**（咖啡）
2. **sal**（盐）
3. **zapato**（鞋子）
4. **chino**（中国人）
5. **llave**（钥匙）

## 发音提示

- f/s/z：擦音，气流从缝隙中流出，摩擦声要明显
- ch：先塞住后摩擦，类似中文拼音"ch"
- ll：在西班牙大部分地区发音类似英语的"y"，在阿根廷等地发音类似英语的"sh"（zh音）""",
        "exercises": [
            {
                "type": "choice",
                "question": "'ch' 的发音类似中文拼音的？",
                "options": ["z", "c", "ch", "sh"],
                "answer": "C",
                "explanation": "'ch' 的发音类似中文拼音的 'ch'，先塞住后摩擦。"
            },
            {
                "type": "choice",
                "question": "'llave' 的意思是？",
                "options": ["咖啡", "盐", "鞋子", "钥匙"],
                "answer": "D",
                "explanation": "'llave' 在西语中是'钥匙'的意思。"
            },
            {
                "type": "true_false",
                "question": "擦音是从缝隙中流出的气流",
                "answer": "T",
                "explanation": "正确！擦音是通过窄缝形成的摩擦音。"
            }
        ]
    },
    {
        "week": 1,
        "day": 1,
        "title": "语音速成营-第5段：辅音(4)边音与其他",
        "topic": "辅音(4)边音与其他",
        "content": """# 辅音（4）——边音与其他（15分钟）

## 学习内容

### 边音

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **y** | 类似中文的"耶"或"义" | yo（我） |

### 其他

| 辅音 | 发音特点 | 例词 |
|------|---------|------|
| **w** | 类似英语的"w" | web（网页） |
| **x** | 在词首类似英语的"s"，在词中类似"ks" | examen（考试） |
| **j** / **g**（在e/i前） | 类似德语的"ch"（喉音） | jefe（老板）、gente（人） |
| **qu** | 发音为"k" | que（那） |
| **gui** | 发音为"gi" | guitarra（吉他） |

## 例词练习

1. **yo**（我）
2. **web**（网页）
3. **examen**（考试）
4. **jefe**（老板）
5. **que**（那）
6. **guitarra**（吉他）

## 发音提示

- y：类似英语的"y"，在大部分地区发音类似"j"
- j/ge/gi：喉音，类似德语"ich"或法语"r"，是西语特色音
- qu/gui中的u不发音""",
        "exercises": [
            {
                "type": "choice",
                "question": "'jefe' 的意思是？",
                "options": ["考试", "老板", "吉他", "网页"],
                "answer": "B",
                "explanation": "'jefe' 在西语中是'老板'的意思。"
            },
            {
                "type": "choice",
                "question": "在 'que' 中，字母 u 的发音是？",
                "options": ["发 'u' 音", "不发音", "发 'v' 音", "发 'w' 音"],
                "answer": "B",
                "explanation": "在 'que' 中，字母 u 不发音。"
            },
            {
                "type": "true_false",
                "question": "西语的 j 和 ge/gi 发音相同",
                "answer": "T",
                "explanation": "正确！西语的 j 和 ge/gi 都发喉音。"
            }
        ]
    },
    {
        "week": 1,
        "day": 1,
        "title": "语音速成营-第6段：综合测验",
        "topic": "语音综合测验",
        "content": """# 综合测验（15分钟）

恭喜你完成了前5段学习！现在是综合测验时间。

## 测验内容

### 第一部分：元音识别（10题）

1. 请读出以下单词：**amigo**（朋友）
   - a-mi-go
   - 提示：每个元音都要发清楚

2. 请读出以下单词：**español**（西班牙语）
   - es-pa-ñol
   - 提示：注意 ñ 的发音

### 第二部分：辅音拼读（10题）

3. 请读出以下单词：**mamá**
4. 请读出以下单词：**papá**
5. 请读出以下单词：**niño**
6. 请读出以下单词：**luna**
7. 请读出以下单词：**pan**
8. 请读出以下单词：**café**
9. 请读出以下单词：**chino**
10. 请读出以下单词：**guitarra**

### 第三部分：综合发音（5题）

11. 请读出以下单词：**Buenos días**（早上好）
12. 请读出以下单词：**¿Cómo estás?**（你好吗？）
13. 请读出以下单词：**Me llamo...**（我叫...）
14. 请读出以下单词：**Mucho gusto**（很高兴认识你）
15. 请读出以下单词：**Hasta luego**（再见）

## 学习提示

- 不要害怕犯错，大声读出来！
- 如果不确定，可以重听示范
- 完成这15题后，你就能读出大部分西语单词了！""",
        "exercises": [
            {
                "type": "choice",
                "question": "'Buenos días' 的意思是？",
                "options": ["再见", "谢谢", "早上好", "你好吗？"],
                "answer": "C",
                "explanation": "'Buenos días' 在西语中是'早上好'的意思。"
            },
            {
                "type": "choice",
                "question": "'Me llamo...' 的意思是？",
                "options": ["你好吗？", "我叫...", "再见", "很高兴认识你"],
                "answer": "B",
                "explanation": "'Me llamo...' 在西语中是'我叫...'的意思。"
            },
            {
                "type": "fill",
                "question": "'Hasta luego'的意思是______（用中文回答）",
                "answer": "再见",
                "explanation": "'Hasta luego' 是'再见'的意思。"
            },
            {
                "type": "writing",
                "question": "请用西语说'很高兴认识你'",
                "answer": "Mucho gusto",
                "explanation": "'很高兴认识你'的西语是 'Mucho gusto'。"
            }
        ]
    }
]

def create_courses():
    """创建课程到数据库"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("创建语音速成营课程（6段）")
    print("=" * 60)
    
    for i, course_data in enumerate(day1_courses, 1):
        print(f"\n[{i}/6] 创建课程: {course_data['title']}")
        
        # 插入课程
        cursor.execute("""
            INSERT INTO courses (week_number, day_number, title, description, content, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            course_data['week'],
            course_data['day'],
            course_data['title'],
            course_data['topic'],  # 用topic作为description
            course_data['content'],
            datetime.now().isoformat()
        ))
        
        course_id = cursor.lastrowid
        print(f"  [OK] 课程ID: {course_id}")
        
        # 插入练习题
        for j, exercise in enumerate(course_data['exercises'], 1):
            options_json = str(exercise.get('options', []))
            
            cursor.execute("""
                INSERT INTO exercises (course_id, question_type, question_text, options, correct_answer, explanation, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                course_id,
                exercise['type'],
                exercise['question'],
                options_json,
                exercise['answer'],
                exercise['explanation'],
                datetime.now().isoformat()
            ))
        
        print(f"  [OK] 创建了 {len(course_data['exercises'])} 道练习题")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("课程创建完成！")
    print("=" * 60)

if __name__ == "__main__":
    try:
        create_courses()
    except Exception as e:
        print(f"[ERROR] 创建失败: {e}")
        import traceback
        traceback.print_exc()
