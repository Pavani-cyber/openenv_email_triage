# 🧪 Testing Guide

Complete testing checklist before Round 1 submission.

---

## ✅ Pre-Submission Tests

### 1. Environment Validation

```bash
# Run environment checks
python validate.py

# Expected output:
# ✓ Environment initialized
# ✓ Sample emails loaded
# ✓ Action space: Discrete(5)
# ✓ Observation space: Box(11,)
# ✓ Reset successful
# ✓ Step successful
```

### 2. Agent Testing

```bash
# Test trained agent
python test_agent.py

# Expected output:
# Testing agent on {N} emails...
# ✓ Agent predictions made
# ✓ Rewards calculated
# ✓ Info dicts formatted
# ✓ Mean reward: {value}
```

### 3. Evaluation

```bash
# Evaluate performance
python evaluate.py

# Expected output:
# Accuracy: {percentage}%
# Mean Reward: {value}
# Correct Predictions: {count}
# Incorrect Predictions: {count}
```

---

## 🖥️ Local Deployment Tests

### Test 1: Gradio Demo

```bash
# Start Gradio app
python app_gradio.py

# In browser, test:
✓ Load http://localhost:7860
✓ See email displayed
✓ Click "🔄 Reset Environment"
✓ Email changes
✓ Click "🤖 Agent Step"
✓ Action label appears
✓ Reward displayed
✓ Select manual action and click "✋ Manual Step"
✓ Results update
```

### Test 2: FastAPI Backend

```bash
# Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In new terminal, test endpoints:
curl http://localhost:8000/
# Response: {"message": "Email Triage OpenEnv Running 🚀", ...}

curl http://localhost:8000/health
# Response: {"status": "healthy"}

curl http://localhost:8000/reset
# Response: {"status": "reset", "observation": {...}, ...}

curl http://localhost:8000/agent-step
# Response: {"action": 0-4, "action_label": "...", "reward": {...}, ...}

curl -X POST http://localhost:8000/step -H "Content-Type: application/json" -d '{"action": 0}'
# Response: {"action": 0, "action_label": "spam", ...}
```

---

## 🐳 Docker Tests

### Test 3: Docker Build

```bash
# Build image
docker build -t email-triage:test .

# Expected:
# Successfully tagged email-triage:test
# Size: reasonably small

# Check size
docker images | grep email-triage
# Should be < 5GB
```

### Test 4: Docker Run

```bash
# Run container
docker run --rm -p 7860:7860 email-triage:test

# In browser test:
✓ Load http://localhost:7860
✓ See Gradio interface
✓ Test all buttons work
✓ Check browser console for errors

# Check logs
docker logs {container_id}
# Should see startup messages, no errors
```

---

## 📊 Performance Tests

### Test 5: Training

```bash
# Run training (fresh model)
python train.py

# Check:
✓ Training starts
✓ Updates every N steps
✓ Model saves successfully
✓ File: ppo_email_triage.zip created
✓ Size: 50-150 MB
```

### Test 6: Model Prediction Speed

```python
# Quick performance test
from stable_baselines3 import PPO
from app.environment import EmailTriageEnv
import time

env = EmailTriageEnv()
model = PPO.load("ppo_email_triage")

# Predict speed
start = time.time()
for _ in range(100):
    obs = env._get_obs()
    action, _ = model.predict(obs)
elapsed = time.time() - start

print(f"100 predictions in {elapsed:.2f}s")
print(f"Average: {elapsed/100*1000:.1f}ms per prediction")

# Expected: < 50ms per prediction
```

---

## 🔍 Code Quality Tests

### Test 7: Import Check

```bash
# Verify imports
python -c "from app.environment import EmailTriageEnv; print('✓ Environment imports OK')"
python -c "from app.main import app; print('✓ FastAPI app imports OK')"
python -c "import app_gradio; print('✓ Gradio app imports OK')"
```

### Test 8: Syntax Check

```bash
# Use Python's compile
python -m py_compile train.py
python -m py_compile app/environment.py
python -m py_compile app_gradio.py

# If no errors: Syntax OK
```

### Test 9: Linting (Optional)

```bash
# Install pylint (optional)
pip install pylint

# Check code
pylint app/environment.py --disable=all --enable=syntax-error
pylint train.py --disable=all --enable=syntax-error
```

---

## 📝 Documentation Tests

### Test 10: README Verification

Checklist for README.md:

