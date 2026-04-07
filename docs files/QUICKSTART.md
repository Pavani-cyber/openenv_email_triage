# ⚡ Quick Start Guide

Get Email Triage OpenEnv running in under 5 minutes!

---

## 🖥️ Option 1: Fastest Way (Docker)

```bash
# Build image
docker build -t email-triage:latest .

# Run container
docker run -p 7860:7860 email-triage:latest

# Open browser → http://localhost:7860
```

**Done!** The Gradio demo is now running.

---

## 💻 Option 2: Local Setup (Linux/macOS)

```bash
# 1. Clone and enter directory
git clone https://github.com/YOUR_USERNAME/openenv_email_triage.git
cd openenv_email_triage

# 2. Run setup (automatic venv + dependencies + model)
bash setup.sh

# 3. Activate environment
source venv/bin/activate

# 4. Run demo
python app_gradio.py

# 5. Open browser → http://localhost:7860
```

---

## 🪟 Option 3: Local Setup (Windows)

```bash
# 1. Clone and enter directory
git clone https://github.com/YOUR_USERNAME/openenv_email_triage.git
cd openenv_email_triage

# 2. Run setup (automatic venv + dependencies + model)
setup.bat

# 3. Activate environment (should be automatic)

# 4. Run demo
python app_gradio.py

# 5. Open browser → http://localhost:7860
```

---

## 🎮 Using the Demo

1. **🔄 Reset** - Load a new email to classify
2. **🤖 Agent Step** - Let the AI decide
3. **✋ Manual Step** - You decide

Compare your prediction with the agent's!

---

## 📚 Full Documentation

- **Setup & Deployment:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Overview:** See [README.md](README.md)
- **Submission Details:** See [SUBMISSION.md](SUBMISSION.md)

---

## 🚨 Troubleshooting

| Issue              | Solution                                             |
| ------------------ | ---------------------------------------------------- |
| Port 7860 in use   | Change port in code or find process: `lsof -i :7860` |
| Model not found    | Run `python train.py` to train locally               |
| Dependencies fail  | Delete venv and run setup script again               |
| Docker build fails | Ensure Docker daemon is running                      |

---

## 🔗 Key Commands

```bash
# Training
python train.py

# Evaluation
python evaluate.py

# Validation
python validate.py

# API Server (FastAPI)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Interactive Demo
python app_gradio.py
```

---

**Ready?** Pick your option above and get started! 🚀
