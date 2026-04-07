# 🔧 Troubleshooting Guide

Common issues and their solutions.

---

## ⚠️ Installation Issues

### Issue 1: `setuptools.build_meta` Error

**Error Message:**

```
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta'
```

**Cause:** setuptools is not properly installed or is outdated.

**Solution:**

**Windows (CMD or PowerShell):**

```bash
# Option 1: Fresh venv
rmdir /s /q venv
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-build-isolation -r requirements.txt
```

**Linux/macOS:**

```bash
# Option 1: Fresh venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-build-isolation -r requirements.txt
```

### Issue 2: Dependency Conflict on Windows

**Error:** Different packages failing during install

**Solution:**

```bash
# Try installing in order with --no-build-isolation
python -m pip install --upgrade pip setuptools wheel
python -m pip install --no-build-isolation numpy==1.24.3
python -m pip install --no-build-isolation gymnasium==0.29.1
python -m pip install --no-build-isolation torch==2.1.1
python -m pip install --no-build-isolation stable-baselines3==2.2.1
python -m pip install --no-build-isolation fastapi uvicorn pydantic gradio tqdm
```

### Issue 3: PyTorch Installation Fails

**Error:** torch package fails to install

**Workaround 1 - Use CPU-only torch:**

```bash
python -m pip install torch==2.1.1 --index-url https://download.pytorch.org/whl/cpu
```

**Workaround 2 - Skip torch, use pre-built:**

```bash
# Just skip installing locally, use the pre-trained model
python -m pip install --no-cache-dir -r requirements.txt --skip-pip-version-check
```

### Issue 4: `ModuleNotFoundError: No module named 'numpy._core.numeric'`

**Error Message:**

```
ModuleNotFoundError: No module named 'numpy._core.numeric'
```

**Cause:** Numpy version mismatch - pre-trained model was saved with numpy 1.24.x but newer versions (1.26+) changed module structure.

**Solution:**

```bash
# Use exactly numpy 1.24.3 (compatible with pre-trained model)
python -m pip install numpy==1.24.3 --force-reinstall

# Verify installation
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
```

**Important:** Do NOT use numpy 1.26.0 or higher with the pre-trained model. The `requirements.txt` is already configured with the correct version.

---

## 🐍 Python Version Issues

### Issue: Python Version Not Compatible

**Check Python version:**

```bash
python --version
```

**Requirements:** Python 3.10 or higher

**Solution:**

- Use Python 3.10, 3.11, or 3.12
- If using older Python, update it first

```bash
# Windows: Download from https://www.python.org/
# macOS: brew install python@3.11
# Linux: apt install python3.11
```

---

## 🏃 Runtime Issues

### Issue 4: Model File Not Found

**Error:** `FileNotFoundError: ppo_email_triage.zip`

**Solution:**

```bash
# Train a new model (5-10 minutes)
python train.py

# Or use pre-trained if available
# Copy ppo_email_triage.zip to project directory
```

### Issue 5: Gradio Demo Doesn't Load

**Error:** Browser shows connection error or timeout

**Solution:**

```bash
# Make sure you're running:
python app_gradio.py

# Then open: http://localhost:7860

# If using Jupyter/remote, use:
python app_gradio.py --share
```

### Issue 6: Port 7860 Already in Use

**Error:** `Address already in use`

**Solution:**

```bash
# Option 1: Kill the existing process
# Windows - Find and kill the process
tasklist | findstr python
taskkill /PID {PID} /F

# Linux/macOS - Kill process on port 7860
lsof -i :7860
kill -9 {PID}

# Option 2: Use different port in your script
# Edit app_gradio.py, change:
# demo.launch(server_port=7861)
```

---

## 🐳 Docker Issues

### Issue 7: Docker Build Fails

**Error:** Docker build stops with error

**Solution:**

```bash
# Clean build
docker system prune -a
docker build --no-cache -t email-triage:latest .

# Check for output
docker build -t email-triage:latest . 2>&1 | tail -50
```

### Issue 8: Docker Container Exits Immediately

**Error:** Container starts then stops

**Solution:**

```bash
# Run with logs
docker run -it -p 7860:7860 email-triage:latest

# Or check logs
docker logs {container_id}

# Common fix: Make sure Python dependencies are all installed
```

