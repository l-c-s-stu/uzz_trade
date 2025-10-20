from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'goods', 'content', 'created_at']
        read_only_fields = ['user', 'created_at', 'user_name', 'goods']  # ✅ 这里一定要加 goods
