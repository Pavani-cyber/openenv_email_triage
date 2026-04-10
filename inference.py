#!/usr/bin/env python3
"""
Email Triage Inference Script
Uses OpenAI-compatible API for intelligent email classification
Supports offline execution with local LLM servers
"""

import os
import json
import argparse
import sys
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: OpenAI package not installed. Run: pip install openai")
    sys.exit(1)

# Environment variables with defaults
API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-endpoint>")
MODEL_NAME = os.getenv("MODEL_NAME", "<your-active-model>")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# Email classification labels
LABELS = ["spam", "urgent", "informational", "followup", "archive"]

# Classification prompt template
CLASSIFICATION_PROMPT = """
You are an expert email triage assistant. Analyze the following email and classify it into exactly ONE of these categories:

- spam: Unwanted promotional, scam, or unsolicited commercial emails
- urgent: Time-sensitive emails requiring immediate action (deadlines, emergencies, critical updates)
- informational: Newsletters, announcements, product updates, or general information
- followup: Email threads, meeting reminders, or responses to previous conversations
- archive: Personal, casual, or non-urgent emails that can be archived

Email Details:
Subject: {subject}
Body: {body}
Sender Domain: {sender_domain}

Respond with ONLY the category name in lowercase, nothing else.
"""

def log_start(task: str) -> None:
    print(f"START: {task}")


def log_step(message: str) -> None:
    print(f"STEP: {message}")


def log_end(task: str) -> None:
    print(f"END: {task}")


def validate_environment() -> bool:
    """Validate required environment variables"""
    errors = []

    if not API_BASE_URL:
        errors.append("API_BASE_URL environment variable is required")

    if not MODEL_NAME:
        errors.append("MODEL_NAME environment variable is required")

    if not HF_TOKEN and not LOCAL_IMAGE_NAME:
        errors.append("HF_TOKEN environment variable is required unless LOCAL_IMAGE_NAME is used with from_docker_image().")

    if LOCAL_IMAGE_NAME and not hasattr(OpenAI, "from_docker_image"):
        if not HF_TOKEN:
            errors.append("LOCAL_IMAGE_NAME is set but OpenAI.from_docker_image() is unavailable; HF_TOKEN is required to use the API client.")

    if errors:
        log_step("Environment validation failed")
        for error in errors:
            log_step(f"{error}")
        return False

    log_step("Environment variables validated")
    return True


def create_openai_client() -> OpenAI:
    """Create OpenAI client with custom base URL or Docker image."""
    if LOCAL_IMAGE_NAME and hasattr(OpenAI, "from_docker_image"):
        log_step(f"Creating OpenAI client from Docker image: {LOCAL_IMAGE_NAME}")
        return OpenAI.from_docker_image(
            image=LOCAL_IMAGE_NAME,
            api_key=HF_TOKEN,
            base_url=API_BASE_URL
        )

    log_step("Creating OpenAI client with API_BASE_URL and HF_TOKEN")
    return OpenAI(
        api_key=HF_TOKEN,
        base_url=API_BASE_URL
    )

def classify_email_with_openenv(client: OpenAI, email: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """
    Classify an email using LLM and return OpenEnv-compatible observation
    Returns (prediction, observation_dict)
    """
    # Extract email components
    subject = email.get("subject", "")
    body = email.get("body", "")
    sender_domain = email.get("sender_domain", "unknown")

    # Create prompt
    prompt = CLASSIFICATION_PROMPT.format(
        subject=subject,
        body=body,
        sender_domain=sender_domain
    )

    try:
        # Make API call
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert email classifier."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.1  # Low temperature for consistent classification
        )

        # Extract prediction
        prediction = response.choices[0].message.content.strip().lower()

        # Validate prediction is in our labels
        if prediction not in LABELS:
            log_step(f"Warning: LLM returned invalid label '{prediction}', defaulting to informational")
            prediction = "informational"

        # Create OpenEnv-compatible observation
        # Use the same feature extraction as the RL environment
        try:
            from app.environment import EmailTriageEnv
            env = EmailTriageEnv()
            env.emails = [email]
            env.index = 0
            obs_array = env._get_obs()

            observation = {
                "spam_score": float(obs_array[0]),
                "urgent_score": float(obs_array[1]),
                "informational_score": float(obs_array[2]),
                "followup_score": float(obs_array[3]),
                "archive_score": float(obs_array[4]),
                "thread_depth": float(obs_array[5]),
                "subject_length": float(obs_array[6]),
                "body_length": float(obs_array[7]),
                "has_exclamation": bool(obs_array[8]),
                "has_question": bool(obs_array[9]),
                "timestamp_norm": float(obs_array[10])
            }
        except ImportError:
            # Fallback if OpenEnv environment not available
            observation = {
                "subject": subject,
                "body": body,
                "sender_domain": sender_domain,
                "llm_prediction": prediction
            }

        return prediction, observation

    except Exception as e:
        log_step(f"Error during LLM classification: {e}")
        return "informational", {}

def get_default_email() -> Dict[str, Any]:
    """Return a default email for testing"""
    return {
        "sender_domain": "example.com",
        "subject": "Important update for your account",
        "body": "Please review your recent account activity and respond if this looks unfamiliar.",
        "thread_depth": 1,
        "timestamp": 0,
        "label": "informational"
    }

def main():
    parser = argparse.ArgumentParser(description="Email triage inference using LLM")
    parser.add_argument(
        "--email",
        type=str,
        help="JSON string representing the email to classify"
    )
    parser.add_argument(
        "--input-file",
        type=str,
        help="Path to JSON file containing email payload"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate environment and exit"
    )

    args = parser.parse_args()

    log_start("inference")
    # Validate environment
    if not validate_environment():
        log_end("inference")
        sys.exit(1)

    if args.validate_only:
        log_step("Environment validation successful")
        log_end("inference")
        return

    # Load email data
    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                email = json.load(f)
        except Exception as e:
            log_step(f"Error loading email from file: {e}")
            log_end("inference")
            sys.exit(1)
    elif args.email:
        try:
            email = json.loads(args.email)
        except Exception as e:
            log_step(f"Error parsing email JSON: {e}")
            log_end("inference")
            sys.exit(1)
    else:
        email = get_default_email()
        log_step("Using default test email")

    # Create OpenAI client
    try:
        client = create_openai_client()
    except Exception as e:
        log_step(f"Error creating OpenAI client: {e}")
        log_end("inference")
        sys.exit(1)

    # Classify email
    log_step("Classifying email with LLM")
    prediction, observation = classify_email_with_openenv(client, email)

    # Prepare output
    action_index = LABELS.index(prediction)
    output = {
        "action": action_index,
        "label": prediction,
        "observation": observation,
        "email": email,
        "model": MODEL_NAME,
        "api_base": API_BASE_URL,
        "framework": "OpenEnv"
    }

    # Print result
    print(json.dumps(output, indent=2))
    log_end("inference")

if __name__ == "__main__":
    main()
