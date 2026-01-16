from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['id', 'username', 'email', 'student_id', 'college', 'phone', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'college', 'date_joined']
    search_fields = ['username', 'email', 'student_id', 'college', 'phone']
    ordering = ['-date_joined']
    
    # 在用户编辑页面添加自定义字段
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('phone', 'avatar', 'student_id', 'college')}),
    )
    
    # 在用户创建页面添加自定义字段
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('phone', 'avatar', 'student_id', 'college')}),
    )
