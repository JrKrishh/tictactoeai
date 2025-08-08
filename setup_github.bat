@echo off
echo 🚀 GitHub Repository Setup Script
echo ================================

set /p username="Enter your GitHub username: "

echo.
echo Setting up remote repository...
git remote add origin https://github.com/%username%/ai-tictactoe-challenge.git

echo.
echo Checking remote configuration...
git remote -v

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Upload complete!
echo 🌐 Your repository: https://github.com/%username%/ai-tictactoe-challenge
echo 🎮 Live demo: https://tictactoe-pzcsxkg59-yangs-projects-33bbed0c.vercel.app

pause