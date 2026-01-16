from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理"""
    list_display = ['id', 'order_sn', 'user', 'goods', 'order_mount', 'pay_status', 'pay_time', 'add_time']
    list_filter = ['pay_status', 'add_time', 'pay_time']
    search_fields = ['order_sn', 'trade_no', 'user__username', 'goods__title']
    readonly_fields = ['order_sn', 'trade_no', 'add_time', 'pay_time']
    ordering = ['-add_time']
    list_editable = ['pay_status']  # 允许直接在列表页修改支付状态
    
    fieldsets = (
        ('订单信息', {
            'fields': ('order_sn', 'user', 'goods', 'order_mount')
        }),
        ('支付信息', {
            'fields': ('pay_status', 'trade_no', 'pay_time')
        }),
        ('其他信息', {
            'fields': ('post_script', 'add_time')
        }),
    )
    
    def get_queryset(self, request):
        # 管理员可以看到所有订单
        return super().get_queryset(request)
