from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel, Field


class AgentContext(BaseModel):
    user_id: str
    sync_started_at: datetime = Field(default_factory=datetime.utcnow)
    dry_run: bool = False


class AgentFinding(BaseModel):
    kind: str
    title: str
    confidence: float = Field(ge=0, le=1)
    metadata: dict[str, object] = Field(default_factory=dict)


class AgentResult(BaseModel):
    agent: str
    findings: list[AgentFinding]
    warnings: list[str] = Field(default_factory=list)


class Agent(ABC):
    name: str

    @abstractmethod
    async def run(self, context: AgentContext) -> AgentResult:
        """Run an idempotent extraction or recommendation pass."""
