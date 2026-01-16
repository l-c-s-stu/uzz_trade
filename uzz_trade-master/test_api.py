#!/usr/bin/env python
"""测试 API 接口"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from goods.models import Category, Goods
import json

User = get_user_model()
client = Client()

def test_models():
    """测试模型"""
    print("\n=== 测试模型 ===")
    
    # 测试用户模型
    user_count = User.objects.count()
    print(f"用户数量: {user_count}")
    
    # 测试分类模型
    category_count = Category.objects.count()
    print(f"分类数量: {category_count}")
    
    # 测试商品模型
    goods_count = Goods.objects.count()
    print(f"商品数量: {goods_count}")
    
    # 测试商品货号
    goods_with_sn = Goods.objects.exclude(goods_sn__isnull=True).count()
    print(f"有货号的商品: {goods_with_sn}/{goods_count}")
    
    return True

def test_api_endpoints():
    """测试 API 端点"""
    print("\n=== 测试 API 端点 ===")
    
    # 测试商品列表
    try:
        response = client.get('/api/goods/')
        print(f"GET /api/goods/ - Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"  返回商品数量: {len(data) if isinstance(data, list) else 'N/A'}")
    except Exception as e:
        print(f"  错误: {e}")
    
    # 测试分类列表
    try:
        response = client.get('/api/goods/categories/')
        print(f"GET /api/goods/categories/ - Status: {response.status_code}")
    except Exception as e:
        print(f"  错误: {e}")
    
    return True

if __name__ == '__main__':
    print("开始测试...")
    test_models()
    test_api_endpoints()
    print("\n测试完成!")

