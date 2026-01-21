# 安装脚本 - 解决权限问题
Write-Host "设置本地 npm 缓存..." -ForegroundColor Green
npm config set cache ".\node_cache" --location=project

Write-Host "开始安装依赖..." -ForegroundColor Green
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n安装成功！" -ForegroundColor Cyan
    Write-Host "现在可以运行: npm run dev" -ForegroundColor Yellow
} else {
    Write-Host "`n安装失败，请尝试以管理员身份运行" -ForegroundColor Red
}



