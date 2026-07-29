from datetime import datetime, timedelta
from apps.api.astra_os.services.events import EventEvaluationInput, score_event


def test_event_recommender_attends_high_value_low_cost_event():
    start = datetime(2026, 7, 29, 18)
    recommendation = score_event(
        EventEvaluationInput(
            id="hack",
            title="AI Hackathon",
            starts_at=start,
            ends_at=start + timedelta(hours=3),
            networking=90,
            placement_value=85,
            skill_growth=95,
            interest=90,
            attendance_impact=5,
            deadline_conflict=0,
            travel_minutes=10,
        )
    )
    assert recommendation.recommendation == "attend"
    assert recommendation.score >= 68


def test_event_recommender_skips_low_value_high_conflict_event():
    start = datetime(2026, 7, 29, 10)
    recommendation = score_event(
        EventEvaluationInput(
            id="low",
            title="Generic Talk",
            starts_at=start,
            ends_at=start + timedelta(hours=2),
            networking=10,
            placement_value=5,
            skill_growth=10,
            interest=10,
            attendance_impact=80,
            deadline_conflict=90,
            travel_minutes=90,
            od_cost=50,
        )
    )
    assert recommendation.recommendation == "skip"
