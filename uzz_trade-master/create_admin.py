#!/usr/bin/env python
"""
创建或查看管理员账户的脚本
"""
import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_trade.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def list_admin_users():
    """列出所有管理员账户"""
    admin_users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
    admin_users = admin_users.distinct()
    
    if admin_users.exists():
        print("\n=== 现有管理员账户 ===")
        for user in admin_users:
            print(f"\n用户名: {user.username}")
            print(f"  邮箱: {user.email or '(未设置)'}")
            print(f"  学号: {user.student_id or '(未设置)'}")
            print(f"  学院: {user.college or '(未设置)'}")
            print(f"  是否超级管理员: {'是' if user.is_superuser else '否'}")
            print(f"  是否员工: {'是' if user.is_staff else '否'}")
            print(f"  是否激活: {'是' if user.is_active else '否'}")
            print(f"  注册时间: {user.date_joined}")
    else:
        print("\n⚠️  没有找到管理员账户！")
        print("请使用以下命令创建管理员账户：")
        print("  python manage.py createsuperuser")
        return False
    
    return True

def create_admin_user():
    """创建管理员账户"""
    print("\n=== 创建管理员账户 ===")
    username = input("请输入用户名: ").strip()
    
    if User.objects.filter(username=username).exists():
        print(f"❌ 用户名 '{username}' 已存在！")
        return False
    
    email = input("请输入邮箱 (可选): ").strip() or ""
    phone = input("请输入手机号 (可选): ").strip() or ""
    student_id = input("请输入学号 (可选): ").strip() or ""
    college = input("请输入学院 (可选): ").strip() or ""
    
    password = input("请输入密码: ").strip()
    if not password:
        print("❌ 密码不能为空！")
        return False
    
    confirm_password = input("请再次输入密码: ").strip()
    if password != confirm_password:
        print("❌ 两次输入的密码不一致！")
        return False
    
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone if phone else None,
            student_id=student_id if student_id else None,
            college=college if college else None,
            is_staff=True,
            is_superuser=True
        )
        print(f"\n✅ 管理员账户 '{username}' 创建成功！")
        return True
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("管理员账户管理工具")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create':
        create_admin_user()
    else:
        has_admin = list_admin_users()
        if not has_admin:
            print("\n" + "=" * 50)
            choice = input("\n是否现在创建管理员账户？(y/n): ").strip().lower()
            if choice == 'y':
                create_admin_user()



