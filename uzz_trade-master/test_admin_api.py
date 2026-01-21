#!/usr/bin/env python
"""
测试管理后台 API
"""
import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from django.contrib.auth import get_user_model
from goods.models import Goods
from trade.models import Order
from wishes.models import Wish

User = get_user_model()

print("=" * 50)
print("管理后台统计数据测试")
print("=" * 50)

# 统计各模型数量
total_users = User.objects.count()
total_goods = Goods.objects.count()
total_orders = Order.objects.count()
total_wishes = Wish.objects.count()

print(f"\n总用户数: {total_users}")
print(f"总商品数: {total_goods}")
print(f"总订单数: {total_orders}")
print(f"想买总数: {total_wishes}")

# 检查管理员账户
admin_users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
admin_users = admin_users.distinct()

print(f"\n管理员账户数量: {admin_users.count()}")
if admin_users.exists():
    print("\n管理员账户列表:")
    for user in admin_users:
        print(f"  - {user.username} (is_staff={user.is_staff}, is_superuser={user.is_superuser})")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)