- [ ] Problem statement clear
- [ ] RL formulation explained
- [ ] Installation instructions work
- [ ] Usage examples provided
- [ ] Docker commands present
- [ ] Troubleshooting section included
- [ ] All links valid and working

### Test 11: File Completeness

```bash
# Verify all required files exist
test -f Dockerfile && echo "✓ Dockerfile"
test -f requirements.txt && echo "✓ requirements.txt"
test -f README.md && echo "✓ README.md"
test -f LICENSE && echo "✓ LICENSE"
test -f app/environment.py && echo "✓ environment.py"
test -f app_gradio.py && echo "✓ app_gradio.py"
test -f train.py && echo "✓ train.py"
test -f ppo_email_triage.zip && echo "✓ Model file"
```

---

## 🌐 Hugging Face Spaces Pre-Deployment

### Test 12: Space Simulation

```bash
# Simulate HF Spaces environment
# (These are already working, but good to double-check)

# 1. Fresh clone simulation
git clone .
cd openenv_email_triage

# 2. Setup
bash setup.sh

# 3. Run app
python app_gradio.py

# 4. Test interface loads and functions correctly
```

### Test 13: Model File Check

```bash
# Verify model will be accessible
ls -lh ppo_email_triage.zip

# Should be:
# > 50 MB (model is large)
# < 200 MB (reasonable for deployment)

# Test loading
python -c "from stable_baselines3 import PPO; model = PPO.load('ppo_email_triage'); print('✓ Model loads successfully')"
```

---

## 🚀 Final Submission Checklist

Before pushing to GitHub:

```
Environment Tests:
- [ ] validate.py runs without errors
- [ ] test_agent.py runs without errors
- [ ] evaluate.py shows reasonable accuracy (>70%)

Local Tests:
- [ ] Gradio demo works on localhost
- [ ] FastAPI endpoints respond correctly
- [ ] No error messages in console

Docker Tests:
- [ ] Docker builds successfully
- [ ] Docker container runs
- [ ] Gradio accessible on localhost:7860

Code Tests:
- [ ] All imports work
- [ ] Syntax is valid
- [ ] No obvious bugs

Documentation Tests:
- [ ] README is complete
- [ ] All files present
- [ ] License included

Submission Readiness:
- [ ] GitHub repo is public
- [ ] All files committed and pushed
- [ ] Model file included
- [ ] Deployment guide available

Hugging Face Spaces:
- [ ] Space created
- [ ] Files uploaded
- [ ] Model accessible
- [ ] Interface loads
- [ ] All features work
```

---

## 🔄 Test Loop Before Submission

```bash
# Run this testing loop the day before submission

# 1. Fresh environment test
rm -rf venv
bash setup.sh

# 2. Run validation suite
python validate.py
python test_agent.py
python evaluate.py

# 3. Local deployment
python app_gradio.py
# (test manually in browser)

# 4. Docker deployment
docker build -t email-triage:final .
docker run -p 7860:7860 email-triage:final
# (test manually in browser)

# 5. Code quality
python -m py_compile train.py app/environment.py app_gradio.py

# 6. Documentation
# (review README, DEPLOYMENT, SUBMISSION docs)

# 7. Commit and push
git add .
git commit -m "Final submission: Email Triage OpenEnv Round 1"
git push origin main

# 8. Update HF Space
# (following DEPLOYMENT.md instructions)
```

---

## ⚠️ Common Issues and Fixes

| Issue              | Test      | Fix                                  |
| ------------------ | --------- | ------------------------------------ |
| Import Error       | Test 7    | Check Python path, venv activation   |
| Model not found    | Test 2, 6 | Run `python train.py`                |
| Port in use        | Test 3, 4 | Use different port                   |
| Slow predictions   | Test 6    | Check CPU/GPU, consider optimization |
| Docker build fails | Test 3    | Check Docker daemon, disk space      |

---

## 📊 Expected Outputs

### Successful Training Output

```
Logging to tmp...
Updated epsilon smoothing value
| rollout/                   |
|                  ep_len_mean | 8.75 |
| rollout/                   |
|                    ep_rew_mean | 50.3 |
---
Total timesteps: 100000
Model saved as ppo_email_triage.zip
✅ Training complete
```

### Successful Evaluation Output

```
Accuracy: 78.5%
Mean Reward: 58.3
Correct Predictions: 157
Incorrect Predictions: 43
---
Label-wise Accuracy:
  spam: 82.1%
  urgent: 76.3%
  informational: 74.8%
  followup: 78.9%
  archive: 80.1%
```

---

**All tests passing? Ready to submit! 🚀**
