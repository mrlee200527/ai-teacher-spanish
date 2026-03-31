"""小米大模型API客户端"""
import requests
from flask import session

class XiaoMiLLMClient:
    """小米大模型客户端"""
    
    def __init__(self):
        self.api_url = 'https://api.xiaomi.com/v1/chat/completions'
    
    def get_api_key(self):
        """从Session中获取API密钥"""
        return session.get('xiaomi_api_key')
    
    def set_api_key(self, api_key):
        """设置API密钥到Session"""
        session['xiaomi_api_key'] = api_key
    
    def chat(self, messages, model='xiaomi-pro'):
        """
        调用小米大模型对话接口
        
        Args:
            messages: 消息列表 [{'role': 'user', 'content': '...'}]
            model: 模型名称，默认 xiaomi-pro
        
        Returns:
            response: 响应内容
        """
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError('API密钥未设置，请先登录')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model,
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise Exception(f'API调用失败: {str(e)}')
    
    def generate_content(self, topic, level='A1'):
        """
        根据主题生成课文内容
        
        Args:
            topic: 主题（如：'自我介绍'）
            level: 级别（A1/A2）
        
        Returns:
            content: 生成的课文内容
        """
        prompt = f"""
        请生成一篇西班牙语课文，主题是"{topic}"，难度为{level}级别。
        要求：
        1. 包含实用的词汇和表达
        2. 包含中文翻译
        3. 适合零基础到A1水平的学习者
        4. 长度在200-300词之间
        
        请按以下格式输出：
        [西班牙语课文]
        ...
        
        [中文翻译]
        ...
        """
        
        messages = [
            {'role': 'system', 'content': '你是一位专业的西班牙语教师，擅长生成适合初学者的课文。'},
            {'role': 'user', 'content': prompt}
        ]
        
        return self.chat(messages)
    
    def generate_exercise(self, content, exercise_type='choice'):
        """
        根据课文生成练习题
        
        Args:
            content: 课文内容
            exercise_type: 练习类型（choice/true_false/fill）
        
        Returns:
            exercise: 练习题（JSON格式）
        """
        type_prompt = {
            'choice': '选择题',
            'true_false': '判断题',
            'fill': '填空题'
        }
        
        prompt = f"""
        请根据以下课文内容，生成一道{type_prompt.get(exercise_type, '选择题')}。
        
        课文：
        {content}
        
        要求：
        1. 题目要涵盖课文的核心知识点
        2. 难度适中，适合A1-A2水平
        3. 如果是选择题，请提供4个选项（A/B/C/D），并标注正确答案
        4. 如果是判断题，请标注正确答案（正确/错误）
        5. 如果是填空题，请标注正确答案
        6. 提供详细的解析
        
        请按以下JSON格式输出：
        {{
            "question": "题目内容",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "correct_answer": "正确答案",
            "explanation": "解析"
        }}
        """
        
        messages = [
            {'role': 'system', 'content': '你是一位专业的西班牙语教师，擅长生成练习题。请确保输出的是有效的JSON格式。'},
            {'role': 'user', 'content': prompt}
        ]
        
        return self.chat(messages)
    
    def grade_writing(self, student_answer, reference_answer):
        """
        批改写作题
        
        Args:
            student_answer: 学生答案
            reference_answer: 参考答案
        
        Returns:
            feedback: 批改反馈
        """
        prompt = f"""
        请批改以下西班牙语写作题。
        
        参考答案：
        {reference_answer}
        
        学生答案：
        {student_answer}
        
        要求：
        1. 指出语法错误
        2. 指出用词错误
        3. 给出修改建议
        4. 语气要鼓励，不要太严厉
        
        请按以下格式输出：
        [总体评价]
        ...
        
        [语法错误]
        ...
        
        [修改建议]
        ...
        """
        
        messages = [
            {'role': 'system', 'content': '你是一位专业的西班牙语教师，擅长批改写作。'},
            {'role': 'user', 'content': prompt}
        ]
        
        return self.chat(messages)
