from pydantic import BaseModel
from typing import Optional, List

class Email(BaseModel):
    id: int
    subject: str
    body: str
    category: str
    thread: List[str] = []

class Observation(BaseModel):
    email: Email
    step_count: int

class Action(BaseModel):
    action_type: str  # reply, archive, spam
    reply_text: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str