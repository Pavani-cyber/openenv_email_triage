"""
App package exports for the Email Triage OpenEnv project.
This makes imports cleaner across training, testing, and API files.
"""

from .environment import EmailTriageEnv
from .baseline import baseline_agent

__all__ = ["EmailTriageEnv", "baseline_agent"]