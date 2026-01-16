from django.db import models
from django.conf import settings
from goods.models import Goods
import uuid
from datetime import datetime

# Create your models here.

class Order(models.Model):
    """订单模型"""
    PAY_STATUS_CHOICES = (
        ('WAIT', '待支付'),
        ('SUCCESS', '已支付'),
        ('CANCEL', '已取消'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='orders', verbose_name="买家")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='orders', 
                             verbose_name="商品")
    order_sn = models.CharField(max_length=50, unique=True, verbose_name="订单号")
    trade_no = models.CharField(max_length=100, null=True, blank=True, 
                               verbose_name="支付流水号")
    pay_status = models.CharField(max_length=10, choices=PAY_STATUS_CHOICES, 
                                 default='WAIT', verbose_name="支付状态")
    post_script = models.TextField(max_length=200, blank=True, null=True, 
                                  verbose_name="订单留言")
    order_mount = models.DecimalField(max_digits=10, decimal_places=2, 
                                     verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ['-add_time']
    
    def __str__(self):
        return f"订单{self.order_sn} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        """自动生成订单号"""
        if not self.order_sn:
            # 格式：当前时间戳(10位) + 用户ID + 随机UUID前8位
            timestamp = str(int(datetime.now().timestamp()))
            user_id = str(self.user.id) if self.user else '0'
            uuid_part = str(uuid.uuid4())[:8].replace('-', '')
            self.order_sn = f"{timestamp}{user_id.zfill(3)}{uuid_part}"
        super().save(*args, **kwargs)
