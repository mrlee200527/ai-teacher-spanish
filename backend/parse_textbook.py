"""解析教材文本，提取课程结构"""
import re
import sys

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

input_file = "d:/2026-03-31_AITeacher/course/textbook_extract.txt"
output_file = "d:/2026-03-31_AITeacher/course/textbook_parsed.md"

print("=" * 60)
print("教材课程结构解析")
print("=" * 60)

try:
    # 读取提取的文本
    print(f"\n[读取文件...]")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"[OK] 文本长度: {len(text)} 字符")
    
    # 识别课程标题（常见的教材格式）
    print(f"\n[识别课程结构...]")
    
    # 常见的课程标题模式
    patterns = [
        r'Lecci[oó]n\s+(\d+)',  # Lección 1
        r'第\s*(\d+)\s*[课课]+',  # 第1课
        r'Unidad\s+(\d+)',  # Unidad 1
        r'Lesson\s+(\d+)',  # Lesson 1
    ]
    
    # 查找所有课程标题
    lessons = []
    for pattern in patterns:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in matches:
            lesson_num = match.group(1)
            start_pos = match.start()
            end_pos = min(start_pos + 2000, len(text))  # 取标题后2000字符
            lesson_title = text[start_pos:end_pos].strip()
            lessons.append({
                'number': lesson_num,
                'title': lesson_title[:100],  # 前100字符
                'position': start_pos
            })
    
    # 去重
    seen_numbers = set()
    unique_lessons = []
    for lesson in lessons:
        if lesson['number'] not in seen_numbers:
            seen_numbers.add(lesson['number'])
            unique_lessons.append(lesson)
    
    # 按课程编号排序
    unique_lessons.sort(key=lambda x: int(x['number']))
    
    print(f"[OK] 识别到 {len(unique_lessons)} 个课程")
    
    # 显示识别结果
    print(f"\n[课程列表]")
    print("-" * 60)
    for i, lesson in enumerate(unique_lessons[:10], 1):  # 只显示前10个
        print(f"{i}. 第 {lesson['number']} 课")
        print(f"   标题预览: {lesson['title'][:80]}")
        print()
    
    # 提取前5课的完整内容
    print(f"[提取前5课完整内容...]")
    parsed_content = "# 教材课程结构解析\n\n"
    parsed_content += f"识别到 {len(unique_lessons)} 个课程\n\n"
    
    for i, lesson in enumerate(unique_lessons[:5], 1):
        parsed_content += f"{'='*60}\n"
        parsed_content += f"第 {lesson['number']} 课\n"
        parsed_content += f"{'='*60}\n\n"
        
        # 提取课程内容（从当前位置到下一个课程标题）
        start_pos = lesson['position']
        if i < len(unique_lessons[:5]):
            end_pos = unique_lessons[i]['position']
        else:
            end_pos = min(start_pos + 5000, len(text))  # 最多5000字符
        
        lesson_content = text[start_pos:end_pos].strip()
        parsed_content += lesson_content
        parsed_content += "\n\n"
    
    # 保存解析结果
    print(f"[保存解析结果...]")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(parsed_content)
    
    print(f"[OK] 解析结果已保存到: {output_file}")
    
    print("\n" + "=" * 60)
    print("解析完成！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 检查解析的课程结构（必要时手动调整）")
    print("2. 使用课程内容创建学习系统课程")
    
except FileNotFoundError:
    print(f"[ERROR] 文件不存在: {input_file}")
    print(f"\n请先运行OCR提取脚本:")
    print(f"  python extract_textbook_ocr.py")
except Exception as e:
    print(f"[ERROR] 解析失败: {e}")
    import traceback
    traceback.print_exc()
