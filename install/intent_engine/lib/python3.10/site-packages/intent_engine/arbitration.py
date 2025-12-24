from dataclasses import dataclass
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class IntentData:
    id: str
    type: str
    source: str
    confidence: float
    meta: dict  # ← This should be Dict[str, Any] or just leave as dict
    priority_score: int = 0

class Arbitrator:
    def score_intent(self, intent: IntentData) -> int:
        """Apply rule-based scoring."""
        score = 0
        if intent.id == "stop":
            score = 100
        elif intent.id == "call_nurse":
            score = 90
        elif intent.id == "move":
            if intent.meta.get("obstacle_near", False):
                score = 30
            else:
                score = 70
        # Add more rules here
        return min(max(score, 0), 100)

    def arbitrate(self, intents: List[IntentData]) -> Optional[IntentData]:
        """Return highest-scoring intent, or None."""
        if not intents:
            return None
        scored_intents = []
        for intent in intents:
            intent.priority_score = self.score_intent(intent)
            scored_intents.append(intent)
        winner = max(scored_intents, key=lambda i: i.priority_score)
        logger.info(f"Arbitration winner: {winner.id} (score={winner.priority_score})")
        return winner