from django.contrib import admin
from .models import Goods, Category, GoodsImage

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """商品分类管理"""
    list_display = ['id', 'name', 'code', 'parent', 'get_sub_count']
    list_filter = ['parent']
    search_fields = ['name', 'code']
    ordering = ['id']
    
    def get_sub_count(self, obj):
        """显示子分类数量"""
        return obj.sub_cat.count()
    get_sub_count.short_description = '子分类数'

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    """商品管理"""
    list_display = ['id', 'goods_sn', 'title', 'owner', 'category', 'price', 'status', 'wish_count_display', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'owner']
    search_fields = ['title', 'description', 'goods_sn', 'owner__username']
    readonly_fields = ['goods_sn', 'created_at']
    ordering = ['-created_at']
    list_editable = ['status']  # 允许直接在列表页修改状态
    
    fieldsets = (
        ('基本信息', {
            'fields': ('owner', 'category', 'goods_sn', 'title', 'description')
        }),
        ('价格与图片', {
            'fields': ('price', 'image', 'status')
        }),
        ('时间信息', {
            'fields': ('created_at',)
        }),
    )
    
    def wish_count_display(self, obj):
        """显示想买人数"""
        from wishes.models import Wish
        return Wish.objects.filter(goods=obj).count()
    wish_count_display.short_description = '想买人数'
    
    def get_queryset(self, request):
        # 管理员可以看到所有商品
        return super().get_queryset(request)

@admin.register(GoodsImage)
class GoodsImageAdmin(admin.ModelAdmin):
    """商品图片管理"""
    list_display = ['id', 'goods', 'image', 'add_time']
    list_filter = ['add_time']
    search_fields = ['goods__title']
    ordering = ['-add_time']
