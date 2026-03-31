// 首页JavaScript
const API_BASE = 'http://localhost:5000';

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    checkLogin();
    setupLoginForm();
    setupLogoutButton();
});

// 检查登录状态
function checkLogin() {
    fetch(`${API_BASE}/api/check-login`)
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                showCourseSection(data);
            } else {
                showLoginSection();
            }
        })
        .catch(error => {
            console.error('检查登录状态失败:', error);
            showLoginSection();
        });
}

// 显示登录区域
function showLoginSection() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('course-section').style.display = 'none';
}

// 显示课程区域
function showCourseSection(data) {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('course-section').style.display = 'block';
    
    document.getElementById('username-display').textContent = data.username;
    document.getElementById('user-info').innerHTML = `
        <span>欢迎, ${data.username}</span>
        <button id="logout-btn" class="btn btn-outline">退出</button>
    `;
    
    loadCourses();
    loadProgress();
}

// 设置登录表单
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const apiKey = document.getElementById('api-key').value;
        
        showLoading();
        
        fetch(`${API_BASE}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                api_key: apiKey
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                showCourseSection(data);
                // 保存API密钥到LocalStorage（可选，用于下次自动填充）
                localStorage.setItem('username', username);
            } else {
                alert(data.error || '登录失败');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('登录失败:', error);
            alert(`登录失败：${error.message || '请检查网络连接'}\n\n请确保后端服务器已启动：\ncd d:/2026-03-31_AITeacher/backend\npython app.py`);
        });
    });
    
    // 自动填充上次登录的用户名
    const lastUsername = localStorage.getItem('username');
    if (lastUsername) {
        document.getElementById('username').value = lastUsername;
    }
}

// 设置退出按钮
function setupLogoutButton() {
    document.getElementById('logout-btn')?.addEventListener('click', function() {
        if (confirm('确定要退出登录吗？')) {
            fetch(`${API_BASE}/api/logout`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showLoginSection();
                    localStorage.removeItem('username');
                }
            })
            .catch(error => {
                console.error('退出失败:', error);
            });
        }
    });
}

// 加载课程列表
function loadCourses() {
    fetch(`${API_BASE}/api/courses`)
        .then(response => response.json())
        .then(data => {
            const courseList = document.getElementById('course-list');
            courseList.innerHTML = '';
            
            if (data.courses.length === 0) {
                courseList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">暂无课程，请联系管理员添加课程</p>';
                return;
            }
            
            data.courses.forEach(course => {
                const courseCard = document.createElement('div');
                courseCard.className = `course-card ${course.is_completed ? 'completed' : ''}`;
                courseCard.innerHTML = `
                    <div class="course-info">
                        <h4>${course.title}</h4>
                        <p>第${course.week_number}周 - 第${course.day_number}天</p>
                        <p>${course.description}</p>
                    </div>
                    <div class="course-status">
                        <span class="status-badge ${course.is_completed ? 'completed' : 'incomplete'}">
                            ${course.is_completed ? '已完成' : '未完成'}
                        </span>
                        <a href="course.html?id=${course.id}" class="btn btn-primary">开始学习</a>
                    </div>
                `;
                courseList.appendChild(courseCard);
            });
        })
        .catch(error => {
            console.error('加载课程失败:', error);
            const courseList = document.getElementById('course-list');
            courseList.innerHTML = '<p style="text-align: center; color: #f44336; padding: 2rem;">加载课程失败，请刷新页面重试</p>';
        });
}

// 加载进度
function loadProgress() {
    fetch(`${API_BASE}/api/progress`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-courses').textContent = data.total_courses;
            document.getElementById('completed-courses').textContent = data.completed_courses;
            document.getElementById('completion-rate').textContent = data.completion_rate + '%';
        })
        .catch(error => {
            console.error('加载进度失败:', error);
        });
}

// 显示加载中
function showLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'flex';
}

// 隐藏加载中
function hideLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'none';
}
