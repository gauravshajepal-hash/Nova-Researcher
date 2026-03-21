from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class Artifact(BaseModel):
    """An immutable record of a specific research finding or action."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_ids: List[str] = []
    agent_id: str
    skill_used: str
    topic: str
    data: Dict[str, Any]
    confidence: float = 1.0
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = {}

class UnmetNeed(BaseModel):
    """A broadcast request for a capability or data the current agent lacks."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    requester_agent_id: str
    need_type: str  # e.g., "full_text_pdf", "protein_folding", "admet_prediction"
    description: str
    priority: int = 1
    context: Dict[str, Any] = {}
    resolved_artifact_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class ResearchState(BaseModel):
    """The aggregate state of the research DAG."""
    artifacts: Dict[str, Artifact] = {}
    unmet_needs: List[UnmetNeed] = []
    last_updated: datetime = Field(default_factory=datetime.now)
