# PowerShell 脚本：激活虚拟环境并启动服务器

Write-Host "正在激活虚拟环境..." -ForegroundColor Green

# 激活虚拟环境
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "虚拟环境已激活" -ForegroundColor Green
Write-Host ""

Write-Host "正在启动 Django 开发服务器..." -ForegroundColor Green
Write-Host ""

# 启动服务器
python manage.py runserver





