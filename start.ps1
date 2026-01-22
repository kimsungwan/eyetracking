# KoreanSaaS 시작 스크립트
# 프론트엔드 (Next.js)와 백엔드 (FastAPI)를 동시에 실행합니다.
# Docker는 별도로 실행해야 합니다.

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  KoreanSaaS 서비스 시작" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = $PSScriptRoot

# 백엔드 (FastAPI AI Service) 시작
Write-Host "[1/2] AI 백엔드 서비스 시작 중..." -ForegroundColor Yellow
$backendPath = Join-Path $projectRoot "apps\ai-service"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host 'AI Backend (FastAPI) - http://localhost:8000' -ForegroundColor Green; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# 잠시 대기 (백엔드가 먼저 시작되도록)
Start-Sleep -Seconds 2

# 프론트엔드 (Next.js) 시작
Write-Host "[2/2] 프론트엔드 서비스 시작 중..." -ForegroundColor Yellow
$frontendPath = Join-Path $projectRoot "apps\client"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Frontend (Next.js) - http://localhost:3000' -ForegroundColor Green; pnpm dev"

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  모든 서비스가 시작되었습니다!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "  프론트엔드: http://localhost:3000" -ForegroundColor White
Write-Host "  백엔드:     http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "  종료하려면 각 PowerShell 창을 닫으세요." -ForegroundColor Gray
    