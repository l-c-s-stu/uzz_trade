from django.urls import path
from .views import WishToggleView

urlpatterns = [
    path('goods/<int:goods_id>/wish/', WishToggleView.as_view(), name='wish-toggle'),
]