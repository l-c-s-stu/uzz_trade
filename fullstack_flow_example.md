# 🔄 全栈开发通信流程示例

## 场景：用户删除商品

### 1. 用户操作
```
用户在浏览器中点击"删除商品"按钮
```

### 2. 前端处理
```javascript
// goods.js
async function deleteGood(goodsId) {
    // 确认删除
    if (!confirm('确定要删除这个商品吗？')) {
        return;
    }
    
    // 发送删除请求
    const response = await apiClient.deleteGood(goodsId);
    
    if (response.ok) {
        alert('删除成功！');
        location.reload(); // 刷新页面显示最新数据
    }
}
```

### 3. API请求
```javascript
// api.js
async deleteGood(id) {
    const response = await this.request(`/goods/${id}/delete/`, {
        method: 'DELETE',  // HTTP方法
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access')}`  // 用户认证
        }
    });
    return response;
}
```

### 4. 后端路由
```python
# goods/urls.py
urlpatterns = [
    path('<int:pk>/delete/', GoodsDeleteView.as_view(), name='goods_delete'),
]
```

### 5. 后端视图处理
```python
# goods/views.py
class GoodsDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # 获取商品对象
        self.perform_destroy(instance)  # 从数据库删除
        return Response({'message': '商品删除成功'}, status=200)
```

### 6. 权限检查
```python
# goods/views.py
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 管理员可以删除任何商品
        if request.user.is_superuser:
            return True
        # 商品发布者可以删除自己的商品
        return obj.owner == request.user
```

### 7. 数据库操作
```python
# Django自动执行SQL
DELETE FROM goods_goods WHERE id = 1;
```

### 8. 响应返回
```json
{
    "message": "商品删除成功"
}
```

### 9. 前端更新
```javascript
// 用户看到删除成功的提示
alert('删除成功！');
// 页面刷新，显示最新的商品列表
location.reload();
```

## 🔑 关键概念

### HTTP方法
- **GET**: 获取数据 (查看商品列表)
- **POST**: 创建数据 (发布新商品)
- **PUT/PATCH**: 更新数据 (修改商品信息)
- **DELETE**: 删除数据 (删除商品)

### 状态码
- **200**: 成功
- **401**: 未授权 (需要登录)
- **403**: 禁止访问 (权限不足)
- **404**: 未找到
- **500**: 服务器错误

### 数据格式
- **JSON**: 前后端交换数据的标准格式
- **FormData**: 上传文件时使用

