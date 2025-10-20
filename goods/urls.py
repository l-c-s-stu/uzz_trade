from django.urls import path
from .views import GoodsListCreateView, GoodsDetailView

#"/api/goods/"->所有商品
#"/api/goods/1/"->id=1的商品详情
urlpatterns = [
    path('', GoodsListCreateView.as_view(), name='goods_list_create'),
    path('<int:pk>', GoodsDetailView.as_view(), name='goods_detail'),
]
