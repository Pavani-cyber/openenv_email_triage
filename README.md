# 📧 Email Triage OpenEnv

An intelligent **multi-modal environment** for email triage classification, supporting both Reinforcement Learning and Large Language Models, built with OpenEnv framework for the **Meta × PyTorch OpenEnv Hackathon**.

**🎯 Key Features:**

- ✅ **Dual Inference Modes**: RL (PPO) and LLM-based classification
- ✅ **Offline-first design** (works with local LLM servers)
- ✅ **OpenEnv Framework** compliant
- ✅ Interactive Gradio demo on Hugging Face Spaces
- ✅ FastAPI backend for programmatic access
- ✅ Docker-ready for easy deployment
- ✅ Resource-efficient (2 vCPUs, 8 GB RAM)

---

## 🚀 Problem Statement

Email overload is a critical productivity challenge. This environment simulates **sequential email decision-making**, where an RL agent learns to intelligently classify emails into categories:

- **spam** - Unwanted promotional/scam emails
- **urgent** - Time-sensitive emails requiring immediate action
- **informational** - Newsletters, announcements, product updates
- **followup** - Email threads and meeting reminders
- **archive** - Personal/non-urgent emails

The goal is to **maximize triage accuracy** and help users prioritize their inbox.

---

## 🧠 RL Formulation

### State Space

Each observation is a **11-dimensional feature vector**:

```python
[
  spam_score,           # 0: Likelihood of spam keywords
  urgent_score,         # 1: Urgency indicators
  informational_score,  # 2: Newsletter/announcement markers
  followup_score,       # 3: Reminder/meeting keywords
  archive_score,        # 4: Personal/casual content
  thread_depth,         # 5: Email chain depth (normalized)
  subject_length,       # 6: Subject line length (normalized)
  body_length,          # 7: Email body length (normalized)
  has_exclamation,      # 8: Binary - exclamation mark present
  has_question,         # 9: Binary - question mark present
  timestamp_norm        # 10: Normalized timestamp
]
```

### Action Space

Discrete actions (5 possible outputs):

```
0 = spam
1 = urgent
2 = informational
3 = followup
4 = archive
```

### Reward Function

- **Correct classification**: +15.0 reward
- **Incorrect classification**: -5.0 reward
- **Repeating same action**: Additional -1.0 penalty

---

## 📊 Project Structure

```
openenv_project/
├── app/
│   ├── __init__.py              # Package init
│   ├── environment.py           # Gymnasium-based RL environment
│   ├── main.py                  # FastAPI backend
│   ├── models.py                # Pydantic models
│   ├── baseline.py              # Baseline agents
│   ├── grader.py                # Evaluation metrics
│   └── tasks.py                 # Task definitions
├── data/
│   ├── sample_emails.json       # Training data
│   └── test_emails.json         # Test data
├── inference.py                 # LLM-based inference (main script)
├── validate.py                  # Environment validation
├── app_gradio.py                # Gradio demo interface
├── train.py                     # RL training script
├── evaluate.py                  # RL evaluation script
├── test_agent.py                # Agent testing
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── openenv.yaml                 # OpenEnv framework config
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

---

## 🛠️ Installation

### Local Development

#### Prerequisites

- Python 3.10+
- pip or uv package manager

#### Setup

```bash
# Clone the repository
git clone https://github.com/Pavani-cyber/openenv_email_triage.git
cd openenv_email_triage

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Install uv for faster package management
pip install uv
uv pip install -r requirements.txt
```

---

## 🎮 Usage

### 1. Train the Agent

```bash
python train.py
```

This will:

- Initialize the `EmailTriageEnv` with sample data
- Train a PPO agent for 100,000 timesteps
- Save the trained model as `ppo_email_triage.zip`

**Training typically takes 5-10 minutes on CPU.**

### 2. Evaluate the Agent

```bash
python evaluate.py
```

This evaluates the trained agent on test data and prints performance metrics.

### 3. Run Gradio Demo (Interactive)

```bash
python app_gradio.py
```

Then open `http://localhost:7860` in your browser.

**Features:**

- Watch the AI agent classify emails in real-time
- Manually classify emails yourself
- Compare your predictions with the agent
- See feature scores for each email

### Demo script

```bash
python demo.py
```

This demonstrates:

environment initialization
reset behavior
action stepping
rewards
termination flags
grader correctness

This helps evaluators quickly verify the environment.

### 4. FastAPI Backend (Developer Mode)

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then visit:

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Available endpoints:**

- `GET /` - Health check and environment info
- `GET /actions` - Get available actions and action space
- `GET /state` - Get current environment state/observation
- `GET /reset` - Reset environment (also supports POST)
- `POST /reset` - Reset environment
- `GET /agent-step` - Agent takes an action using trained model
- `POST /step` - Manual action with `{"action": 0-4}`

---

## 🤖 LLM Inference (Alternative Mode)

