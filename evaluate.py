from stable_baselines3 import PPO
from app.environment import EmailTriageEnv

LABELS = ["spam", "urgent", "informational", "followup", "archive"]

env = EmailTriageEnv("data/test_emails.json")
model = PPO.load("ppo_email_triage")

obs, _ = env.reset()

y_true = []
y_pred = []

for _ in range(len(env.emails)):
    action, _ = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)

    y_true.append(info["correct_label"])
    y_pred.append(info["chosen_label"])

    if done:
        break


# =============================
# Manual Confusion Matrix
# =============================
matrix = {label: {l: 0 for l in LABELS} for label in LABELS}

for true, pred in zip(y_true, y_pred):
    matrix[true][pred] += 1


# =============================
# Accuracy
# =============================
correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
accuracy = correct / len(y_true)

print(f"\nOverall Accuracy: {accuracy:.2%}\n")


# =============================
# Precision, Recall, F1
# =============================
print("Per Label Metrics:")
print("-" * 60)

for label in LABELS:
    tp = matrix[label][label]
    fp = sum(matrix[other][label] for other in LABELS if other != label)
    fn = sum(matrix[label][other] for other in LABELS if other != label)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    print(
        f"{label:15} "
        f"Precision: {precision:.2f}  "
        f"Recall: {recall:.2f}  "
        f"F1: {f1:.2f}"
    )


# =============================
# Print Confusion Matrix
# =============================
print("\nConfusion Matrix:")
print("-" * 60)

header = "True\\Pred".ljust(15) + "".join(l.ljust(15) for l in LABELS)
print(header)

for true_label in LABELS:
    row = true_label.ljust(15)
    for pred_label in LABELS:
        row += str(matrix[true_label][pred_label]).ljust(15)
    print(row)