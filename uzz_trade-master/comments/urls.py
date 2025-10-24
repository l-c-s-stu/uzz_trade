from django.urls import path
from .views import CommentListCreateView

urlpatterns = [
    path('goods/<int:goods_id>/comments/', CommentListCreateView.as_view(), name='goods-comments'),
]