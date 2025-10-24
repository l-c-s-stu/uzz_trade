from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Goods
from .serializers import GoodsSerializer

# 自定义权限类：只有商品发布者或管理员可以删除
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 超级管理员可以删除任何商品
        if request.user.is_superuser:
            return True
        # 商品发布者可以删除自己的商品
        return obj.owner == request.user

# Create your views here.

#商品创建
class GoodsListCreateView(generics.ListCreateAPIView):
    queryset = Goods.objects.all().order_by('-created_at')
    serializer_class = GoodsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

#商品列表(所有商品)
class GoodsListView(generics.ListAPIView):
    queryset = Goods.objects.all().order_by('-created_at')
    serializer_class = GoodsSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

#商品详情(单个商品)
class GoodsDetailView(generics.RetrieveAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

#商品修改
class GoodsUpdateView(generics.UpdateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': '商品修改成功', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

#商品删除
class GoodsDeleteView(generics.DestroyAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': '商品删除成功'}, status=status.HTTP_200_OK)