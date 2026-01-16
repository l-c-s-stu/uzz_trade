from django.contrib import admin
from .models import Wish

@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    """想买管理"""
    list_display = ['id', 'user', 'goods', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'goods__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
