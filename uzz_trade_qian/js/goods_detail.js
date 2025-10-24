document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const goodsId = urlParams.get('id');
    
    if (!goodsId) {
        document.getElementById('goodsDetail').innerHTML = '<div class="error">商品ID无效</div>';
        return;
    }

    try {
        // 加载商品详情
        await loadGoodsDetail(goodsId);
        
        // 加载评论
        await loadComments(goodsId);
        
        // 显示评论区域
        document.getElementById('commentsSection').style.display = 'block';
        
        // 如果用户已登录，显示评论表单
        if (apiClient.isLoggedIn()) {
            document.getElementById('commentForm').style.display = 'block';
            setupCommentForm(goodsId);
        }
        
    } catch (error) {
        console.error('加载商品详情失败:', error);
        document.getElementById('goodsDetail').innerHTML = '<div class="error">加载商品详情失败</div>';
    }
});

async function loadGoodsDetail(goodsId) {
    const response = await apiClient.getGoodDetail(goodsId);
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    
    const good = await response.json();
    
    const imageUrl = good.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuaXoOazleiDveWKoOi9vTwvdGV4dD48L3N2Zz4=';
    
    document.getElementById('goodsDetail').innerHTML = `
        <div class="goods-info">
            <div class="goods-image">
                <img src="${imageUrl}" alt="${good.title}" />
            </div>
            <div class="goods-meta">
                <h1 class="goods-title">${good.title}</h1>
                <div class="goods-price">¥${good.price}</div>
                <div class="goods-description">${good.description}</div>
                
                <div class="goods-stats">
                    <div class="stat-item">
                        <div class="stat-label">想买人数</div>
                        <div class="stat-value">${good.wish_count}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">发布人</div>
                        <div class="stat-value">${good.owner_name}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">发布时间</div>
                        <div class="stat-value">${new Date(good.created_at).toLocaleDateString()}</div>
                    </div>
                </div>
                
                <div class="action-buttons">
                    <button id="wishBtn" class="btn btn-warning">
                        ❤️ 想买
                    </button>
                    <button id="contactBtn" class="btn btn-success">
                        📞 联系卖家
                    </button>
                    ${good.is_owner ? `
                        <button id="editBtn" class="btn btn-primary">✏️ 编辑商品</button>
                        <button id="deleteBtn" class="btn btn-danger">🗑️ 删除商品</button>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    // 设置心愿单按钮
    setupWishButton(goodsId);
    
    // 设置联系卖家按钮
    setupContactButton();
    
    // 设置编辑和删除按钮
    if (good.is_owner) {
        setupEditButton(goodsId);
        setupDeleteButton(goodsId);
    }
}

async function loadComments(goodsId) {
    try {
        const response = await apiClient.getComments(goodsId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const comments = await response.json();
        
        document.getElementById('commentCount').textContent = `${comments.length} 条评论`;
        
        if (comments.length === 0) {
            document.getElementById('commentsList').innerHTML = '<div class="loading">暂无评论</div>';
            return;
        }
        
        const commentsHtml = comments.map(comment => `
            <div class="comment-item">
                <div class="comment-header">
                    <span class="comment-user">${comment.user_name}</span>
                    <span class="comment-time">${new Date(comment.created_at).toLocaleString()}</span>
                </div>
                <div class="comment-content">${comment.content}</div>
            </div>
        `).join('');
        
        document.getElementById('commentsList').innerHTML = commentsHtml;
        
    } catch (error) {
        console.error('加载评论失败:', error);
        document.getElementById('commentsList').innerHTML = '<div class="error">加载评论失败</div>';
    }
}

function setupCommentForm(goodsId) {
    const submitBtn = document.getElementById('submitComment');
    const commentText = document.getElementById('commentText');
    
    submitBtn.addEventListener('click', async () => {
        const content = commentText.value.trim();
        
        if (!content) {
            alert('请输入评论内容');
            return;
        }
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = '发表中...';
            
            const response = await apiClient.createComment(goodsId, content);
            
            if (response.ok) {
                commentText.value = '';
                alert('评论发表成功！');
                // 重新加载评论
                await loadComments(goodsId);
            } else {
                const errorData = await response.json();
                alert('评论发表失败：' + JSON.stringify(errorData));
            }
        } catch (error) {
            alert('评论发表失败：网络错误');
            console.error('发表评论错误:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = '发表评论';
        }
    });
}

function setupWishButton(goodsId) {
    const wishBtn = document.getElementById('wishBtn');
    
    wishBtn.addEventListener('click', async () => {
        if (!apiClient.isLoggedIn()) {
            alert('请先登录');
            window.location.href = 'login.html';
            return;
        }
        
        try {
            const response = await apiClient.addToWish(goodsId);
            
            if (response.ok) {
                const data = await response.json();
                alert(data.message);
                // 重新加载商品详情以更新想买人数
                await loadGoodsDetail(goodsId);
            } else {
                const errorData = await response.json();
                alert('操作失败：' + JSON.stringify(errorData));
                console.error('心愿单API错误:', response.status, errorData);
            }
        } catch (error) {
            alert('操作失败：网络错误 - ' + error.message);
            console.error('心愿单操作错误:', error);
        }
    });
}

function setupContactButton() {
    const contactBtn = document.getElementById('contactBtn');
    
    contactBtn.addEventListener('click', () => {
        alert('联系卖家功能开发中...\n\n你可以通过以下方式联系卖家：\n1. 在评论区留言\n2. 通过平台私信功能\n3. 查看卖家联系方式');
    });
}

function setupEditButton(goodsId) {
    const editBtn = document.getElementById('editBtn');
    
    editBtn.addEventListener('click', () => {
        if (!apiClient.isLoggedIn()) {
            alert('请先登录');
            window.location.href = 'login.html';
            return;
        }
        
        // 跳转到编辑页面
        window.location.href = `edit_goods.html?id=${goodsId}`;
    });
}

function setupDeleteButton(goodsId) {
    const deleteBtn = document.getElementById('deleteBtn');
    
    deleteBtn.addEventListener('click', async () => {
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
                // 返回商品列表
                window.location.href = 'goods.html';
            } else {
                const errorData = await response.json();
                alert('删除失败：' + JSON.stringify(errorData));
                console.error('删除商品API错误:', response.status, errorData);
            }
        } catch (error) {
            alert('删除失败：网络错误 - ' + error.message);
            console.error('删除商品错误:', error);
        }
    });
}
