from fastapi import FastAPI
from pydantic import BaseModel
from stable_baselines3 import PPO
from app.environment import EmailTriageEnv
import numpy as np

app = FastAPI(
    title="Email Triage OpenEnv",
    description="RL Environment for intelligent email triage",
    version="1.0.0"
)

# Initialize environment and load pre-trained model
try:
    env = EmailTriageEnv()
    model = PPO.load("ppo_email_triage")
except FileNotFoundError:
    print("Warning: Model not found. Training a new model...")
    env = EmailTriageEnv()
    model = None

current_obs = None
current_email = None

LABELS = ["spam", "urgent", "informational", "followup", "archive"]


def get_obs_dict(obs):
    """Convert flat numpy observation array to interpretable dict"""
    if obs is None:
        return None
    return {
        "spam_score": float(obs[0]),
        "urgent_score": float(obs[1]),
        "informational_score": float(obs[2]),
        "followup_score": float(obs[3]),
        "archive_score": float(obs[4]),
        "thread_depth": float(obs[5]),
        "subject_length": float(obs[6]),
        "body_length": float(obs[7]),
        "has_exclamation": bool(obs[8]),
        "has_question": bool(obs[9]),
        "timestamp_norm": float(obs[10])
    }


@app.get("/")
def home():
    return {
        "message": "Email Triage OpenEnv Running 🚀",
        "status": "ready",
        "labels": LABELS
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/reset")
@app.post("/reset")
def reset():
    global current_obs, current_email
    obs, info = env.reset()
    current_obs = obs
    current_email = env.emails[env.index]
    
    return {
        "status": "reset",
        "observation": get_obs_dict(obs),
        "email_preview": {
            "sender_domain": current_email.get("sender_domain"),
            "subject": current_email.get("subject"),
            "label": current_email.get("label")
        }
    }


@app.get("/agent-step")
def agent_step():
    global current_obs, current_email
    
    if current_obs is None:
        obs, _ = env.reset()
        current_obs = obs
        current_email = env.emails[env.index]
    
    if model is None:
        return {"error": "Model not trained yet"}
    
    action, _ = model.predict(current_obs)
    obs, reward, terminated, truncated, info = env.step(int(action))
    
    current_obs = obs
    current_email = env.emails[env.index]
    
    return {
        "action": int(action),
        "action_label": LABELS[int(action)],
        "reward": float(reward),
        "is_correct": info.get("is_correct", False),
        "correct_label": info.get("correct_label"),
        "observation": get_obs_dict(obs),
        "email_preview": {
            "sender_domain": current_email.get("sender_domain"),
            "subject": current_email.get("subject"),
            "label": current_email.get("label")
        }
    }


class ActionInput(BaseModel):
    action: int


@app.post("/step")
def manual_step(data: ActionInput):
    global current_obs, current_email
    
    if current_obs is None:
        obs, _ = env.reset()
        current_obs = obs
        current_email = env.emails[env.index]
    
    obs, reward, terminated, truncated, info = env.step(data.action)
    current_obs = obs
    current_email = env.emails[env.index]
    
    return {
        "action": data.action,
        "action_label": LABELS[data.action],
        "reward": float(reward),
        "is_correct": info.get("is_correct", False),
        "correct_label": info.get("correct_label"),
        "observation": get_obs_dict(obs),
        "email_preview": {
            "sender_domain": current_email.get("sender_domain"),
            "subject": current_email.get("subject"),
            "label": current_email.get("label")
        }
    }