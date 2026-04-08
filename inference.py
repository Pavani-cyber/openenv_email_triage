import argparse
import json
from pathlib import Path

from stable_baselines3 import PPO
from app.environment import EmailTriageEnv, LABELS

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "ppo_email_triage"


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return PPO.load(str(MODEL_PATH))


def predict(email):
    env = EmailTriageEnv()
    env.emails = [email]
    env.index = 0
    obs = env._get_obs()
    model = load_model()
    action, _ = model.predict(obs)
    return int(action), LABELS[int(action)]


def default_email():
    return {
        "sender_domain": "example.com",
        "subject": "Important update for your account",
        "body": "Please review your recent account activity and respond if this looks unfamiliar.",
        "thread_depth": 1,
        "timestamp": 0,
        "label": "informational"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run email triage inference using the PPO model.")
    parser.add_argument(
        "--email",
        type=str,
        help="A JSON string representing the email to classify."
    )
    parser.add_argument(
        "--input-file",
        type=str,
        help="Path to a JSON file containing the email payload."
    )
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            email = json.load(f)
    elif args.email:
        email = json.loads(args.email)
    else:
        email = default_email()

    action, label = predict(email)
    output = {
        "action": action,
        "label": label,
        "email": email
    }
    print(json.dumps(output, indent=2))
