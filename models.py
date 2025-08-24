from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

# Pydantic models for API request/response

class UserCreate(BaseModel):
    session_uuid: Optional[UUID] = None

class User(BaseModel):
    id: UUID
    session_uuid: UUID
    created_at: datetime
    last_active: datetime

class SituationBase(BaseModel):
    title: str
    description: str
    persona_script: str
    difficulty_level: str = "beginner"
    category: str = "general"

class Situation(SituationBase):
    id: int
    created_at: datetime
    is_active: bool = True

class RoleplaySessionCreate(BaseModel):
    user_id: UUID
    situation_id: int

class RoleplaySession(BaseModel):
    id: UUID
    user_id: UUID
    situation_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str = "active"
    session_duration: int = 0

class DialogueMessageCreate(BaseModel):
    session_id: UUID
    message_type: str  # 'user' or 'persona'
    content: str
    message_order: int

class DialogueMessage(BaseModel):
    id: UUID
    session_id: UUID
    message_type: str
    content: str
    timestamp: datetime
    message_order: int

class SessionSummaryCreate(BaseModel):
    session_id: UUID
    performance_score: Optional[int] = None
    feedback_text: Optional[str] = None
    strengths: Optional[str] = None
    improvement_areas: Optional[str] = None
    key_insights: Optional[str] = None

class SessionSummary(BaseModel):
    id: UUID
    session_id: UUID
    performance_score: Optional[int]
    feedback_text: Optional[str]
    strengths: Optional[str]
    improvement_areas: Optional[str]
    key_insights: Optional[str]
    created_at: datetime

# Extended models for frontend responses
class SessionWithSituation(RoleplaySession):
    situation: Situation
    message_count: int = 0

class SessionWithMessages(RoleplaySession):
    situation: Situation
    messages: List[DialogueMessage]
    summary: Optional[SessionSummary] = None