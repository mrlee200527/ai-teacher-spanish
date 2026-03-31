# API接口文档

## 基础信息

- **基础URL**：`http://localhost:5000`
- **Content-Type**：`application/json`

---

## 认证接口

### POST /api/login

登录

**请求参数**：
```json
{
  "username": "用户名",
  "api_key": "小米大模型API密钥"
}
```

**响应**：
```json
{
  "success": true,
  "user_id": 1,
  "username": "用户名"
}
```

**错误响应**：
```json
{
  "error": "用户名不能为空"
}
```

---

### POST /api/logout

登出

**请求**：无

**响应**：
```json
{
  "success": true
}
```

---

### GET /api/check-login

检查登录状态

**请求**：无

**响应**：
```json
{
  "logged_in": true,
  "user_id": 1,
  "username": "用户名"
}
```

---

## 课程接口

### GET /api/courses

获取课程列表

**请求**：无（需要登录）

**响应**：
```json
{
  "courses": [
    {
      "id": 1,
      "title": "自我介绍",
      "description": "学习基本的自我介绍表达",
      "week_number": 1,
      "day_number": 1,
      "content": "课文内容...",
      "is_unlocked": true,
      "is_completed": false,
      "created_at": "2026-03-31 23:00:00"
    }
  ]
}
```

---

### GET /api/courses/{course_id}

获取课程详情

**请求**：无（需要登录）

**响应**：
```json
{
  "course": {
    "id": 1,
    "title": "自我介绍",
    "description": "学习基本的自我介绍表达",
    "week_number": 1,
    "day_number": 1,
    "content": "课文内容...",
    "is_unlocked": true,
    "created_at": "2026-03-31 23:00:00"
  },
  "exercises": [
    {
      "id": 1,
      "course_id": 1,
      "question_type": "choice",
      "question_text": "Me ____ Juan.",
      "options": ["soy", "estoy", "tengo", "vivo"],
      "correct_answer": null,
      "explanation": "Me soy 是错误的表达，应该用 Me llamo"
    }
  ],
  "progress": {
    "id": 1,
    "student_id": 1,
    "course_id": 1,
    "is_completed": false,
    "completed_at": null
  }
}
```

---

### POST /api/courses/generate

生成课程内容（教师功能）

**请求**：
```json
{
  "week_number": 1,
  "day_number": 1,
  "title": "自我介绍",
  "topic": "自我介绍"
}
```

**响应**：
```json
{
  "success": true,
  "course_id": 1,
  "exercise_count": 3
}
```

---

### POST /api/courses/{course_id}/exercises/{exercise_id}/submit

提交练习答案

**请求**：
```json
{
  "answer": "soy"
}
```

**响应**：
```json
{
  "success": true,
  "is_correct": false,
  "feedback": "Me soy 是错误的表达，应该用 Me llamo",
  "correct_answer": "Me llamo"
}
```

---

### POST /api/courses/{course_id}/complete

标记课程为已完成

**请求**：无（需要登录）

**响应**：
```json
{
  "success": true
}
```

**错误响应**：
```json
{
  "error": "请完成所有练习后再标记完成"
}
```

---

## 进度接口

### GET /api/progress

获取学习进度

**请求**：无（需要登录）

**响应**：
```json
{
  "total_courses": 7,
  "completed_courses": 3,
  "completion_rate": 42.86,
  "wrong_answers": [
    {
      "id": 1,
      "student_id": 1,
      "exercise_id": 1,
      "wrong_answer": "soy",
      "correct_answer": "Me llamo",
      "feedback": "Me soy 是错误的表达，应该用 Me llamo",
      "created_at": "2026-03-31 23:30:00",
      "question_text": "Me ____ Juan.",
      "question_type": "choice"
    }
  ]
}
```

---

## 微信机器人接口

### GET /api/wechat/push/{student_id}

推送课程链接给学生

**请求**：无

**响应**：
```json
{
  "success": true,
  "message": "新课程已解锁：自我介绍",
  "course_url": "http://localhost:5000/course.html?id=1"
}
```

---

### GET /api/wechat/completion-rate

获取课程完成率

**请求**：无

**响应**：
```json
{
  "total_courses": 7,
  "completed_courses": 3,
  "completion_rate": 42.86
}
```

---

### POST /api/wechat/unlock-next

解锁下一环节（当完成率达到60%时自动调用）

**请求**：无

**响应**：
```json
{
  "success": true,
  "message": "已解锁新课程（ID: 2）",
  "completion_rate": 60.0
}
```

**错误响应**：
```json
{
  "success": false,
  "message": "完成率未达到60%（当前：42.86%）"
}
```

---

### GET /api/wechat/remind

提醒未完成的学生

**请求**：无

**响应**：
```json
{
  "success": true,
  "count": 2,
  "students": [
    {
      "student_id": 2,
      "username": "student2",
      "nickname": "学员student2",
      "incomplete_courses": 1
    }
  ]
}
```

---

## 错误码说明

| HTTP状态码 | 说明 |
|----------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未登录 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
