from stable_baselines3 import PPO
from app.environment import EmailTriageEnv

env = EmailTriageEnv("data/test_emails.json")
model = PPO.load("ppo_email_triage")

obs, _ = env.reset()

for _ in range(len(env.emails)):
    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)

    print("Action:", action)
    print("Reward:", reward)
    print("Info:", info)
    print("-" * 50)

    if done:
        break