from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# 缓存功能已集成到视图方法中，无需额外导入

from .models import Goods, Category, GoodsImage
from .serializers import GoodsSerializer, CategorySerializer, GoodsImageSerializer

# 自定义权限类：只有商品发布者或管理员可以删除
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 超级管理员可以删除任何商品
        if request.user.is_superuser:
            return True
        # 商品发布者可以删除自己的商品
        return obj.owner == request.user

# Create your views here.

#商品列表和创建（合并视图，支持缓存）
class GoodsListCreateView(generics.ListCreateAPIView):
    queryset = Goods.objects.all().order_by('-created_at')
    serializer_class = GoodsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """列表查询（已缓存）"""
        from django.core.cache import cache
        import hashlib
        
        # 生成缓存键
        query_string = request.GET.urlencode()
        cache_key = f'goods_list_{hashlib.md5(query_string.encode()).hexdigest()}'
        
        # 尝试从缓存获取
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)
        
        # 获取数据
        response = super().list(request, *args, **kwargs)
        
        # 缓存响应数据（60秒）
        if response.status_code == 200:
            cache.set(cache_key, response.data, 60)
        
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
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

# 分类相关视图
class CategoryListView(generics.ListAPIView):
    """获取所有分类（支持多级）"""
    queryset = Category.objects.filter(parent=None)  # 只获取顶级分类
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        """列表查询（已缓存5分钟）"""
        from django.core.cache import cache
        
        # 生成缓存键
        cache_key = 'category_list_all'
        
        # 尝试从缓存获取
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)
        
        # 获取数据
        response = super().list(request, *args, **kwargs)
        
        # 缓存响应数据（5分钟 = 300秒）
        if response.status_code == 200:
            cache.set(cache_key, response.data, 300)
        
        return response

# 商品图片相关视图
class GoodsImageCreateView(generics.CreateAPIView):
    """为商品添加图片"""
    queryset = GoodsImage.objects.all()
    serializer_class = GoodsImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        goods_id = self.kwargs.get('goods_id')
        goods = get_object_or_404(Goods, id=goods_id)
        # 验证用户是否有权限（只有商品所有者或管理员可以添加图片）
        if not (self.request.user.is_superuser or goods.owner == self.request.user):
            raise permissions.PermissionDenied("您没有权限为此商品添加图片")
        serializer.save(goods=goods)

class GoodsImageDeleteView(generics.DestroyAPIView):
    """删除商品图片"""
    queryset = GoodsImage.objects.all()
    serializer_class = GoodsImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        image = get_object_or_404(GoodsImage, id=self.kwargs.get('image_id'))
        # 验证用户是否有权限
        if not (self.request.user.is_superuser or image.goods.owner == self.request.user):
            raise permissions.PermissionDenied("您没有权限删除此图片")
        return image