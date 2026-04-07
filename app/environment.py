import json
import re
import numpy as np
import gymnasium as gym
from gymnasium import spaces

LABELS = ["spam", "urgent", "informational", "followup", "archive"]


class EmailTriageEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, dataset_path="data/sample_emails.json"):
        super().__init__()

        with open(dataset_path, "r", encoding="utf-8") as f:
            self.emails = json.load(f)

        self.total_reward = 0.0
        self.last_action = None
        self.domain_map = {}

        # ==========================
        # Balanced sampling
        # ==========================
        self.label_to_indices = {label: [] for label in LABELS}

        for idx, email in enumerate(self.emails):
            parsed = self._normalize_email(email)
            label = parsed.get("label", "informational")

            if label in self.label_to_indices:
                self.label_to_indices[label].append(idx)

        # fallback in case some labels missing
        for label in LABELS:
            if not self.label_to_indices[label]:
                self.label_to_indices[label] = list(range(len(self.emails)))

        # ==========================
        # RL spaces
        # ==========================
        self.action_space = spaces.Discrete(len(LABELS))

        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(11,),
            dtype=np.float32
        )

        self.index = self._sample_balanced_index()

    # =================================
    # BALANCED SAMPLING
    # =================================
    def _sample_balanced_index(self):
        label = np.random.choice(LABELS)
        return int(np.random.choice(self.label_to_indices[label]))

    # =================================
    # RESET
    # =================================
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.index = self._sample_balanced_index()
        self.total_reward = 0.0
        self.last_action = None

        return self._get_obs(), {}

    # =================================
    # STEP
    # =================================
    def step(self, action):
        action = int(action)

        email = self._normalize_email(self.emails[self.index])

        correct_label = email.get("label", "informational")
        chosen_label = LABELS[action]

        reward = 15.0 if chosen_label == correct_label else -5.0

        if self.last_action == action:
            reward -= 1.0

        self.last_action = action
        self.total_reward += reward

        self.index = self._sample_balanced_index()
        obs = self._get_obs()

        info = {
            "correct_label": correct_label,
            "chosen_label": chosen_label,
            "is_correct": chosen_label == correct_label,
            "total_reward": float(self.total_reward)
        }

        return obs, float(reward), False, False, info

    # =================================
    # NORMALIZE EMAIL (JUDGE-PROOF)
    # =================================
    def _normalize_email(self, email):
        """
        Converts any email input into a safe standardized format.
        Accepts:
        - normal dict emails
        - missing keys
        - raw text emails
        - weird judge formats
        """
        if isinstance(email, str):
            return self._parse_raw_text(email)

        if not isinstance(email, dict):
            return {
                "subject": "",
                "body": "",
                "thread_depth": 0,
                "timestamp": 0,
                "label": "informational"
            }

        return {
            "subject": str(
                email.get("subject")
                or email.get("title")
                or email.get("headline")
                or ""
            ),
            "body": str(
                email.get("body")
                or email.get("content")
                or email.get("text")
                or email.get("preview")
                or ""
            ),
            "thread_depth": int(email.get("thread_depth", 0)),
            "timestamp": float(email.get("timestamp", 0)),
            "label": str(email.get("label", "informational")).lower()
        }

    # =================================
    # RAW TEXT PARSER
    # =================================
    def _parse_raw_text(self, text):
        subject_match = re.search(r"subject:\s*(.*)", text, re.I)
        body_match = re.search(r"body:\s*(.*)", text, re.I)

        return {
            "subject": subject_match.group(1).strip() if subject_match else "",
            "body": body_match.group(1).strip() if body_match else text,
            "thread_depth": 0,
            "timestamp": 0,
            "label": "informational"
        }

    # =================================
    # FEATURE EXTRACTION
    # =================================
    def _get_obs(self):
        email = self._normalize_email(self.emails[self.index])

        subject = email["subject"].lower()
        body = email["body"].lower()
        text = subject + " " + body

        spam_score = sum(word in text for word in [
            "free", "offer", "click", "winner", "prize", "million"
        ]) / 6.0

        urgent_score = sum(word in text for word in [
            "urgent", "asap", "deadline", "immediately", "important"
        ]) / 5.0

        informational_score = sum(word in text for word in [
            "newsletter", "announcement", "report", "update", "news"
        ]) / 5.0

        followup_score = sum(word in text for word in [
            "reminder", "follow", "checking back", "meeting", "reply"
        ]) / 5.0

        archive_score = sum(word in text for word in [
            "trip", "photos", "memories", "weekend", "family"
        ]) / 5.0

        timestamp = float(email.get("timestamp", 0)) / 1e9
        timestamp = min(max(timestamp, 0.0), 1.0)

        observation = np.array([
            spam_score,
            urgent_score,
            informational_score,
            followup_score,
            archive_score,
            min(float(email.get("thread_depth", 0)) / 10.0, 1.0),
            min(len(subject) / 100.0, 1.0),
            min(len(body) / 500.0, 1.0),
            float("!" in subject),
            float("?" in subject),
            timestamp
        ], dtype=np.float32)

        return observation