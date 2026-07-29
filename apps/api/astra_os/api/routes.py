from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel, Field
from astra_os.scheduler.engine import BusyBlock, ScheduleRequest, TaskInput, build_schedule

router = APIRouter()


class TaskPayload(BaseModel):
    id: str
    title: str
    priority: int = Field(ge=1, le=100)
    deadline: datetime
    duration_minutes: int = Field(gt=0)
    difficulty: int = Field(default=3, ge=1, le=5)
    energy_required: int = Field(default=3, ge=1, le=5)
    dependencies: list[str] = Field(default_factory=list)
    preferred_start_hour: int | None = Field(default=None, ge=0, le=23)


class BusyPayload(BaseModel):
    title: str
    start: datetime
    end: datetime
    fixed: bool = True


class SchedulePayload(BaseModel):
    day_start: datetime
    day_end: datetime
    tasks: list[TaskPayload]
    busy: list[BusyPayload] = Field(default_factory=list)
    energy_by_hour: dict[int, int] = Field(default_factory=dict)


@router.get("/brief/today")
def today_brief() -> dict[str, object]:
    return {
        "headline": "Your day is optimized for early deadline progress and attendance safety.",
        "now": "Review your highest-risk task, then attend mandatory classes.",
        "alerts": [],
    }


@router.post("/planner/schedule")
def plan_day(payload: SchedulePayload) -> dict[str, object]:
    request = ScheduleRequest(
        day_start=payload.day_start,
        day_end=payload.day_end,
        tasks=[TaskInput(**task.model_dump()) for task in payload.tasks],
        busy=[BusyBlock(**block.model_dump()) for block in payload.busy],
        energy_by_hour=payload.energy_by_hour,
    )
    return build_schedule(request).to_dict()
