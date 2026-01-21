from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from goods.models import Goods
from trade.models import Order
from wishes.models import Wish
from .serializers import AdminUserSerializer, AdminGoodsSerializer

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    """检查用户是否为管理员"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """获取管理后台统计数据"""
    stats = {
        'total_users': User.objects.count(),
        'total_goods': Goods.objects.count(),
        'total_orders': Order.objects.count(),
        'total_wishes': Wish.objects.count(),
    }
    return Response(stats)


class AdminUserListView(generics.ListAPIView):
    """管理员用户列表视图"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username', 'email', 'student_id', 'college', 'phone']


class AdminUserUpdateView(generics.UpdateAPIView):
    """管理员更新用户状态"""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    
    def partial_update(self, request, *args, **kwargs):
        """支持 PATCH 方法部分更新"""
        instance = self.get_object()
        # 只允许更新 is_active 字段
        is_active = request.data.get('is_active')
        if is_active is not None:
            instance.is_active = bool(is_active)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                'message': '用户状态已更新',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'error': '请提供 is_active 字段'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """支持 PUT 方法"""
        return self.partial_update(request, *args, **kwargs)


class AdminGoodsListView(generics.ListAPIView):
    """管理员商品列表视图"""
    queryset = Goods.objects.all().order_by('-created_at')
    serializer_class = AdminGoodsSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        """支持按状态筛选"""
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=int(status))
        return queryset


class AdminGoodsUpdateView(generics.UpdateAPIView):
    """管理员更新商品状态"""
    queryset = Goods.objects.all()
    serializer_class = AdminGoodsSerializer
    permission_classes = [IsAdminUser]
    
    def partial_update(self, request, *args, **kwargs):
        """支持 PATCH 方法部分更新"""
        instance = self.get_object()
        # 只允许更新 status 字段
        status_value = request.data.get('status')
        if status_value is not None:
            instance.status = int(status_value)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response({
                'message': '商品状态已更新',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'error': '请提供 status 字段'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """支持 PUT 方法"""
        return self.partial_update(request, *args, **kwargs)


class AdminGoodsDeleteView(generics.DestroyAPIView):
    """管理员删除商品"""
    queryset = Goods.objects.all()
    serializer_class = AdminGoodsSerializer
    permission_classes = [IsAdminUser]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '商品已删除'
        }, status=status.HTTP_200_OK)
