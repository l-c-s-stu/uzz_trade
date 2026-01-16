from django.urls import path
from .views import (GoodsListCreateView, GoodsDetailView, GoodsDeleteView, GoodsUpdateView,
                   CategoryListView, GoodsImageCreateView, GoodsImageDeleteView)

#"/api/goods/"->所有商品
#"/api/goods/1/"->id=1的商品详情
#"/api/goods/1/update/"->修改id=1的商品
#"/api/goods/1/delete/"->删除id=1的商品
#"/api/goods/categories/"->获取所有分类
#"/api/goods/<goods_id>/images/"->为商品添加图片
#"/api/goods/images/<image_id>/delete/"->删除商品图片
urlpatterns = [
    # 商品列表和创建（GET 获取列表，POST 创建商品）
    path('', GoodsListCreateView.as_view(), name='goods_list_create'),
    # 商品详情
    path('<int:pk>/', GoodsDetailView.as_view(), name='goods_detail'),
    # 商品更新
    path('<int:pk>/update/', GoodsUpdateView.as_view(), name='goods_update'),
    # 商品删除
    path('<int:pk>/delete/', GoodsDeleteView.as_view(), name='goods_delete'),
    # 分类列表
    path('categories/', CategoryListView.as_view(), name='category_list'),
    # 商品图片管理
    path('<int:goods_id>/images/', GoodsImageCreateView.as_view(), name='goods_image_create'),
    path('images/<int:image_id>/delete/', GoodsImageDeleteView.as_view(), name='goods_image_delete'),
]
