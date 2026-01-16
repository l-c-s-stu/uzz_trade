#!/usr/bin/env python
"""测试服务器启动"""
import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')

try:
    django.setup()
    print("Django environment setup success")
    
    # 测试导入
    from goods.views import GoodsListCreateView
    print("Views import success")
    
    from goods.models import Goods, Category
    print("Models import success")
    
    from goods.serializers import GoodsSerializer
    print("Serializers import success")
    
    print("\nAll imports test passed, server should start normally")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

