document.addEventListener('DOMContentLoaded', async () => {
    const goodsContainer = document.getElementById('goodsContainer');
    const userInfo = document.getElementById('userInfo');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginLink = document.getElementById('loginLink');

    // 检查用户登录状态
    if (apiClient.isLoggedIn()) {
        const username = localStorage.getItem('username');
        userInfo.textContent = `欢迎，${username}`;
        logoutBtn.style.display = 'inline-block';
        loginLink.style.display = 'none';
        
        // 绑定退出登录事件
        logoutBtn.addEventListener('click', () => {
            apiClient.logout();
        });
    } else {
        userInfo.textContent = '请先登录';
        logoutBtn.style.display = 'none';
        loginLink.style.display = 'inline-block';
    }

    try {
        const response = await apiClient.getGoods();
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const goodsList = await response.json();
        
        if (goodsList.length === 0) {
            goodsContainer.innerHTML = '<div class="error">暂无商品</div>';
            return;
        }

        goodsContainer.innerHTML = '';
        
        goodsList.forEach(good => {
            const card = document.createElement('div');
            card.className = "goods-card";
            
            // 使用API返回的完整图片URL，如果没有图片则使用占位图
            const imageUrl = good.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4=';
            
            card.innerHTML = `
                <img src="${imageUrl}" alt="${good.title}" />
                <h3>${good.title}</h3>
                <p class="price">¥${good.price}</p>
                <p class="wish-count">❤️ ${good.wish_count} 人想买</p>
                <p style="font-size: 12px; color: #999;">发布人：${good.owner_name}</p>
                <p style="font-size: 12px; color: #999;">${new Date(good.created_at).toLocaleDateString()}</p>
                ${good.is_owner ? `
                    <div style="margin-top: 10px;">
                        <button class="edit-btn" onclick="event.stopPropagation(); editGood(${good.id})">编辑商品</button>
                        <button class="delete-btn" onclick="event.stopPropagation(); deleteGood(${good.id})">删除商品</button>
                    </div>
                ` : ''}
            `;
            
            // 点击卡片跳转到商品详情
            card.addEventListener('click', () => {
                window.location.href = `goods_detail.html?id=${good.id}`;
            });
            
            goodsContainer.appendChild(card);
        });
        
    } catch (error) {
        console.error('加载商品失败', error);
        goodsContainer.innerHTML = '<div class="error">无法加载商品列表，请稍后重试。</div>';
    }
});

// 删除商品函数
async function deleteGood(goodsId) {
    if (!apiClient.isLoggedIn()) {
        alert('请先登录');
        window.location.href = 'login.html';
        return;
    }
    
    if (!confirm('确定要删除这个商品吗？删除后无法恢复！')) {
        return;
    }
    
    try {
        const response = await apiClient.deleteGood(goodsId);
        
        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            // 重新加载商品列表
            location.reload();
        } else {
            const errorData = await response.json();
            alert('删除失败：' + JSON.stringify(errorData));
            console.error('删除商品API错误:', response.status, errorData);
        }
    } catch (error) {
        alert('删除失败：网络错误 - ' + error.message);
        console.error('删除商品错误:', error);
    }
}

// 编辑商品函数
function editGood(goodsId) {
    if (!apiClient.isLoggedIn()) {
        alert('请先登录');
        window.location.href = 'login.html';
        return;
    }
    
    // 跳转到编辑页面
    window.location.href = `edit_goods.html?id=${goodsId}`;
}