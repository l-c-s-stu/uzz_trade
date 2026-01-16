from django.db import models
from django.conf import settings
import uuid
from datetime import datetime

# Create your models here.

class Category(models.Model):
    """商品分类模型 - 支持多级分类"""
    name = models.CharField(max_length=50, verbose_name="分类名称")
    code = models.CharField(max_length=20, unique=True, verbose_name="分类编码")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, 
                               related_name='sub_cat', verbose_name="父类级别")
    
    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
    
    def __str__(self):
        return self.name

class Goods(models.Model):
    STATUS_CHOICES = (
        (1, '在售'),
        (2, '已出'),
        (3, '下架'),
    )
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goods')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='goods', verbose_name="商品分类")
    goods_sn = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="商品唯一货号")
    title = models.CharField(max_length=100, verbose_name="商品标题")
    description = models.TextField(verbose_name="商品描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")
    image = models.ImageField(upload_to='goods_image', null=True, blank=True, verbose_name="主图")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="商品状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """自动生成商品唯一货号"""
        if not self.goods_sn:
            # 格式：当前时间戳(10位) + 用户ID + 随机UUID前8位
            timestamp = str(int(datetime.now().timestamp()))
            user_id = str(self.owner.id) if self.owner else '0'
            uuid_part = str(uuid.uuid4())[:8].replace('-', '')
            self.goods_sn = f"{timestamp}{user_id.zfill(3)}{uuid_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class GoodsImage(models.Model):
    """商品图片模型 - 支持一个商品多张详情图"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images', verbose_name="商品")
    image = models.ImageField(upload_to='goods_image/detail', verbose_name="商品图片")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    
    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
        ordering = ['add_time']
    
    def __str__(self):
        return f"{self.goods.title} - 图片"