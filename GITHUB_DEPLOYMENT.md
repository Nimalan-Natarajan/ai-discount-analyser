# 🚀 GitHub & Deployment Setup Guide

## Step 1: Create GitHub Repository

1. **Go to GitHub**: Visit [github.com](https://github.com) and log in
2. **Create New Repository**:
   - Click the "+" button → "New repository"
   - Repository name: `ai-discount-analyser` (or your preferred name)
   - Description: "AI-Driven Discount Analyser Tool for logistics quotations"
   - Set to **Public** (required for free Streamlit deployment)
   - **DON'T** initialize with README, .gitignore, or license (we have them already)
   - Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the GitHub repository, run these commands in your terminal:

```bash
# Add your GitHub repository as remote (replace with your actual GitHub username/repo)
git remote add origin https://github.com/YOUR_USERNAME/ai-discount-analyser.git

# Rename main branch to match GitHub's default
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Example with actual commands (update with your GitHub username):**
```bash
git remote add origin https://github.com/NimalanNatarajan/ai-discount-analyser.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Streamlit Community Cloud

### 3.1 Access Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 3.2 Deploy Your App
1. Click **"New app"**
2. **Repository**: Select `your-username/ai-discount-analyser`
3. **Branch**: `main`
4. **Main file path**: `src/app.py`
5. **App URL**: Choose a custom URL like `ai-discount-analyser` or use auto-generated
6. Click **"Deploy!"**

### 3.3 Wait for Deployment
- Deployment typically takes 2-5 minutes
- You'll see the build logs in real-time
- Once complete, you'll get a URL like: `https://ai-discount-analyser.streamlit.app`

## Step 4: Test Your Deployed App

1. **Visit your app URL**
2. **Test the workflow**:
   - Go to "Data Upload" and upload a sample CSV
   - Navigate to "Static Predictions" 
   - Test the historical analysis feature
   - Go to "Settings" and verify API key input works
   - Test "AI Predictions" with a valid Gemini API key

## Step 5: Share Your App

Your app is now live! Share the URL with users:
- **App URL**: `https://your-app-name.streamlit.app`
- Users need to bring their own Gemini API keys
- The Static Predictions page works without any API key

## 🎉 Success Checklist

- [ ] GitHub repository created and code pushed
- [ ] Streamlit Community Cloud deployment successful
- [ ] App loads without errors
- [ ] Data upload functionality works
- [ ] Static predictions work (no API key needed)
- [ ] Settings page allows API key input
- [ ] AI predictions work when API key is provided

## 🔧 Troubleshooting

### Common Issues:

**Build fails on Streamlit Cloud:**
- Check that `src/app.py` path is correct
- Ensure `requirements.txt` has all dependencies
- Check build logs for specific error messages

**App loads but has errors:**
- Usually due to missing sample data file
- Ensure `data/sample_quotes.csv` exists in repository

**Import errors:**
- Verify all files are in correct directory structure
- Check that `src/` directory has `__init__.py` file

### Need Help?
- Check Streamlit Community Forum
- Review deployment logs in Streamlit Cloud dashboard
- Test locally first: `streamlit run src/app.py`

## 📁 Final Repository Structure
```
ai-discount-analyser/
├── .streamlit/
│   └── config.toml
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── ai_predictor.py
│   ├── data_processor.py
│   ├── static_analyzer.py
│   └── utils/
├── data/
│   └── sample_quotes.csv
├── tests/
├── .gitignore
├── requirements.txt
├── README.md
└── DEPLOYMENT_STEPS.md
```

## 🌟 Your App Features
- **No-cost deployment** on Streamlit Community Cloud
- **User-provided API keys** (no API costs for you)
- **Fast static analysis** without AI (< 2 seconds)
- **Professional UI** with interactive charts
- **Secure** - no sensitive data stored
- **Scalable** - supports unlimited users

**Ready to deploy!** 🚀
