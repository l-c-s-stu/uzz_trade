from django.shortcuts import render
from pyexpat.errors import messages
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from goods.models import Goods
from .models import Wish
from .serializers import WishSerializer

# Create your views here.
class WishToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, goods_id):
        goods = get_object_or_404(Goods, id=goods_id)
        wish, created = Wish.objects.get_or_create(user=request.user, goods=goods)
        if created:
            return Response({'message': '已添加到想买列表'}, status=status.HTTP_201_CREATED)
        return Response({'message': '已经标记过了'}, status=status.HTTP_200_OK)

    def delete(self, request, goods_id):
        Wish.objects.filter(user=request.user, goods_id=goods_id).delete()
        return Response({'message': '已取消想买'}, status=status.HTTP_204_NO_CONTENT)

class WishListView(generics.ListAPIView):
    """获取当前用户的想买列表"""
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """只返回当前用户的想买记录"""
        return Wish.objects.filter(user=self.request.user).order_by('-created_at')