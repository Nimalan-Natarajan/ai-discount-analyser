@echo off
echo 🚀 GitHub Repository Setup Helper
echo.
echo This script will help you push your code to GitHub and deploy it.
echo.
echo =====================================
echo Step 1: Create GitHub Repository
echo =====================================
echo 1. Go to https://github.com and log in
echo 2. Click "+" button -^> "New repository"  
echo 3. Name: ai-discount-analyser (or your choice)
echo 4. Set to PUBLIC (required for free Streamlit deployment)
echo 5. DON'T initialize with README/gitignore (we have them)
echo 6. Click "Create repository"
echo.
pause
echo.
echo =====================================
echo Step 2: Get Your GitHub Repository URL
echo =====================================
echo After creating the repository, GitHub will show you a URL like:
echo https://github.com/YOUR_USERNAME/ai-discount-analyser.git
echo.
set /p GITHUB_URL="Enter your GitHub repository URL: "
echo.
echo =====================================
echo Step 3: Push Code to GitHub
echo =====================================
echo Running git commands...
echo.

REM Add remote origin
git remote add origin %GITHUB_URL%
if %errorlevel% neq 0 (
    echo Updating existing remote...
    git remote set-url origin %GITHUB_URL%
)

REM Rename branch to main
git branch -M main

REM Add the new deployment guide to git
git add GITHUB_DEPLOYMENT.md
git commit -m "Add GitHub deployment guide"

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% == 0 (
    echo.
    echo ✅ SUCCESS! Your code is now on GitHub!
    echo.
    echo =====================================
    echo Step 4: Deploy on Streamlit Cloud
    echo =====================================
    echo 1. Go to https://share.streamlit.io
    echo 2. Sign in with your GitHub account
    echo 3. Click "New app"
    echo 4. Select your repository: ai-discount-analyser
    echo 5. Main file path: src/app.py
    echo 6. Click "Deploy!"
    echo.
    echo Your app will be live at:
    echo https://your-app-name.streamlit.app
    echo.
    echo 🎉 No API keys needed in deployment!
    echo Users enter their own Gemini API keys in the app.
    echo.
) else (
    echo.
    echo ❌ Error pushing to GitHub. Please check:
    echo 1. Repository URL is correct
    echo 2. You have write access to the repository
    echo 3. Your GitHub credentials are set up
    echo.
)

echo See GITHUB_DEPLOYMENT.md for detailed instructions.
pause
