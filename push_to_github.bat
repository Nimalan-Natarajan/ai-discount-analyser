@echo off
echo 🚀 AI-Discount-Analyser - GitHub Push Helper
echo ============================================
echo.

echo Checking current directory...
echo Current directory: %CD%
echo.

echo Checking if git is initialized...
if not exist ".git" (
    echo Initializing git repository...
    git init
    git config user.name "NimalanNatarajan"
    git config user.email "nimalan94@gmail.com"
    echo Git repository initialized!
) else (
    echo Git repository already exists
)

echo Checking git status...
git status
echo.

echo Checking if remote exists...
git remote -v
echo.

echo Adding all files to git...
git add .
echo.

echo Committing changes...
git commit -m "Deploy AI-Driven Discount Analyser Tool"
echo.

echo Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/Nimalan-Natarajan/ai-discount-analyser.git
echo.

echo Verifying remote...
git remote -v
echo.

echo Setting main branch...
git branch -M main
echo.

echo Pushing to GitHub...
echo This may ask for your GitHub credentials...
git push -u origin main --force
echo.

if %errorlevel% == 0 (
    echo ✅ SUCCESS! Your code is now on GitHub!
    echo.
    echo 🌐 Repository URL: https://github.com/Nimalan-Natarajan/ai-discount-analyser
    echo.
    echo 📋 Next steps:
    echo 1. Go to https://share.streamlit.io
    echo 2. Sign in with GitHub
    echo 3. Click "New app"
    echo 4. Repository: Nimalan-Natarajan/ai-discount-analyser
    echo 5. Main file: src/app.py
    echo 6. Click Deploy!
    echo.
    echo Your app will be live at: https://your-app-name.streamlit.app
) else (
    echo.
    echo ❌ Push failed. Common solutions:
    echo 1. Make sure you're signed in to GitHub
    echo 2. Check if the repository exists
    echo 3. Verify you have write access
    echo.
    echo Try running: git push -u origin main
)

echo.
pause
