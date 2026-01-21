from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone

from .models import Order
from .serializers import OrderSerializer
from goods.models import Goods

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """订单视图集"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """只返回当前用户的订单"""
        return Order.objects.filter(user=self.request.user)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """创建订单（使用事务）"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 在 perform_create 中已经使用了事务，这里再次确保
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': '订单创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'], url_path='pay')
    def pay_order(self, request, pk=None):
        """支付订单（模拟支付）"""
        order = self.get_object()
        
        if order.pay_status != 'WAIT':
            return Response({
                'message': f'订单状态为{order.get_pay_status_display()}，无法支付'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查商品状态，确保商品仍然"在售"
        goods = order.goods
        if goods.status != 1:
            return Response({
                'message': f'商品状态为{goods.get_status_display()}，无法支付'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查该商品是否已有其他已支付的订单
        paid_orders = Order.objects.filter(
            goods=goods,
            pay_status='SUCCESS'
        ).exclude(id=order.id)
        
        if paid_orders.exists():
            return Response({
                'message': '该商品已被其他订单购买，无法支付'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 模拟支付：生成交易流水号
        trade_no = f"TRADE{int(timezone.now().timestamp())}{order.id}"
        
        with transaction.atomic():
            order.trade_no = trade_no
            order.pay_status = 'SUCCESS'
            order.pay_time = timezone.now()
            order.save()
            
            # 支付成功后，将商品状态改为"已出"
            goods.status = 2  # 已出
            goods.save()
            
            # 取消该商品的所有其他待支付订单（因为商品已售出）
            Order.objects.filter(
                goods=goods,
                pay_status='WAIT'
            ).exclude(id=order.id).update(pay_status='CANCEL')
        
        serializer = self.get_serializer(order)
        return Response({
            'message': '支付成功',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        """取消订单"""
        order = self.get_object()
        
        if order.pay_status == 'SUCCESS':
            return Response({
                'message': '已支付的订单无法取消'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if order.pay_status == 'CANCEL':
            return Response({
                'message': '订单已取消'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order.pay_status = 'CANCEL'
            order.save()
            
            # 取消订单后，检查该商品是否还有其他待支付的订单
            # 如果没有，确保商品状态为"在售"（如果之前被错误修改了）
            goods = order.goods
            has_pending_orders = Order.objects.filter(
                goods=goods,
                pay_status='WAIT'
            ).exclude(id=order.id).exists()
            
            # 如果没有其他待支付订单，且商品状态不是"在售"，恢复为"在售"
            if not has_pending_orders and goods.status != 1:
                goods.status = 1  # 恢复为"在售"
                goods.save()
        
        serializer = self.get_serializer(order)
        return Response({
            'message': '订单已取消',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

