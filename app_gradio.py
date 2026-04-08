#!/usr/bin/env python3
"""
Gradio demo for Email Triage OpenEnv
Designed for Docker + Hugging Face Spaces
"""

import os
import warnings
import gradio as gr
from stable_baselines3 import PPO
from app.environment import EmailTriageEnv

warnings.filterwarnings("ignore", category=DeprecationWarning)

LABELS = ["spam", "urgent", "informational", "followup", "archive"]
MODEL_PATH = "ppo_email_triage.zip"

# ==========================
# Initialize Environment
# ==========================
env = EmailTriageEnv("data/sample_emails.json")

# ==========================
# Load PPO Model Safely
# ==========================
model = None
model_loaded = False

try:
    print("📂 Files inside container:", os.listdir("."))

    if os.path.exists(MODEL_PATH):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = PPO.load(MODEL_PATH)
        model_loaded = True
        print("✅ PPO model loaded successfully")
    else:
        print(f"⚠️ Model file not found: {MODEL_PATH}")

except Exception as e:
    print("⚠️ Failed to load PPO model")
    print("Error:", e)

# ==========================
# UI HELPERS
# ==========================
def format_email_display(email):
    return f"""
### 📩 Current Email
- **Sender Domain:** {email.get('sender_domain', 'unknown')}
- **Subject:** {email.get('subject', '')}
- **Body Preview:** {email.get('body', 'N/A')[:200]}...
- **True Label:** {email.get('label', 'unknown')}
- **Thread Depth:** {email.get('thread_depth', 0)}
"""


def format_obs_table(obs):
    return {
        "Feature": [
            "Spam Score",
            "Urgent Score",
            "Informational Score",
            "Followup Score",
            "Archive Score",
            "Thread Depth",
            "Subject Length",
            "Body Length",
            "Has Exclamation",
            "Has Question",
            "Timestamp"
        ],
        "Value": [round(float(x), 3) for x in obs]
    }


# ==========================
# ENV RESET
# ==========================
def reset_env():
    obs, _ = env.reset()
    email = env.emails[env.index]

    return (
        format_email_display(email),
        format_obs_table(obs),
        "✅ Environment reset"
    )


# ==========================
# AGENT ACTION
# ==========================
def agent_step():
    if not model_loaded:
        return (
            "❌ PPO model not loaded",
            {},
            ""
        )

    obs = env._get_obs()
    action, _ = model.predict(obs)

    obs, reward, _, _, info = env.step(int(action))
    email = env.emails[env.index]

    result = f"""
### 🤖 Agent Decision
- **Predicted Label:** {LABELS[int(action)]}
- **Reward:** {reward:.2f}
- **Correct:** {'✅' if info['is_correct'] else '❌'}
- **Expected:** {info['correct_label']}
- **Total Reward:** {info['total_reward']:.2f}
"""

    return result, format_obs_table(obs), format_email_display(email)


# ==========================
# MANUAL ACTION
# ==========================
def manual_action(action_idx):
    if action_idx is None:
        return "⚠️ Please choose a label", {}, ""

    obs, reward, _, _, info = env.step(int(action_idx))
    email = env.emails[env.index]

    result = f"""
### ✋ Manual Decision
- **Chosen Label:** {LABELS[int(action_idx)]}
- **Reward:** {reward:.2f}
- **Correct:** {'✅' if info['is_correct'] else '❌'}
- **Expected:** {info['correct_label']}
- **Total Reward:** {info['total_reward']:.2f}
"""

    return result, format_obs_table(obs), format_email_display(email)


# ==========================
# GRADIO UI
# ==========================
with gr.Blocks(
    title="Email Triage OpenEnv",
    theme=gr.themes.Soft()
) as demo:
    gr.Markdown("# 📧 Email Triage OpenEnv")
    gr.Markdown(
        "RL-powered intelligent email classification demo built for "
        "**Meta × PyTorch OpenEnv Hackathon** 🚀"
    )

    with gr.Row():
        reset_btn = gr.Button("🔄 Reset Environment")

    with gr.Row():
        with gr.Column():
            email_display = gr.Markdown()

        with gr.Column():
            obs_table = gr.Dataframe(interactive=False)

    with gr.Row():
        with gr.Column():
            agent_btn = gr.Button("🤖 Agent Step", variant="primary")
            agent_result = gr.Markdown()

        with gr.Column():
            action_dropdown = gr.Dropdown(
                choices=[(label, i) for i, label in enumerate(LABELS)],
                label="Choose Manual Action"
            )
            manual_btn = gr.Button("✋ Manual Step")
            manual_result = gr.Markdown()

    demo.load(
        reset_env,
        outputs=[email_display, obs_table, agent_result]
    )

    reset_btn.click(
        reset_env,
        outputs=[email_display, obs_table, agent_result]
    )

    agent_btn.click(
        agent_step,
        outputs=[agent_result, obs_table, email_display]
    )

    manual_btn.click(
        manual_action,
        inputs=[action_dropdown],
        outputs=[manual_result, obs_table, email_display]
    )

    gr.Markdown(
        """
---
### 📘 Labels
- **spam** → scam / promo / phishing
- **urgent** → immediate response needed
- **informational** → updates / newsletters
- **followup** → replies / reminders
- **archive** → personal / low priority
"""
    )


# ==========================
# RUN SERVER
# ==========================
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )