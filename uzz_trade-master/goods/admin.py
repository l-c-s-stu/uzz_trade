from django.contrib import admin
from .models import Goods

# Register your models here.

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'price', 'created_at']
    list_filter = ['created_at', 'owner']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        # 管理员可以看到所有商品
        return super().get_queryset(request)
