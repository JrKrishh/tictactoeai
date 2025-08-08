# GitHub Repository Setup Script
Write-Host "🚀 GitHub Repository Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$username = Read-Host "Enter your GitHub username"

Write-Host "`nSetting up remote repository..." -ForegroundColor Yellow
git remote add origin "https://github.com/$username/ai-tictactoe-challenge.git"

Write-Host "`nChecking remote configuration..." -ForegroundColor Yellow
git remote -v

Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host "`n✅ Upload complete!" -ForegroundColor Green
Write-Host "🌐 Your repository: https://github.com/$username/ai-tictactoe-challenge" -ForegroundColor Green
Write-Host "🎮 Live demo: https://tictactoe-pzcsxkg59-yangs-projects-33bbed0c.vercel.app" -ForegroundColor Green

Read-Host "`nPress Enter to continue..."