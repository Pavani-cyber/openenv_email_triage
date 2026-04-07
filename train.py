from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from app.environment import EmailTriageEnv


def main():
    env = EmailTriageEnv("data/sample_emails.json")

    check_env(env)

    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=1e-4,
        n_steps=128,
        batch_size=64,
        gamma=0.99
    )

    model.learn(total_timesteps=100000)
    model.save("ppo_email_triage")

    print("✅ Training complete")


if __name__ == "__main__":
    main()