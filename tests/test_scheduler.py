from datetime import datetime, timedelta
from apps.api.astra_os.scheduler.engine import ScheduleRequest, TaskInput, build_schedule


def test_scheduler_places_high_priority_task():
    start = datetime(2026, 7, 29, 9)
    request = ScheduleRequest(
        day_start=start,
        day_end=start + timedelta(hours=4),
        tasks=[TaskInput(id="t1", title="DSA", priority=90, deadline=start + timedelta(days=1), duration_minutes=60, difficulty=4, energy_required=4)],
        energy_by_hour={9: 4},
    )
    response = build_schedule(request)
    assert response.blocks[0].task_id == "t1"
    assert not response.unscheduled_task_ids
