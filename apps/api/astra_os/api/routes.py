from fastapi import APIRouter
from astra_os.scheduler.engine import ScheduleRequest, build_schedule

router = APIRouter()


@router.get("/brief/today")
def today_brief() -> dict[str, object]:
    return {
        "headline": "Your day is optimized for early deadline progress and attendance safety.",
        "now": "Review your highest-risk task, then attend mandatory classes.",
        "alerts": [],
    }


@router.post("/planner/schedule")
def plan_day(request: ScheduleRequest) -> dict[str, object]:
    return build_schedule(request).model_dump()
