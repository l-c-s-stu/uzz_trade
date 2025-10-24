document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert('两次输入的密码不一致，请重新输入。');
        return;
    }

    try {
        const response = await apiClient.register({username, email, phone, password});

        if (response.ok) {
            alert('注册成功！请登录。');
            window.location.href = 'login.html';
        } else {
            const errorData = await response.json();
            alert('注册失败：' + JSON.stringify(errorData));
        }
    } catch (error) {
        alert('注册失败：网络错误');
        console.error('注册错误:', error);
    }
});