from django.urls import path
from .views import GoodsListCreateView, GoodsDetailView, GoodsListView, GoodsDeleteView, GoodsUpdateView

#"/api/goods/"->所有商品
#"/api/goods/1/"->id=1的商品详情
#"/api/goods/1/update/"->修改id=1的商品
#"/api/goods/1/delete/"->删除id=1的商品
urlpatterns = [
    path('', GoodsListCreateView.as_view(), name='goods_list_create'),
    path('', GoodsListView.as_view(), name='goods_list'),
    path('<int:pk>', GoodsDetailView.as_view(), name='goods_detail'),
    path('<int:pk>/update/', GoodsUpdateView.as_view(), name='goods_update'),
    path('<int:pk>/delete/', GoodsDeleteView.as_view(), name='goods_delete'),
]
