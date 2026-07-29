from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class BriefTask:
    title: str
    priority: int
    risk_level: str


@dataclass(frozen=True)
class BriefAttendanceAlert:
    course: str
    percent: float
    action: str


@dataclass(frozen=True)
class DailyBrief:
    day: date
    headline: str
    focus: str
    tasks: list[BriefTask] = field(default_factory=list)
    attendance_alerts: list[BriefAttendanceAlert] = field(default_factory=list)
    recommended_events: list[str] = field(default_factory=list)


def build_morning_brief(
    day: date,
    tasks: list[BriefTask],
    attendance_alerts: list[BriefAttendanceAlert],
    recommended_events: list[str],
) -> DailyBrief:
    ordered_tasks = sorted(tasks, key=lambda task: (-task.priority, task.risk_level))[:5]
    if ordered_tasks:
        focus = ordered_tasks[0].title
        headline = f"Start with {focus}; it is the highest-priority item today."
    elif attendance_alerts:
        focus = f"Attend {attendance_alerts[0].course}"
        headline = "Attendance safety is the main risk today."
    else:
        focus = "Protect a deep-work block"
        headline = "No urgent academic risk detected; use today to get ahead."
    return DailyBrief(
        day=day,
        headline=headline,
        focus=focus,
        tasks=ordered_tasks,
        attendance_alerts=attendance_alerts,
        recommended_events=recommended_events[:3],
    )
