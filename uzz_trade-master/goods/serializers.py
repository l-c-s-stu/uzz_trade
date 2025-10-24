from rest_framework import serializers
from .models import Goods
from wishes.models import Wish

class GoodsSerializer(serializers.ModelSerializer):
    wish_count = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    is_owner = serializers.SerializerMethodField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Goods
        fields = ['id','owner','owner_name','title','description','price','image','created_at','wish_count','is_owner']

    def get_wish_count(self, obj):
        #统计该商品被多少人标记为"想买"
        return Wish.objects.filter(goods=obj).count()
    
    def get_is_owner(self, obj):
        # 检查当前用户是否是商品发布者或管理员
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # 管理员可以删除任何商品
            if request.user.is_superuser:
                return True
            # 商品发布者可以删除自己的商品
            return obj.owner == request.user
        return False