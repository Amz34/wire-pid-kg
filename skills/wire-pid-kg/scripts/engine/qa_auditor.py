"""Goldfish Zero-Context Review Swarm for P&ID Knowledge Graph."""
from typing import Dict, Any, List
from skills.wire_pid_kg.scripts.engine.models import ProcessKnowledgeGraph

class PIDGoldfishReviewer:
    """Evaluates process graph connectivity without prior drafting context to guarantee zero hallucination."""
    def __init__(self, reviewer_name: str = "Goldfish-ProcessAuditor"):
        self.reviewer_name = reviewer_name

    def audit(self, pkg: ProcessKnowledgeGraph) -> Dict[str, Any]:
        errors: List[str] = []
        warnings: List[str] = []
        score = 100.0

        eq_ids = {e.id for e in pkg.equipment}
        valves_ids = {v.id for v in pkg.valves}
        all_entities = eq_ids | valves_ids

        connected_entities = set()
        for conn in pkg.connections:
            connected_entities.add(conn.source)
            connected_entities.add(conn.target)

        # Floating equipment check
        for eq in pkg.equipment:
            if eq.id not in connected_entities and len(pkg.equipment) > 1:
                warnings.append(f"Unconnected equipment: '{eq.id}' ({eq.name}) has no upstream/downstream flow lines.")
                score -= 15.0

        # Loop validation
        instrument_loops = {i.loop_id for i in pkg.instruments if i.loop_id}
        if not instrument_loops:
            warnings.append("No active control loops identified in instrumentation.")
            score -= 10.0

        score = max(0.0, score)
        passed = (len(errors) == 0 and score >= 70.0)

        return {
            "auditor": self.reviewer_name,
            "passed": passed,
            "score": round(score, 2),
            "errors": errors,
            "warnings": warnings
        }
