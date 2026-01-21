from rest_framework import filters
from django_filters import rest_framework as django_filters
from .models import Goods

class GoodsFilter(django_filters.FilterSet):
    """商品筛选器"""
    category = django_filters.NumberFilter(field_name='category__id', lookup_expr='exact')
    category_code = django_filters.CharFilter(field_name='category__code', lookup_expr='exact')
    status = django_filters.NumberFilter(field_name='status', lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    owner = django_filters.NumberFilter(field_name='owner__id', lookup_expr='exact')
    
    class Meta:
        model = Goods
        fields = ['category', 'category_code', 'status', 'min_price', 'max_price', 'title', 'owner']



