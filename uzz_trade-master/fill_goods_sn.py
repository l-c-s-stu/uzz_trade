#!/usr/bin/env python
"""填充现有商品的 goods_sn 字段"""
import os
import django
import sys

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from goods.models import Goods
from datetime import datetime
import uuid

def fill_goods_sn():
    """为所有没有 goods_sn 的商品生成货号"""
    goods_list = Goods.objects.filter(goods_sn__isnull=True)
    count = 0
    
    for goods in goods_list:
        timestamp = str(int(datetime.now().timestamp()))
        user_id = str(goods.owner.id) if goods.owner else '0'
        uuid_part = str(uuid.uuid4())[:8].replace('-', '')
        goods.goods_sn = f"{timestamp}{user_id.zfill(3)}{uuid_part}"
        goods.save()
        count += 1
    
    print(f'Success: Generated goods_sn for {count} goods')
    return count

if __name__ == '__main__':
    fill_goods_sn()

