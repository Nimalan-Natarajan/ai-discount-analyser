# Deployment Guide - AI-Driven Discount Analyser Tool

This guide provides multiple options to deploy your Streamlit application to make it accessible to users worldwide.

## 🚀 Quick Deployment Options

### 1. Streamlit Community Cloud (FREE & RECOMMENDED)
**Best for**: Quick deployment, free hosting, GitHub integration

#### Prerequisites:
- GitHub account
- Your code pushed to a GitHub repository

#### Steps:
1. **Push your code to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - AI Discount Analyser"
   git remote add origin https://github.com/YOUR_USERNAME/discount-predictor.git
   git push -u origin main
   ```

2. **Visit Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy your app**:
   - Click "New app"
   - Select your GitHub repository
   - Set the main file path: `src/app.py`
   - Click "Deploy!"

4. **Configure secrets** (for API key):
   - In your app dashboard, go to "Settings" → "Secrets"
   - Add your secrets:
     ```toml
     GEMINI_API_KEY = "your_actual_api_key_here"
     ```

#### Advantages:
- ✅ Free hosting
- ✅ Automatic updates from GitHub
- ✅ HTTPS by default
- ✅ Easy to manage

---

### 2. Heroku (PAID)
**Best for**: Professional deployment with more control

#### Prerequisites:
- Heroku account
- Heroku CLI installed

#### Files needed:
Create these files in your project root:

**Procfile**:
```
web: sh setup.sh && streamlit run src/app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**runtime.txt**:
```
python-3.11.5
```

#### Deployment steps:
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set GEMINI_API_KEY=your_actual_api_key_here

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

### 3. Railway (EASY & AFFORDABLE)
**Best for**: Simple deployment with GitHub integration

#### Steps:
1. Visit [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect it's a Python app
6. Set environment variables:
   - `GEMINI_API_KEY`: your API key
   - `PORT`: 8501
7. Deploy!

---

### 4. Google Cloud Platform (SCALABLE)
**Best for**: Enterprise deployment with high scalability

#### Using Cloud Run:
1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8080

   CMD ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
   ```

2. **Deploy to Cloud Run**:
   ```bash
   # Build and deploy
   gcloud run deploy discount-analyser \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=your_api_key
   ```

---

## 🔧 Pre-Deployment Checklist

### 1. Create deployment-ready files:
