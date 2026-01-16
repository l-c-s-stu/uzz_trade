from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """评论管理"""
    list_display = ['id', 'user', 'goods', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username', 'goods__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        """内容预览（截取前50个字符）"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容'
