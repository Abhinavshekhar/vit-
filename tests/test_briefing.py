from datetime import date
from apps.api.astra_os.services.briefing import BriefTask, build_morning_brief


def test_morning_brief_prioritizes_highest_priority_task():
    brief = build_morning_brief(
        day=date(2026, 7, 29),
        tasks=[BriefTask(title="Low", priority=10, risk_level="low"), BriefTask(title="CAT prep", priority=95, risk_level="high")],
        attendance_alerts=[],
        recommended_events=["AI Hackathon"],
    )
    assert brief.focus == "CAT prep"
    assert brief.recommended_events == ["AI Hackathon"]
