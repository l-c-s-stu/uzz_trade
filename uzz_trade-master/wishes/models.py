from django.db import models
from django.conf import settings
from goods.models import Goods
# Create your models here.
class Wish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishes')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='wishes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'goods')

    def __str__(self):
        return f"{self.user.username} 想买 {self.goods.title}"