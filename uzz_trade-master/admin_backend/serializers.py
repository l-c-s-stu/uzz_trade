from rest_framework import serializers
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """管理员用户序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'student_id', 'college', 
                 'is_active', 'is_staff', 'is_superuser', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')


class AdminGoodsSerializer(serializers.ModelSerializer):
    """管理员商品序列化器"""
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Goods
        fields = ('id', 'title', 'description', 'price', 'image', 'status', 'status_display',
                 'owner', 'owner_name', 'category', 'category_name', 'created_at')
        read_only_fields = ('id', 'owner', 'created_at')

