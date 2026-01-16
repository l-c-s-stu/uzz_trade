document.addEventListener('DOMContentLoaded', () => {
    const formContainer = document.getElementById('formContainer');
    
    // 检查用户登录状态
    if (!apiClient.isLoggedIn()) {
        formContainer.innerHTML = `
            <div class="error">
                <h3>请先登录</h3>
                <p>发布商品需要先登录账号</p>
                <a href="login.html" class="btn btn-primary">去登录</a>
            </div>
        `;
        return;
    }
    
    // 显示发布表单
    showCreateForm();
});

function showCreateForm() {
    const formContainer = document.getElementById('formContainer');
    
    formContainer.innerHTML = `
        <form id="createGoodsForm">
            <div class="form-group">
                <label for="title">商品标题 <span class="required">*</span></label>
                <input type="text" id="title" name="title" required 
                       placeholder="请输入商品标题" maxlength="100">
                <small>简洁明了地描述你的商品</small>
            </div>
            
            <div class="form-group">
                <label for="description">商品描述 <span class="required">*</span></label>
                <textarea id="description" name="description" required 
                          placeholder="详细描述商品的特点、使用情况、购买时间等信息"></textarea>
                <small>详细的描述有助于买家了解商品</small>
            </div>
            
            <div class="form-group">
                <label for="price">价格 <span class="required">*</span></label>
                <input type="number" id="price" name="price" required 
                       placeholder="0.00" step="0.01" min="0">
                <small>请输入合理的价格（元）</small>
            </div>
            
            <div class="form-group">
                <label for="image">商品图片</label>
                <input type="file" id="image" name="image" accept="image/*">
                <small>支持 JPG、PNG、GIF 格式，建议尺寸 800x600 以上</small>
                <div id="imagePreview" class="image-preview"></div>
            </div>
            
            <div class="submit-section">
                <button type="submit" class="btn btn-success btn-large">发布商品</button>
                <button type="button" class="btn btn-danger btn-large" onclick="resetForm()">重置表单</button>
            </div>
        </form>
    `;
    
    setupFormHandlers();
}

function setupFormHandlers() {
    const form = document.getElementById('createGoodsForm');
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
            submitBtn.textContent = '发布中...';
            
            const response = await apiClient.createGood({
                title: formData.get('title'),
                description: formData.get('description'),
                price: formData.get('price'),
                image: formData.get('image')
            });
            
            if (response.ok) {
                const good = await response.json();
                showSuccessMessage(good);
            } else {
                const errorData = await response.json();
                alert('发布失败：' + JSON.stringify(errorData));
            }
        } catch (error) {
            alert('发布失败：网络错误');
            console.error('发布商品错误:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = '发布商品';
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

function showSuccessMessage(good) {
    const formContainer = document.getElementById('formContainer');
    
    formContainer.innerHTML = `
        <div class="success">
            <h3>🎉 商品发布成功！</h3>
            <p>你的商品《${good.title}》已成功发布</p>
            <div style="margin: 20px 0;">
                <a href="goods_detail.html?id=${good.id}" class="btn btn-primary">查看商品</a>
                <a href="goods.html" class="btn btn-success">返回列表</a>
                <button onclick="showCreateForm()" class="btn btn-primary">继续发布</button>
            </div>
        </div>
    `;
}

function resetForm() {
    if (confirm('确定要重置表单吗？所有输入的内容将被清空。')) {
        document.getElementById('createGoodsForm').reset();
        document.getElementById('imagePreview').innerHTML = '';
    }
}



