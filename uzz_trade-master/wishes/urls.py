from django.urls import path
from .views import WishToggleView, WishListView

urlpatterns = [
    path('goods/<int:goods_id>/wish/', WishToggleView.as_view(), name='wish-toggle'),
    path('wishes/', WishListView.as_view(), name='wish-list'),  # 获取当前用户的想买列表
]