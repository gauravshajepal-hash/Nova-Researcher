import abc
from typing import List, Optional
from src.reactor.models import Artifact, UnmetNeed
from src.reactor.event_bus import ArtifactReactor

class BaseAgent(abc.ABC):
    """Base class for all swarm workers and the PI."""
    
    def __init__(self, agent_id: str, reactor: ArtifactReactor):
        self.agent_id = agent_id
        self.reactor = reactor

    @abc.abstractmethod
    def run_cycle(self):
        """Standard heartbeat loop."""
        pass

    def publish(self, topic: str, skill: str, data: dict, parent_ids: List[str] = []) -> str:
        artifact = Artifact(
            agent_id=self.agent_id,
            topic=topic,
            skill_used=skill,
            data=data,
            parent_ids=parent_ids
        )
        return self.reactor.publish_artifact(artifact)

    def ask(self, need_type: str, description: str, context: dict = {}) -> str:
        need = UnmetNeed(
            requester_agent_id=self.agent_id,
            need_type=need_type,
            description=description,
            context=context
        )
        return self.reactor.broadcast_need(need)
