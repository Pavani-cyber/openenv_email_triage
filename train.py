#!/usr/bin/env python3
"""
Train PPO agent for Email Triage OpenEnv
"""

import warnings
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from app.environment import EmailTriageEnv

warnings.filterwarnings("ignore", category=DeprecationWarning)


def main():
    print("🚀 Initializing environment...")
    env = EmailTriageEnv("data/sample_emails.json")

    print("✅ Checking environment...")
    check_env(env)

    print("🤖 Creating PPO model...")
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=1e-4,
        n_steps=128,
        batch_size=64,
        gamma=0.99
    )

    print("📚 Training started...")
    model.learn(total_timesteps=100000)

    print("💾 Saving model...")
    model.save("ppo_email_triage")

    print("✅ Training complete")
    print("✅ Saved file: ppo_email_triage.zip")


if __name__ == "__main__":
    main()