---

## 💾 Memory/Storage Issues

### Issue 9: Out of Memory During Training

**Error:** `MemoryError` or system freezes

**Solution:**

```bash
# Reduce batch size in train.py
# Change:
batch_size=64 → batch_size=32
n_steps=128 → n_steps=64

# Then run:
python train.py
```

### Issue 10: Disk Space Running Out

**Error:** `No space left on device`

**Solution:**

```bash
# Clean up unused Docker images
docker image prune -a

# Clean up old models
rm -f ppo_email_triage*.zip

# Check disk space
# Windows: dir C:\
# Linux/macOS: df -h
```

---

## 🔍 Debugging Tips

### Enable Verbose Output

```bash
# For pip installs
python -m pip install -v -r requirements.txt

# For model training
python train.py -v

# For Gradio
python app_gradio.py --debug
```

### Check Environment Variables

```bash
# Windows
set PYTHONPATH=C:\Users\PAVANI\OneDrive\Desktop\openenv_project
echo %PYTHONPATH%

# Linux/macOS
export PYTHONPATH=/path/to/openenv_project
echo $PYTHONPATH
```

### Test Individual Components

```python
# Test imports
python -c "import gymnasium; print('gymnasium OK')"
python -c "import stable_baselines3; print('stable_baselines3 OK')"
python -c "from app.environment import EmailTriageEnv; print('environment OK')"
python -c "from stable_baselines3 import PPO; print('PPO OK')"

# Test model loading
python -c "from stable_baselines3 import PPO; model = PPO.load('ppo_email_triage'); print('Model loaded OK')"

# Test environment
python validate.py
```

---

## 🆘 Not Finding Your Issue?

### Step 1: Check Error Message

Copy the exact error message and search in:

- [TESTING.md](TESTING.md) - Testing guide
- [README.md](README.md) - Project overview
- GitHub Issues

### Step 2: Try Fresh Setup

```bash
# Remove everything and start fresh
rm -rf venv
rm -rf ppo_email_triage.zip
bash setup.sh              # Linux/macOS
# OR
rmdir /s venv
setup.bat                  # Windows
```

### Step 3: Check Requirements

```bash
# Update pip first
python -m pip install --upgrade pip

# Try minimal install
python -m pip install gymnasium numpy torch stable-baselines3

# Then full install
python -m pip install -r requirements.txt
```

### Step 4: Rollback Versions

If recent versions cause issues, try older stable versions:

```
numpy==1.23.5
torch==2.0.1
gymnasium==0.28.1
```

### Step 5: Create Minimal Test

```python
# test.py
import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO

print("All imports OK")

# Test environment
env = gym.make("CartPole-v1")
obs, info = env.reset()
print(f"Environment OK: {obs.shape}")

print("✅ All basic tests passed")
```

Run: `python test.py`

---

## 📞 Getting Help

1. **Check this file** - Most common issues are here
2. **Read [TESTING.md](TESTING.md)** - Comprehensive test suite
3. **Check terminal output** - Error messages are usually clear
4. **Try setup scripts** - They handle most issues automatically
5. **Use fresh venv** - Corrupted virtual environments cause issues

---

## ✅ Verified Working Setups

**Windows 11:**

- Python 3.11.7
- pip 23.3.1
- setuptools 68.2.2

**macOS (M1/M2):**

- Python 3.11 (via Homebrew)
- pip 23.3.1
- conda suggested for better compatibility

**Ubuntu 22.04:**

- Python 3.10.12 (system)
- pip 23.3.1

---

## 🎯 Quick Fixes Cheat Sheet

| Issue            | Quick Fix                                                            |
| ---------------- | -------------------------------------------------------------------- |
| setuptools error | `pip install --upgrade setuptools wheel`                             |
| PyTorch fails    | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| Model not found  | `python train.py`                                                    |
| Port in use      | Kill process or use different port                                   |
| Out of memory    | Reduce batch size in train.py                                        |
| Docker fails     | `docker system prune -a && docker build --no-cache`                  |
| Import errors    | Fresh venv, `python -m pip install -r requirements.txt`              |

---

**Still stuck?** Check setup.sh or setup.bat - they include error handling for most issues! 🚀
