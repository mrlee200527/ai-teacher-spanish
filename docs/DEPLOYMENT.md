# 部署文档

## 前置要求

- Python 3.12+
- pip（Python包管理工具）
- 小米大模型API密钥

---

## 本地开发环境搭建

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

创建 `.env` 文件（在backend目录下）：

```env
SECRET_KEY=your-secret-key-here
```

### 3. 初始化数据库

数据库会在第一次运行时自动创建，无需手动初始化。

### 4. 启动服务器

```bash
cd backend
python app.py
```

服务器启动后，访问 `http://localhost:5000`

---

## 首次使用

### 1. 生成课程内容（教师功能）

使用API生成第一门课程：

```bash
curl -X POST http://localhost:5000/api/courses/generate \
  -H "Content-Type: application/json" \
  -d '{
    "week_number": 1,
    "day_number": 1,
    "title": "自我介绍",
    "topic": "自我介绍"
  }'
```

### 2. 学生登录

访问 `http://localhost:5000`
- 输入用户名
- 输入小米大模型API密钥
- 点击登录

### 3. 学习课程

- 查看课程列表
- 点击"开始学习"
- 学习课文内容
- 完成练习题
- 标记为已完成

---

## 生产环境部署

### 方案1：使用Gunicorn（推荐）

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务器
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 方案2：使用Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.12

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY frontend/ ./frontend/

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建并运行：

```bash
docker build -t ai-teacher .
docker run -p 5000:5000 ai-teacher
```

### 方案3：使用云服务器（阿里云/腾讯云）

1. 购买云服务器
2. 安装Python环境
3. 上传代码（Git或直接上传）
4. 按照本地开发环境搭建步骤操作
5. 使用Nginx反向代理

---

## 域名配置

### 配置Nginx反向代理

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 配置HTTPS（Let's Encrypt）

```bash
# 安装Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d yourdomain.com
```

---

## 微信机器人集成

### 步骤1：开发微信机器人

使用微信开发者工具或第三方SDK开发微信机器人。

### 步骤2：调用API接口

定时调用以下接口：

- 推送课程链接：`GET /api/wechat/push/{student_id}`
- 查询完成率：`GET /api/wechat/completion-rate`
- 解锁下一环节：`POST /api/wechat/unlock-next`
- 提醒学生：`GET /api/wechat/remind`

### 步骤3：定时任务

使用Cron或类似工具设置定时任务：

```bash
# 每天早上9点推送课程
0 9 * * * curl http://yourdomain.com/api/wechat/push/{student_id}

# 每天晚上8点提醒未完成的学生
0 20 * * * curl http://yourdomain.com/api/wechat/remind
```

---

## 常见问题

### 1. API密钥存储在哪里？

API密钥存储在Session中（服务器端内存），不会保存到数据库或文件中。Session过期（2小时）后密钥自动清除。

### 2. 如何修改Session过期时间？

编辑 `backend/config.py`：

```python
PERMANENT_SESSION_LIFETIME = 7200  # 2小时（单位：秒）
```

### 3. 数据库文件在哪里？

数据库文件位于：`data/aiteacher.db`（项目根目录）

### 4. 如何备份数据库？

```bash
# 备份
cp data/aiteacher.db data/aiteacher.db.backup

# 恢复
cp data/aiteacher.db.backup data/aiteacher.db
```

### 5. 如何重置数据库？

删除数据库文件即可：

```bash
rm data/aiteacher.db
```

下次启动时会自动创建新的数据库。

---

## 性能优化建议

1. **使用缓存**：缓存课程内容、练习题等静态数据
2. **数据库索引**：为常用查询字段添加索引
3. **负载均衡**：使用Nginx做负载均衡，部署多个Flask实例
4. **CDN加速**：使用CDN加速静态资源（CSS/JS/图片）
5. **压缩响应**：启用Gzip压缩

---

## 安全建议

1. **修改SECRET_KEY**：生产环境使用随机生成的密钥
2. **启用HTTPS**：使用Let's Encrypt免费SSL证书
3. **限制CORS**：仅允许特定域名访问
4. **定期备份数据库**：防止数据丢失
5. **监控日志**：监控访问日志，及时发现异常
