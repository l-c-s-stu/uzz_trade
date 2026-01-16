from rest_framework import serializers
from .models import Goods, Category, GoodsImage
from wishes.models import Wish

class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    sub_cat = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'parent', 'sub_cat']
    
    def get_sub_cat(self, obj):
        """获取子分类"""
        sub_categories = obj.sub_cat.all()
        if sub_categories.exists():
            return CategorySerializer(sub_categories, many=True).data
        return []

class GoodsImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""
    
    class Meta:
        model = GoodsImage
        fields = ['id', 'image', 'add_time']

class GoodsSerializer(serializers.ModelSerializer):
    wish_count = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    is_owner = serializers.SerializerMethodField()
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    images = GoodsImageSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Goods
        fields = ['id', 'owner', 'owner_name', 'category', 'category_id', 'goods_sn', 
                  'title', 'description', 'price', 'image', 'status', 'status_display',
                  'created_at', 'wish_count', 'is_owner', 'images']

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
    
    def create(self, validated_data):
        """创建商品时处理分类"""
        category_id = validated_data.pop('category_id', None)
        goods = Goods.objects.create(**validated_data)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                goods.category = category
                goods.save()
            except Category.DoesNotExist:
                pass
        return goods
    
    def update(self, instance, validated_data):
        """更新商品时处理分类"""
        category_id = validated_data.pop('category_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if category_id is not None:
            try:
                category = Category.objects.get(id=category_id)
                instance.category = category
            except Category.DoesNotExist:
                instance.category = None
        instance.save()
        return instance