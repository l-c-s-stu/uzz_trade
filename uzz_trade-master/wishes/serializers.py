from rest_framework import serializers
from .models import Wish
from goods.serializers import GoodsSerializer

class WishSerializer(serializers.ModelSerializer):
    """想买序列化器"""
    goods = GoodsSerializer(read_only=True)
    goods_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Wish
        fields = ['id', 'user', 'goods', 'goods_id', 'created_at']
        read_only_fields = ['user', 'created_at']



