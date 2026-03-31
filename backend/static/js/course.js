// 课程页面JavaScript
const API_BASE = 'http://localhost:5000';

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const courseId = urlParams.get('id');
    
    if (!courseId) {
        alert('缺少课程ID参数');
        window.location.href = 'index.html';
        return;
    }
    
    loadCourseDetail(courseId);
    setupCompleteButton(courseId);
});

// 加载课程详情
function loadCourseDetail(courseId) {
    fetch(`${API_BASE}/api/courses/${courseId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('course-loading').style.display = 'none';
            document.getElementById('course-content').style.display = 'block';
            
            // 显示课程信息
            document.getElementById('course-title').textContent = data.course.title;
            document.getElementById('course-description').textContent = data.course.description;
            document.getElementById('course-meta').textContent = `第${data.course.week_number}周 - 第${data.course.day_number}天`;
            
            // 显示课文内容
            const lessonText = document.getElementById('lesson-text');
            lessonText.innerHTML = formatLessonContent(data.course.content);
            
            // 显示练习题
            loadExercises(data.exercises);
            
            // 检查是否已完成
            if (data.progress && data.progress.is_completed) {
                const completeBtn = document.getElementById('complete-btn');
                completeBtn.textContent = '已完成';
                completeBtn.disabled = true;
            }
        })
        .catch(error => {
            console.error('加载课程详情失败:', error);
            document.getElementById('course-loading').innerHTML = `
                <p style="color: #f44336;">加载课程失败，请刷新页面重试</p>
                <a href="index.html" class="btn btn-secondary" style="margin-top: 1rem;">返回首页</a>
            `;
        });
}

// 格式化课文内容
function formatLessonContent(content) {
    // 将[西班牙语课文]和[中文翻译]格式化为HTML
    let formatted = content;
    
    // 替换[西班牙语课文]
    formatted = formatted.replace(/\[西班牙语课文\]/g, '<h3>西班牙语课文</h3>');
    
    // 替换[中文翻译]
    formatted = formatted.replace(/\[中文翻译\]/g, '<h3>中文翻译</h3>');
    
    return formatted;
}

// 加载练习题
function loadExercises(exercises) {
    const exercisesList = document.getElementById('exercises-list');
    exercisesList.innerHTML = '';
    
    if (exercises.length === 0) {
        exercisesList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">暂无练习题</p>';
        return;
    }
    
    exercises.forEach((exercise, index) => {
        const exerciseItem = document.createElement('div');
        exerciseItem.className = 'exercise-item';
        exerciseItem.id = `exercise-${exercise.id}`;
        
        let optionsHtml = '';
        if (exercise.question_type === 'choice' && exercise.options) {
            optionsHtml = exercise.options.map((option, i) => `
                <label class="option-item">
                    <input type="radio" name="exercise-${exercise.id}" value="${option}">
                    <span>${String.fromCharCode(65 + i)}. ${option}</span>
                </label>
            `).join('');
        } else if (exercise.question_type === 'true_false') {
            optionsHtml = `
                <label class="option-item">
                    <input type="radio" name="exercise-${exercise.id}" value="正确">
                    <span>正确</span>
                </label>
                <label class="option-item">
                    <input type="radio" name="exercise-${exercise.id}" value="错误">
                    <span>错误</span>
                </label>
            `;
        } else if (exercise.question_type === 'fill') {
            optionsHtml = `
                <input type="text" name="exercise-${exercise.id}" 
                       placeholder="请输入答案" 
                       style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px;">
            `;
        } else if (exercise.question_type === 'writing') {
            optionsHtml = `
                <textarea name="exercise-${exercise.id}" 
                          placeholder="请输入你的答案" 
                          rows="4"
                          style="width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-family: inherit;"></textarea>
            `;
        }
        
        exerciseItem.innerHTML = `
            <div class="exercise-question">${index + 1}. ${exercise.question_text}</div>
            <div class="exercise-options">${optionsHtml}</div>
            <div class="exercise-actions">
                <button onclick="submitExercise(${courseId}, ${exercise.id}, '${exercise.question_type}')" 
                        class="btn btn-primary">提交答案</button>
            </div>
            <div class="exercise-feedback" id="feedback-${exercise.id}"></div>
        `;
        
        exercisesList.appendChild(exerciseItem);
    });
}

// 提交练习答案
function submitExercise(courseId, exerciseId, questionType) {
    let answer;
    
    if (questionType === 'fill' || questionType === 'writing') {
        const input = document.querySelector(`[name="exercise-${exerciseId}"]`);
        answer = input.value.trim();
        
        if (!answer) {
            alert('请输入答案');
            return;
        }
    } else {
        const selected = document.querySelector(`[name="exercise-${exerciseId}"]:checked`);
        if (!selected) {
            alert('请选择一个答案');
            return;
        }
        answer = selected.value;
    }
    
    showLoading('提交中...');
    
    fetch(`${API_BASE}/api/courses/${courseId}/exercises/${exerciseId}/submit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        const feedbackDiv = document.getElementById(`feedback-${exerciseId}`);
        const exerciseItem = document.getElementById(`exercise-${exerciseId}`);
        
        if (data.success) {
            feedbackDiv.style.display = 'block';
            
            if (data.is_correct) {
                feedbackDiv.className = 'exercise-feedback correct';
                feedbackDiv.innerHTML = `<strong>✓ 回答正确！</strong><br>${data.feedback}`;
            } else {
                feedbackDiv.className = 'exercise-feedback incorrect';
                feedbackDiv.innerHTML = `<strong>✗ 回答错误</strong><br>正确答案: ${data.correct_answer}<br>${data.feedback}`;
            }
            
            exerciseItem.classList.add('completed');
            
            // 禁用提交按钮
            const submitBtn = exerciseItem.querySelector('button');
            submitBtn.disabled = true;
            submitBtn.textContent = '已提交';
            
            // 检查是否所有练习都已完成
            checkAllExercisesCompleted();
        } else {
            alert(data.error || '提交失败');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('提交答案失败:', error);
        alert('提交失败，请重试');
    });
}

// 检查是否所有练习都已完成
function checkAllExercisesCompleted() {
    const exerciseItems = document.querySelectorAll('.exercise-item');
    const completedItems = document.querySelectorAll('.exercise-item.completed');
    
    if (exerciseItems.length > 0 && exerciseItems.length === completedItems.length) {
        // 启用完成按钮
        const completeBtn = document.getElementById('complete-btn');
        completeBtn.disabled = false;
    }
}

// 设置完成按钮
function setupCompleteButton(courseId) {
    const completeBtn = document.getElementById('complete-btn');
    
    completeBtn.addEventListener('click', function() {
        if (!confirm('确定标记为已完成吗？')) {
            return;
        }
        
        showLoading('正在提交...');
        
        fetch(`${API_BASE}/api/courses/${courseId}/complete`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.success) {
                alert('恭喜！课程已完成');
                completeBtn.textContent = '已完成';
                completeBtn.disabled = true;
            } else {
                alert(data.error || '操作失败');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('标记完成失败:', error);
            alert('操作失败，请重试');
        });
    });
}

// 显示加载中
function showLoading(text) {
    const loading = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    if (loadingText) {
        loadingText.textContent = text || '加载中...';
    }
    loading.style.display = 'flex';
}

// 隐藏加载中
function hideLoading() {
    const loading = document.getElementById('loading-overlay');
    loading.style.display = 'none';
}
