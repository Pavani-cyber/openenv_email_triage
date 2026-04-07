# 🚀 Deployment Guide - Hugging Face Spaces

This guide walks through deploying Email Triage OpenEnv to Hugging Face Spaces with full setup instructions.

---

## Prerequisites

- GitHub account with repository set up
- Hugging Face account (free tier works perfectly)
- Git installed locally

---

## Step 1: Prepare GitHub Repository

### 1.1 Create GitHub Repository

```bash
# Navigate to your project
cd openenv_project

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Email Triage OpenEnv"

# Create repo on GitHub, then add remote
git remote add origin https://github.com/YOUR_USERNAME/openenv_email_triage.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Files Are Included

```bash
# Check what will be tracked
git ls-files

# Should include:
# - app/environment.py
# - app/main.py
# - app_gradio.py
# - train.py
# - requirements.txt
# - Dockerfile
# - data/sample_emails.json
# - README.md
```

---

## Step 2: Create Hugging Face Space

### 2.1 Go to Hugging Face

1. Visit https://huggingface.co/new
2. Create a new Space by clicking **"New Space"**

### 2.2 Configure Space

Fill in:

- **Space name**: `email-triage-env` (or your preferred name)
- **License**: `mit` (or your choice)
- **Space SDK**: Select **"Docker"**
- **Visibility**: Public (for hackathon submission)

Click **"Create Space"**

---

## Step 3: Set Up Space Files

### 3.1 Clone the Space Repository

```bash
# After creating the space, clone it locally
git clone https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env
cd email-triage-env

# You should see a README.md and .gitattributes file
```

### 3.2 Copy Project Files

```bash
# From openenv_project directory, copy files to the space
# Option A: Manual copy
cp -r ../openenv_project/* .

# Option B: Or copy specific files
cp ../openenv_project/Dockerfile .
cp ../openenv_project/requirements.txt .
cp ../openenv_project/app_gradio.py .
cp -r ../openenv_project/app ./
cp -r ../openenv_project/data ./
cp ../openenv_project/train.py .
cp ../openenv_project/evaluate.py .
```

### 3.3 Verify Files

```bash
ls -la

# Should see:
# Dockerfile
# requirements.txt
# app_gradio.py
# app/
# data/
# README.md
# .gitattributes
# .gitignore (optional)
```

---

## Step 4: Train Model Locally (BEFORE Pushing)

### 4.1 Train Locally or Use Pre-trained

**Option A: Train Locally (Recommended)**

```bash
cd openenv_project

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python train.py

# Should output: "✅ Training complete"
# Creates: ppo_email_triage.zip
```

**Option B: Use Pre-trained Model**

If already trained, the model file should be in the project directory.

### 4.2 Verify Model Size

```bash
ls -lh ppo_email_triage.zip

# Should be ~50-100 MB
```

---

## Step 5: Add Pre-trained Model to Space

### 5.1 Use Git LFS (Recommended for Large Files)

```bash
# Navigate to space directory
cd email-triage-env

# Install git-lfs if needed
# On macOS: brew install git-lfs
# On Windows: https://git-lfs.github.com/
# On Linux: apt install git-lfs

# Initialize LFS in the space repo
git lfs install

# Track model files with LFS
git lfs track "*.zip"

# Add the model file
cp ../openenv_project/ppo_email_triage.zip .

# Commit and push
git add .gitattributes ppo_email_triage.zip
git commit -m "Add pre-trained model"
git push
```

### 5.2 Alternative: Build Model on Space (Slower)

Add this to Dockerfile before `CMD`:

```dockerfile
# Uncomment only if model doesn't exist
RUN if [ ! -f ppo_email_triage.zip ]; then python train.py; fi
```

---

## Step 6: Push to Hugging Face Space

```bash
# In the space directory
git add .
git commit -m "Add Email Triage OpenEnv"
git push
```

**Wait for build to complete** (usually 3-5 minutes):

1. Go to your Space on Hugging Face
2. Watch the **"Building"** progress
3. Once complete, you'll see the Gradio interface at `https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env`

---

## Step 7: Verify Deployment

### 7.1 Check the Gradio Interface

1. Visit your Space URL
2. Click **"🔄 Reset Environment"**
3. Click **"🤖 Agent Step"**
4. Verify emails load and agent predicts actions

### 7.2 Troubleshooting

**If the app doesn't load:**

- Check Space Logs: Click "🔧 Settings" → "Logs"
- Common issues:
  - Model file missing → Re-submit with LFS
  - Dependencies missing → Update requirements.txt
  - Port issues → Already handled (7860)

**If predictions fail:**

```bash
# Locally test the model
python test_agent.py
```

---

## Step 8: Create GitHub Release

### 8.1 Tag Your Release

```bash
git tag -a v1.0.0 -m "Round 1 Submission"
git push origin v1.0.0
```

### 8.2 Add GitHub Release Notes

1. Go to your GitHub repo
2. Click **"Releases"** → **"Create a new release"**
3. Fill in:
   - **Tag**: v1.0.0
   - **Title**: Email Triage OpenEnv - Round 1
   - **Description**: Include:

     ```
     ## Round 1 Submission

     **Hugging Face Space URL:** [Your Space URL]

     ### Features:
     - ✅ Offline-first environment
     - ✅ Trained PPO agent
     - ✅ Interactive Gradio demo
     - ✅ FastAPI backend
     - ✅ Docker-ready

     ### Training:
     - Script: `train.py`
     - Model: PPO with MlpPolicy
     - Accuracy: ~75-85%

     ### Usage:
     `python train.py` - Train agent
     `python app_gradio.py` - Run demo
     `docker build -t email-triage . && docker run -p 7860:7860 email-triage`
     ```

---

## Final Submission Checklist

- ✅ GitHub repository public
- ✅ Dockerfile included
- ✅ requirements.txt set
- ✅ Pre-trained model uploaded (ppo_email_triage.zip)
- ✅ Gradio app working on Hugging Face Spaces
- ✅ README.md with instructions
- ✅ Code comments and docstrings
- ✅ No external API calls
- ✅ All data bundled locally

---

## Example Submission Format

```
GitHub Repository: https://github.com/YOUR_USERNAME/openenv_email_triage
Hugging Face Space: https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env

Environment: EmailTriageEnv (app/environment.py)
Training Script: train.py (PPO, 100K timesteps)
Demo: app_gradio.py (Gradio interface)
Backend: app/main.py (FastAPI)

Features:
- 11-dimensional feature vector
- 5 classification labels
- Offline sample data
- No cloud dependencies
```

---

## Additional Resources

- **Hugging Face Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Gradio Docs**: https://gradio.app/docs/
- **Gymnasium Docs**: https://gymnasium.farama.org/
- **Stable Baselines 3**: https://stable-baselines3.readthedocs.io/

---

**Good luck with your submission! 🚀**
