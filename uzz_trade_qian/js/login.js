const form = document.getElementById('loginForm');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await apiClient.login(username, password);

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            localStorage.setItem('username', username);
            alert('登录成功！');
            window.location.href = 'goods.html';
        } else {
            const errorData = await response.json();
            alert('登录失败：' + (errorData.detail || '请检查用户名和密码'));
        }
    } catch (error) {
        alert('登录失败：网络错误');
        console.error('登录错误:', error);
    }
});