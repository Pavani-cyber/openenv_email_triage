from app.environment import EmailTriageEnv

LABELS = ["spam", "urgent", "informational", "followup", "archive"]


def run_demo():
    print("📧 Email Triage OpenEnv Demo")
    print("=" * 50)

    env = EmailTriageEnv("data/sample_emails.json")

    obs, info = env.reset()

    print("✅ Environment initialized")
    print("Initial observation:", obs)
    print("-" * 50)

    for step_num in range(5):
        # simple sample action
        action = env.action_space.sample()

        obs, reward, terminated, truncated, info = env.step(action)

        print(f"Step {step_num + 1}")
        print(f"Action: {action} ({LABELS[action]})")
        print(f"Reward: {reward}")
        print(f"Terminated: {terminated}")
        print(f"Truncated: {truncated}")
        print(f"Correct Label: {info['correct_label']}")
        print(f"Chosen Label: {info['chosen_label']}")
        print(f"Is Correct: {info['is_correct']}")
        print(f"Total Reward: {info['total_reward']}")
        print("Observation:", obs)
        print("-" * 50)

    print("🎉 Demo completed successfully")


if __name__ == "__main__":
    run_demo()