from django.contrib.auth.views import LoginView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),#登录接口
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #刷新 token
    path('profile/', UserProfileView.as_view(), name='user-profile'), #获取当前用户信息
]

