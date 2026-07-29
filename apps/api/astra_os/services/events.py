from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EventEvaluationInput:
    id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    networking: int = 0
    placement_value: int = 0
    skill_growth: int = 0
    interest: int = 0
    attendance_impact: int = 0
    deadline_conflict: int = 0
    travel_minutes: int = 0
    od_cost: int = 0

    def __post_init__(self) -> None:
        for field_name in (
            "networking",
            "placement_value",
            "skill_growth",
            "interest",
            "attendance_impact",
            "deadline_conflict",
            "od_cost",
        ):
            value = getattr(self, field_name)
            if not 0 <= value <= 100:
                raise ValueError(f"{field_name} must be between 0 and 100")
        if self.travel_minutes < 0:
            raise ValueError("travel_minutes must be non-negative")
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")


@dataclass(frozen=True)
class EventRecommendation:
    event_id: str
    recommendation: str
    score: float
    confidence: float
    reason: str


def score_event(event: EventEvaluationInput) -> EventRecommendation:
    benefit = (
        event.networking * 0.22
        + event.placement_value * 0.28
        + event.skill_growth * 0.22
        + event.interest * 0.18
    )
    cost = (
        event.attendance_impact * 0.18
        + event.deadline_conflict * 0.30
        + min(event.travel_minutes, 180) / 180 * 20
        + event.od_cost * 0.12
    )
    score = round(max(0, min(100, benefit - cost + 25)), 2)
    if score >= 68:
        recommendation = "attend"
        reason = "High career, skill, or interest value outweighs schedule and attendance costs."
    elif score >= 45:
        recommendation = "consider"
        reason = "Useful event, but confirm deadline and attendance buffers before committing."
    else:
        recommendation = "skip"
        reason = "Opportunity value does not justify the attendance, deadline, travel, or OD cost."

    confidence = round(0.55 + abs(score - 50) / 100, 2)
    return EventRecommendation(
        event_id=event.id,
        recommendation=recommendation,
        score=score,
        confidence=min(confidence, 0.95),
        reason=reason,
    )
