from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    student_id = serializers.CharField(max_length=20, required=True, allow_blank=False, 
                                       error_messages={'required': '学号不能为空'})
    college = serializers.CharField(max_length=50, required=True, allow_blank=False,
                                   error_messages={'required': '学院不能为空'})

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password', 'student_id', 'college')

    def validate_student_id(self, value):
        """验证学号格式：仅允许数字"""
        if value and not re.match(r'^\d+$', value):
            raise serializers.ValidationError("学号只能包含数字")
        return value

    def create(self,validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            phone=validated_data.get('phone',''),
            student_id=validated_data.get('student_id', ''),
            college=validated_data.get('college', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息序列化器（用于获取当前用户信息）"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'student_id', 'college', 'avatar', 
                 'date_joined', 'is_staff', 'is_superuser', 'is_active')
        read_only_fields = ('id', 'username', 'date_joined', 'is_staff', 'is_superuser', 'is_active')
