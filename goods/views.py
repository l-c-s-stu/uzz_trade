from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Goods
from .serializers import GoodsSerializer
# Create your views here.

#商品创建
class GoodsListCreateView(generics.ListCreateAPIView):
    queryset = Goods.objects.all().order_by('-created_at')
    serializer_class = GoodsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#商品列表(所有商品)
class GoodsListView(generics.ListAPIView):
    queryset = Goods.objects.all().order_by('-created_at')
    serializer_class = GoodsSerializer
    permission_classes = [permissions.AllowAny]

#商品详情(单个商品)
class GoodsDetailView(generics.RetrieveAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permissions_classes = [permissions.AllowAny]