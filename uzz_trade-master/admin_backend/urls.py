from django.urls import path
from . import views

urlpatterns = [
    # 统计数据
    path('stats/', views.admin_stats, name='admin_stats'),
    
    # 用户管理
    path('users/', views.AdminUserListView.as_view(), name='admin_user_list'),
    path('users/<int:pk>/', views.AdminUserUpdateView.as_view(), name='admin_user_update'),
    
    # 商品管理
    path('goods/', views.AdminGoodsListView.as_view(), name='admin_goods_list'),
    path('goods/<int:pk>/', views.AdminGoodsUpdateView.as_view(), name='admin_goods_update'),
    path('goods/<int:pk>/delete/', views.AdminGoodsDeleteView.as_view(), name='admin_goods_delete'),
]



