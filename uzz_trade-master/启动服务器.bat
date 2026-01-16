@echo off
REM 激活虚拟环境并启动 Django 服务器

echo 正在激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo 虚拟环境已激活
echo.

echo 正在启动 Django 开发服务器...
python manage.py runserver

pause