This project supports **Large Language Model-based inference** as an alternative to RL agents. The `inference.py` script uses OpenAI-compatible APIs for intelligent email classification.

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# OpenAI-compatible API base URL
API_BASE_URL=http://localhost:8000/v1  # Local LLM server
# API_BASE_URL=https://api.openai.com/v1  # OpenAI API

# Model name
MODEL_NAME=gpt-3.5-turbo  # or llama2:7b, mistral:7b, etc.

# Hugging Face token (required)
HF_TOKEN=your_huggingface_token_here
```

### Usage

#### Validate Environment

```bash
python inference.py --validate-only
```

#### Classify Single Email

```bash
# Using JSON string
python inference.py --email '{"subject": "Urgent: Meeting at 3 PM", "body": "Please join the team meeting", "sender_domain": "company.com"}'

# Using JSON file
echo '{"subject": "Test email", "body": "This is a test", "sender_domain": "example.com"}' > email.json
python inference.py --input-file email.json
```

#### Offline Execution

For offline execution, configure `API_BASE_URL` to point to a local LLM server:

- **Ollama**: `http://localhost:11434/v1`
- **Local OpenAI-compatible API**: `http://localhost:8000/v1`
- **vLLM**: `http://localhost:8000/v1`

### Output Format

```json
{
  "action": 1,
  "label": "urgent",
  "observation": {
    "spam_score": 0.0,
    "urgent_score": 0.8,
    "informational_score": 0.1,
    "followup_score": 0.1,
    "archive_score": 0.0,
    "thread_depth": 0.0,
    "subject_length": 0.2,
    "body_length": 0.3,
    "has_exclamation": false,
    "has_question": false,
    "timestamp_norm": 0.5
  },
  "email": {...},
  "model": "gpt-3.5-turbo",
  "api_base": "http://localhost:8000/v1",
  "framework": "OpenEnv"
}
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t email-triage-app .
```

### Run Locally

```bash
docker run -p 7860:7860 email-triage-app
```

Visit `http://localhost:7860`

### Deploy to Hugging Face Spaces

1. **Create Repository**
   - Go to https://huggingface.co/new
   - Create a new Space
   - Select **Docker** as the runtime

2. **Upload Files**

   ```bash
   # Inside your Space repository
   git clone https://huggingface.co/spaces/pagadala-pavani/email-env
   cd email-triage-env

   # Copy files (except .git)
   cp -r ../openenv_project/* .

   # Push to HF Spaces
   git add .
   git commit -m "Initial commit"
   git push
   ```

3. **Build & Deploy**
   - HF Spaces will automatically build and deploy

---

## 📈 Performance Metrics

After training, the agent should achieve:

- **Accuracy**: ~75-85% on test set
- **Average Episode Reward**: ~50-70
- **Convergence**: Within 50,000-100,000 timesteps

---

## 🔧 Configuration

### Environment Parameters

Modify in `app/environment.py`:

```python
LABELS = ["spam", "urgent", "informational", "followup", "archive"]

# Keyword detection thresholds can be adjusted in _get_obs()
spam_keywords = ["free", "offer", "click", "winner", "prize", "million"]
urgent_keywords = ["urgent", "asap", "deadline", "immediately"]
# ... etc
```

### Training Hyperparameters

Modify in `train.py`:

```python
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=1e-4,     # Adjust learning rate
    n_steps=128,             # Steps per batch
    batch_size=64,           # Batch size
    gamma=0.99               # Discount factor
)
model.learn(total_timesteps=100000)  # Total training steps
```

---

## 📦 Dependencies

- **gymnasium** - RL environment framework
- **stable-baselines3** - PPO algorithm implementation
- **fastapi** - Web framework
- **gradio** - Interactive UI framework
- **numpy** - Numerical computing
- **torch** - Neural network backend
- **uvicorn** - ASGI server

See `requirements.txt` for exact versions.

---

## 🧪 Testing

```bash
# Unit tests
python -m pytest tests/

# Validate environment
python test_agent.py

# Check environment structure
python validate.py
```

---

## 🌐 OpenEnv Framework

This environment follows the OpenEnv standard by Meta and HuggingFace:

- ✅ Offline-first (no cloud APIs)
- ✅ Reproducible (seeded randomness)
- ✅ Gymnasium-compatible
- ✅ Self-contained with sample data
- ✅ Easy training/inference workflow

---

## 🚨 Troubleshooting

### "Model not found" error

```bash
# Retrain the model
python train.py
```

### Port already in use

```bash
# Use a different port
python app_gradio.py --share  # Auto-detects free port
```

### Out of memory (OOM)

```bash
# Reduce batch size in train.py
batch_size=32  # Instead of 64
n_steps=64     # Instead of 128
```

### Slow inference

- Ensure CUDA is available: `pip install torch --index-url https://download.pytorch.org/whl/cu118`
- Use GPU in Docker: `docker run --gpus all -p 7860:7860 email-triage-env:latest`

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---
