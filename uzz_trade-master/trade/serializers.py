from rest_framework import serializers
from .models import Order
from goods.models import Goods
from django.db import transaction
from django.utils import timezone

class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    goods_title = serializers.CharField(source='goods.title', read_only=True)
    goods_image = serializers.ImageField(source='goods.image', read_only=True)
    goods_price = serializers.DecimalField(source='goods.price', max_digits=10, 
                                          decimal_places=2, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    pay_status_display = serializers.CharField(source='get_pay_status_display', read_only=True)
    goods_id = serializers.IntegerField(write_only=True, required=True)
    order_mount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'goods', 'goods_id', 'goods_title', 
                 'goods_image', 'goods_price', 'order_sn', 'trade_no', 'pay_status', 
                 'pay_status_display', 'post_script', 'order_mount', 'pay_time', 'add_time']
        read_only_fields = ['order_sn', 'trade_no', 'pay_time', 'add_time', 'user', 'goods']
        # order_mount 不在 read_only_fields 中，因为需要在 validate 方法中设置
    
    def validate_goods_id(self, value):
        """验证商品是否存在且可购买"""
        try:
            goods = Goods.objects.get(id=value)
            # 检查商品状态是否为"在售"
            if goods.status != 1:
                raise serializers.ValidationError(f"商品状态为{goods.get_status_display()}，无法购买")
            return value
        except Goods.DoesNotExist:
            raise serializers.ValidationError("商品不存在")
    
    def validate(self, attrs):
        """验证订单金额"""
        goods_id = attrs.get('goods_id')
        if goods_id:
            try:
                goods = Goods.objects.get(id=goods_id)
                # 自动设置订单金额为商品价格
                attrs['order_mount'] = goods.price
            except Goods.DoesNotExist:
                pass
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """创建订单（使用事务保证数据一致性）"""
        goods_id = validated_data.pop('goods_id')
        goods = Goods.objects.select_for_update().get(id=goods_id)  # 使用行锁
        
        # 再次检查商品状态（防止并发问题）
        if goods.status != 1:
            raise serializers.ValidationError(f"商品状态为{goods.get_status_display()}，无法购买")
        
        # 检查该商品是否已有待支付的订单（防止重复购买）
        existing_order = Order.objects.filter(
            goods=goods,
            pay_status='WAIT'  # 待支付状态
        ).first()
        
        if existing_order:
            raise serializers.ValidationError(
                f"该商品已有待支付的订单（订单号：{existing_order.order_sn}），请先支付或取消该订单后再购买"
            )
        
        # 创建订单
        order = Order.objects.create(
            user=self.context['request'].user,
            goods=goods,
            order_mount=validated_data.get('order_mount', goods.price),
            post_script=validated_data.get('post_script', ''),
            pay_status='WAIT'
        )
        
        # 注意：创建订单时不修改商品状态，保持"在售"状态
        # 只有在支付成功后才将商品状态改为"已出"
        # 这样可以防止用户创建多个订单而不支付
        
        return order



