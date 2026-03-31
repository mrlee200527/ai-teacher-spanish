// 进度页面JavaScript
const API_BASE = 'http://localhost:5000';

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    loadProgress();
});

// 加载进度
function loadProgress() {
    showLoading();
    
    fetch(`${API_BASE}/api/progress`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            // 更新统计数据
            document.getElementById('total-courses').textContent = data.total_courses;
            document.getElementById('completed-courses').textContent = data.completed_courses;
            document.getElementById('completion-rate').textContent = data.completion_rate + '%';
            
            // 显示完成率提示
            showCompletionNotice(data.completion_rate);
            
            // 显示错题本
            showWrongAnswers(data.wrong_answers);
        })
        .catch(error => {
            hideLoading();
            console.error('加载进度失败:', error);
            alert('加载进度失败，请刷新页面重试');
        });
}

// 显示完成率提示
function showCompletionNotice(completionRate) {
    const noticeCard = document.getElementById('completion-notice');
    const noticeText = document.getElementById('completion-notice-text');
    
    if (completionRate >= 60) {
        noticeCard.style.display = 'block';
        noticeCard.style.backgroundColor = '#E8F5E9';
        noticeCard.style.borderLeftColor = '#4CAF50';
        noticeText.innerHTML = `<strong>恭喜！</strong> 你的完成率已达到 ${completionRate}%，可以解锁下一环节了！`;
    } else if (completionRate >= 40) {
        noticeCard.style.display = 'block';
        noticeCard.style.backgroundColor = '#FFF3E0';
        noticeCard.style.borderLeftColor = '#FF9800';
        noticeText.innerHTML = `<strong>加油！</strong> 你的完成率为 ${completionRate}%，再完成 ${60 - completionRate}% 就可以解锁下一环节了！`;
    } else {
        noticeCard.style.display = 'none';
    }
}

// 显示错题本
function showWrongAnswers(wrongAnswers) {
    const wrongList = document.getElementById('wrong-answers-list');
    wrongList.innerHTML = '';
    
    if (wrongAnswers.length === 0) {
        wrongList.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">太棒了！你还没有错题记录</p>';
        return;
    }
    
    wrongAnswers.forEach(item => {
        const wrongItem = document.createElement('div');
        wrongItem.className = 'wrong-answer-item';
        
        const typeLabels = {
            'choice': '选择题',
            'true_false': '判断题',
            'fill': '填空题',
            'writing': '写作题'
        };
        
        wrongItem.innerHTML = `
            <h4>${typeLabels[item.question_type] || '练习题'}</h4>
            <p><strong>题目:</strong> ${item.question_text}</p>
            <p><strong>你的答案:</strong> ${item.wrong_answer}</p>
            <p><strong>正确答案:</strong> ${item.correct_answer}</p>
            <div class="feedback">
                <strong>解析:</strong> ${item.feedback}
            </div>
        `;
        
        wrongList.appendChild(wrongItem);
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
