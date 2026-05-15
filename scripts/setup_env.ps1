# Environment Setup Guide (Windows PowerShell)

Write-Host "🚀 Setting up Python Environment for AI Agent Pro..." -ForegroundColor Cyan

# 1. Tạo môi trường ảo
if (-not (Test-Path -Path "venv")) {
    python -m venv venv
    Write-Host "✅ Created virtual environment (venv)." -ForegroundColor Green
}

# 2. Kích hoạt và cài đặt dependencies
Write-Host "📦 Installing dependencies from requirements.txt..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "`n✨ Setup Complete! To start development, run:" -ForegroundColor Cyan
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
