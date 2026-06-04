# Quick start script for Banking Application
# This script starts both backend and frontend servers

Write-Host "🏦 Banking Management System - Quick Start" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is in use
function Test-Port {
    param($port)
    $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

# Check if ports are available
Write-Host "Checking ports..." -ForegroundColor Yellow
if (Test-Port 5000) {
    Write-Host "⚠️  Port 5000 (Backend) is already in use" -ForegroundColor Red
}
else {
    Write-Host "✓ Port 5000 available" -ForegroundColor Green
}

if (Test-Port 3000) {
    Write-Host "⚠️  Port 3000 (Frontend) is already in use" -ForegroundColor Red
}
else {
    Write-Host "✓ Port 3000 available" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start Backend
Write-Host "1️⃣  Starting Backend (Flask)..." -ForegroundColor Cyan
$backendPath = "$PSScriptRoot\BankAPI"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python app.py" -WindowTitle "Banking API - Backend (Port 5000)"

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Start Frontend
Write-Host "2️⃣  Starting Frontend (React)..." -ForegroundColor Cyan
$frontendPath = "$PSScriptRoot\frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev" -WindowTitle "Banking App - Frontend (Port 3000)"

Write-Host ""
Write-Host "🚀 Both services starting..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Backend will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "   - API Docs: http://localhost:5000/apidocs" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend will be available at: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "⏳ Please wait 10-15 seconds for both servers to fully start..." -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Check terminal windows for any errors" -ForegroundColor Yellow
Write-Host "   - If ports are in use, stop other services and try again" -ForegroundColor Yellow
Write-Host "   - Both windows will stay open for monitoring" -ForegroundColor Yellow
Write-Host ""
Write-Host "Happy Banking! 🏦" -ForegroundColor Cyan
