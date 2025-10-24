document.addEventListener('DOMContentLoaded', async () => {
    const formContainer = document.getElementById('formContainer');
    
    // 检查用户登录状态
    if (!apiClient.isLoggedIn()) {
        formContainer.innerHTML = `
            <div class="error">
                <h3>请先登录</h3>
                <p>编辑商品需要先登录账号</p>
                <a href="login.html" class="btn btn-primary">去登录</a>
            </div>
        `;
        return;
    }
    
    // 获取商品ID
    const urlParams = new URLSearchParams(window.location.search);
    const goodsId = urlParams.get('id');
    
    if (!goodsId) {
        formContainer.innerHTML = `
            <div class="error">
                <h3>商品ID缺失</h3>
                <p>请从商品列表或详情页进入编辑页面</p>
                <a href="goods.html" class="btn btn-primary">返回商品列表</a>
            </div>
        `;
        return;
    }
    
    // 加载商品信息
    await loadGoodsInfo(goodsId);
});

async function loadGoodsInfo(goodsId) {
    const formContainer = document.getElementById('formContainer');
    
    try {
        const response = await apiClient.getGoodDetail(goodsId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const goods = await response.json();
        
        // 检查用户是否有权限编辑
        if (!goods.is_owner) {
            formContainer.innerHTML = `
                <div class="error">
                    <h3>权限不足</h3>
                    <p>您只能编辑自己发布的商品</p>
                    <a href="goods.html" class="btn btn-primary">返回商品列表</a>
                </div>
            `;
            return;
        }
        
        // 显示编辑表单
        showEditForm(goods);
        
    } catch (error) {
        console.error('加载商品信息失败', error);
        formContainer.innerHTML = `
            <div class="error">
                <h3>加载失败</h3>
                <p>无法加载商品信息，请稍后重试</p>
                <a href="goods.html" class="btn btn-primary">返回商品列表</a>
            </div>
        `;
    }
}

function showEditForm(goods) {
    const formContainer = document.getElementById('formContainer');
    
    formContainer.innerHTML = `
        <form id="editGoodsForm">
            <div class="form-group">
                <label for="title">商品标题 <span class="required">*</span></label>
                <input type="text" id="title" name="title" required 
                       placeholder="请输入商品标题" maxlength="100" value="${goods.title}">
                <small>简洁明了地描述你的商品</small>
            </div>
            
            <div class="form-group">
                <label for="description">商品描述 <span class="required">*</span></label>
                <textarea id="description" name="description" required 
                          placeholder="详细描述商品的特点、使用情况、购买时间等信息">${goods.description}</textarea>
                <small>详细的描述有助于买家了解商品</small>
            </div>
            
            <div class="form-group">
                <label for="price">价格 <span class="required">*</span></label>
                <input type="number" id="price" name="price" required 
                       placeholder="0.00" step="0.01" min="0" value="${goods.price}">
                <small>请输入合理的价格（元）</small>
            </div>
            
            <div class="form-group">
                <label for="image">商品图片</label>
                <input type="file" id="image" name="image" accept="image/*">
                <small>支持 JPG、PNG、GIF 格式，建议尺寸 800x600 以上。不选择文件则保持原图片</small>
                <div id="imagePreview" class="image-preview"></div>
            </div>
            
            ${goods.image ? `
            <div class="form-group">
                <label>当前图片</label>
                <div class="current-image">
                    <img src="${goods.image}" alt="${goods.title}" />
                    <p>当前商品图片</p>
                </div>
            </div>
            ` : ''}
            
            <div class="submit-section">
                <button type="submit" class="btn btn-success btn-large">保存修改</button>
                <button type="button" class="btn btn-danger btn-large" onclick="cancelEdit()">取消编辑</button>
            </div>
        </form>
    `;
    
    setupEditFormHandlers(goods.id);
}

function setupEditFormHandlers(goodsId) {
    const form = document.getElementById('editGoodsForm');
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    
    // 图片预览
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="预览图片">`;
            };
            reader.readAsDataURL(file);
        } else {
            imagePreview.innerHTML = '';
        }
    });
    
    // 表单提交
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // 验证表单
        if (!validateForm(formData)) {
            return;
        }
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = '保存中...';
            
            const response = await apiClient.updateGood(goodsId, {
                title: formData.get('title'),
                description: formData.get('description'),
                price: formData.get('price'),
                image: formData.get('image')
            });
            
            if (response.ok) {
                const result = await response.json();
                showSuccessMessage(result.data);
            } else {
                const errorData = await response.json();
                alert('修改失败：' + JSON.stringify(errorData));
            }
        } catch (error) {
            alert('修改失败：网络错误');
            console.error('修改商品错误:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = '保存修改';
        }
    });
}

function validateForm(formData) {
    const title = formData.get('title').trim();
    const description = formData.get('description').trim();
    const price = parseFloat(formData.get('price'));
    
    if (!title) {
        alert('请输入商品标题');
        return false;
    }
    
    if (!description) {
        alert('请输入商品描述');
        return false;
    }
    
    if (!price || price <= 0) {
        alert('请输入有效的价格');
        return false;
    }
    
    if (price > 999999.99) {
        alert('价格不能超过999999.99元');
        return false;
    }
    
    return true;
}

function showSuccessMessage(goods) {
    const formContainer = document.getElementById('formContainer');
    
    formContainer.innerHTML = `
        <div class="success">
            <h3>🎉 商品修改成功！</h3>
            <p>商品《${goods.title}》已成功修改</p>
            <div style="margin: 20px 0;">
                <a href="goods_detail.html?id=${goods.id}" class="btn btn-primary">查看商品</a>
                <a href="goods.html" class="btn btn-success">返回列表</a>
            </div>
        </div>
    `;
}

function cancelEdit() {
    if (confirm('确定要取消编辑吗？未保存的修改将丢失。')) {
        window.location.href = 'goods.html';
    }
}

