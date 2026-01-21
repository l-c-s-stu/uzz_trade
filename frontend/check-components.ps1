# Component Check Script
Write-Host "Checking component files..." -ForegroundColor Green
Write-Host ""

$components = @(
    "src\components\Register.vue",
    "src\components\Login.vue",
    "src\components\GoodsList.vue",
    "src\utils\api.js"
)

$allExist = $true
foreach ($file in $components) {
    if (Test-Path $file) {
        Write-Host "[OK] $file exists" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $file NOT found" -ForegroundColor Red
        $allExist = $false
    }
}

Write-Host ""
Write-Host "Checking imports..." -ForegroundColor Green
Write-Host ""

# Check Register.vue
$register = Get-Content "src\components\Register.vue" -Raw -ErrorAction SilentlyContinue
if ($register -match "authAPI") {
    Write-Host "[OK] Register.vue uses authAPI" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Register.vue does NOT use authAPI" -ForegroundColor Red
    $allExist = $false
}

# Check Login.vue
$login = Get-Content "src\components\Login.vue" -Raw -ErrorAction SilentlyContinue
if ($login -match "authAPI") {
    Write-Host "[OK] Login.vue uses authAPI" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Login.vue does NOT use authAPI" -ForegroundColor Red
    $allExist = $false
}

# Check GoodsList.vue
$goodsList = Get-Content "src\components\GoodsList.vue" -Raw -ErrorAction SilentlyContinue
if ($goodsList -match "goodsAPI") {
    Write-Host "[OK] GoodsList.vue uses goodsAPI" -ForegroundColor Green
} else {
    Write-Host "[FAIL] GoodsList.vue does NOT use goodsAPI" -ForegroundColor Red
    $allExist = $false
}

if ($goodsList -match "authAPI") {
    Write-Host "[OK] GoodsList.vue uses authAPI" -ForegroundColor Green
} else {
    Write-Host "[WARN] GoodsList.vue does NOT use authAPI" -ForegroundColor Yellow
}

Write-Host ""
if ($allExist) {
    Write-Host "All checks passed!" -ForegroundColor Cyan
} else {
    Write-Host "Some checks failed. Please review the errors above." -ForegroundColor Red
}





